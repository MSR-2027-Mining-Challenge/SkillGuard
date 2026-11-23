"""Draw the next stratified sample with notebook 03's own code, excluding previously used skills.

    .venv/bin/python -I results/skillguard_runs/next1000/draw_sample.py [--seed 2031] [--check-seed2030]

Notebook 03 (notebooks/03_stratified_sample.ipynb) is executed headless from an in-memory copy;
the file on disk is never written (asserted). Two in-memory changes are made and recorded in the
executed copy's metadata and in exclusion_provenance.json:
  1. settings: SEED and STRATUM_SIZES (400/300/300, the seed-2030 design);
  2. one line appended after `frame["stratum"] = frame.apply(assign, axis=1)`: representatives
     whose file_sha is in exclusions/excluded_file_shas.csv get the stratum label
     "excluded: previously used in SkillGuard experiments" (only rows that were eligible).
Everything else is unchanged: frame, strata, ordering by file_sha, random.Random(seed) keys,
smallest-key selection, manifest columns, and the notebook's byte-identical reproducibility check.
Design weights therefore use the reduced frame (population_N = eligible minus excluded), which is
the sampling frame of this draw; the change of frame is documented in the provenance file.

--check-seed2030 re-runs the unmodified draw with seed 2030 (no exclusions) and relies on the
notebook's own check that the result is byte-identical to the committed seed-2030 manifest.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

import nbformat
from nbclient import NotebookClient

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
NB = REPO / "notebooks/03_stratified_sample.ipynb"
EXCLUSIONS = HERE / "exclusions/excluded_file_shas.csv"
ANCHOR = 'frame["stratum"] = frame.apply(assign, axis=1)'
LABEL = "excluded: previously used in SkillGuard experiments"
SIZES = {"scripts": 400, "supporting_no_scripts": 300, "skill_md_only": 300}


def patched_notebook(seed, exclude):
    original = NB.read_bytes()
    nb = nbformat.reads(original.decode("utf-8"), as_version=4)
    settings = next(c for c in nb.cells if c.cell_type == "code" and re.search(r"^SEED\s*=", c.source, re.M))
    settings.source = re.sub(r"^SEED\s*=.*$", f"SEED = {seed}  # overridden by draw_sample.py", settings.source,
                             count=1, flags=re.M)
    settings.source = re.sub(r"^STRATUM_SIZES\s*=\s*\{.*?^\}", "STRATUM_SIZES = " + json.dumps(SIZES) +
                             "  # overridden by draw_sample.py", settings.source, count=1, flags=re.M | re.S)
    assert f"SEED = {seed}" in settings.source and "overridden" in settings.source.split("STRATUM_SIZES")[1][:200]
    patch = None
    if exclude:
        cells = [c for c in nb.cells if c.cell_type == "code" and ANCHOR in c.source]
        assert len(cells) == 1, "notebook 03 changed: exclusion anchor not found exactly once"
        rel = EXCLUSIONS.relative_to(REPO).as_posix()
        patch = (f"\n_EXCLUDED = {{r['file_sha'] for r in __import__('csv').DictReader(open(ROOT / {rel!r}, "
                 f"encoding='utf-8'))}}  # draw_sample.py\n"
                 f"_eligible = ~frame['stratum'].astype(str).str.startswith('excluded')\n"
                 f"frame.loc[_eligible & frame['file_sha'].isin(_EXCLUDED), 'stratum'] = {LABEL!r}  # draw_sample.py\n")
        cells[0].source = cells[0].source.replace(ANCHOR, ANCHOR + patch, 1)
    nb.metadata["draw_sample"] = {"source_notebook": str(NB.relative_to(REPO)),
                                  "source_sha256": hashlib.sha256(original).hexdigest(), "seed": seed,
                                  "stratum_sizes": SIZES, "exclusion_patch": patch,
                                  "exclusions_sha256": hashlib.sha256(EXCLUSIONS.read_bytes()).hexdigest()
                                  if exclude else None}
    return nb, original


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=2031)
    parser.add_argument("--check-seed2030", action="store_true")
    args = parser.parse_args()
    seed, exclude = (2030, False) if args.check_seed2030 else (args.seed, True)
    nb, original = patched_notebook(seed, exclude)
    client = NotebookClient(nb, timeout=None, kernel_name="python3", resources={"metadata": {"path": str(NB.parent)}})
    prov = HERE / "provenance"
    prov.mkdir(exist_ok=True)
    try:
        client.execute()
    finally:
        nbformat.write(nb, prov / f"03_stratified_sample_seed{seed}{'' if exclude else '_check'}.ipynb")
    assert NB.read_bytes() == original, "notebook 03 on disk changed"
    text = "\n".join(o.get("text", "") for c in nb.cells if c.cell_type == "code" for o in c.get("outputs", [])
                     if o.get("output_type") == "stream")
    m = re.search(r"(results/samples/[^\s:]+)", text)
    print(text[-3000:])
    if exclude and m:
        out = REPO / m.group(1).rstrip("/").split("/sample_manifest.csv")[0]
        summary = json.loads((HERE / "exclusions/summary.json").read_text())
        (out / "exclusion_provenance.json").write_text(json.dumps({
            "drawn_by": "results/skillguard_runs/next1000/draw_sample.py",
            "notebook": nb.metadata["draw_sample"], "exclusion_label": LABEL,
            "exclusions_summary": summary,
            "frame_change": "Representatives previously used in SkillGuard/Cisco/MalSkills experiments were removed "
                            "from the eligible frame before drawing; population_N and design weights refer to "
                            "the reduced frame. Two MalSkills entries could not be mapped to a DB identity and "
                            "therefore could not be excluded (exclusions/unresolved.csv)."}, indent=2) + "\n")
        print("provenance written to", out / "exclusion_provenance.json")


if __name__ == "__main__":
    main()
