"""Derive the pilot manifest and the 4 batch manifests from the approved 1,000-skill sample.

    .venv/bin/python -I results/skillguard_runs/main1000/make_manifests.py

Source: results/samples/agent_skills_sample_seed2030_scripts400_supporting_no_scripts300_skill_md_only300/
sample_manifest.csv (notebook 03, seed 2030). Rows are copied unchanged (same columns, design
weights, sample_id, database hash), so notebook 01's manifest check accepts them.

Pilot (12 skills): per stratum, ranks 1-3 by random key; the 4th slot is the lowest-ranked
incomplete folder if ranks 1-3 contain none, otherwise rank 4. This guarantees the pilot
exercises incomplete-folder handling while staying rule-based.

Batches: every stratum is split by rank with a round-robin (rank r -> batch (r-1) % 4 + 1), so
each batch has 100 scripts / 75 supporting / 75 SKILL.md-only and is itself a stratified random
subsample. The pilot skills stay in their batches (the pilot is a separate test run).
Also writes overlap_with_previous_samples.csv (flags; nothing is excluded).
"""

import csv
import hashlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
SAMPLE = REPO / "results/samples/agent_skills_sample_seed2030_scripts400_supporting_no_scripts300_skill_md_only300/sample_manifest.csv"
PREVIOUS = {
    "dev30_nov3": REPO / "results/cisco_dataset_runs/agent_skills_sample/runs/2026-11-03_173516_sample30-seed2027/sample/sample_manifest.csv",
    "heldout_seed2028": REPO / "results/skillguard_runs/heldout/2026-11-13_heldout-seed2028/sample_manifest.csv",
    "fresh100_seed2029": REPO / "results/skillguard_runs/heldout/2026-11-13_fresh100-seed2029/sample_manifest.csv",
}
STRATA = ["scripts", "supporting_no_scripts", "skill_md_only"]


def write(path, rows, fields):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        raise SystemExit(f"refusing to overwrite {path}")
    with path.open("w", newline="", encoding="utf-8") as h:
        w = csv.DictWriter(h, fieldnames=fields, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    print(path.relative_to(REPO), len(rows), hashlib.sha256(path.read_bytes()).hexdigest()[:12])


def main():
    with SAMPLE.open(encoding="utf-8") as h:
        reader = csv.DictReader(h)
        fields = reader.fieldnames
        rows = list(reader)
    by = {s: sorted((r for r in rows if r["stratum"] == s), key=lambda r: int(r["rank_in_stratum"])) for s in STRATA}

    pilot = []
    for s in STRATA:
        chosen = by[s][:3]
        if any(r["folder_complete"] != "True" for r in chosen):
            chosen.append(by[s][3])
        else:
            incomplete = [r for r in by[s] if r["folder_complete"] != "True"]
            chosen.append(incomplete[0] if incomplete else by[s][3])
        pilot.extend(chosen)
    write(HERE / "manifests/pilot12_manifest.csv", pilot, fields)

    for b in range(1, 5):
        batch = [r for s in STRATA for r in by[s] if (int(r["rank_in_stratum"]) - 1) % 4 + 1 == b]
        write(HERE / f"manifests/batch{b}_of4_manifest.csv", batch, fields)

    previous = {}
    for name, path in PREVIOUS.items():
        for r in csv.DictReader(path.open(encoding="utf-8")):
            previous.setdefault(r["file_sha"], []).append(name)
    flags = [{"skill_id": r["skill_id"], "stratum": r["stratum"], "file_sha": r["file_sha"],
              "previous_samples": "|".join(previous[r["file_sha"]]),
              "used_for_skillguard_development": "dev30_nov3" in previous[r["file_sha"]] or "heldout_seed2028" in previous[r["file_sha"]]}
             for r in rows if r["file_sha"] in previous]
    write(HERE / "manifests/overlap_with_previous_samples.csv", flags,
          ["skill_id", "stratum", "file_sha", "previous_samples", "used_for_skillguard_development"])


if __name__ == "__main__":
    main()
