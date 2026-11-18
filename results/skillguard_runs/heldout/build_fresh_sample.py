"""Draw a fresh held-out sample for SkillGuard V3 evaluation.

    .venv/bin/python -I results/skillguard_runs/heldout/build_fresh_sample.py

Same frame and key method as build_heldout_sample.py (read-only DB, dedup_primary
representatives, complete folders only, frame ordered by file_sha, key =
random.Random(SEED).random(), smallest keys), with:
  * SEED = 2029
  * EXCLUDED: every skill previously used for development or testing, i.e. the
    Nov-3 dev sample and every sample_manifest.csv under results/skillguard_runs/heldout/
    (matched by file_sha).
  * 100 skills, stratified: scripts 50, supporting_no_scripts 25, skill_md_only 25.
    Strata are over-/under-sampled relative to the population; per-stratum design
    weights are recorded for any population-level estimate.
Nothing in skill_security_study/ is read. Skill text is written to disk only for
static scanning; nothing is executed.
"""

from __future__ import annotations

import csv
import datetime as dt
import hashlib
import json
import random
import re
import sqlite3
from pathlib import Path, PurePosixPath

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
DB = REPO / "data/sample/agent_skills_sample.db"
DEV_MANIFEST = REPO / ("results/cisco_dataset_runs/agent_skills_sample/runs/"
                       "2026-11-03_173516_sample30-seed2027/sample/sample_manifest.csv")
SEED = 2029
ALLOCATION = {"scripts": 50, "supporting_no_scripts": 25, "skill_md_only": 25}


def slug(text):
    return re.sub(r"[^a-z0-9]+", "-", (text or "skill").lower()).strip("-")[:40] or "skill"


def safe_rel(name):
    p = PurePosixPath(name)
    return not (p.is_absolute() or ".." in p.parts or name.startswith("~") or "\\" in name)


def main():
    out = HERE / f"{dt.date.today():%Y-%m-%d}_fresh100-seed{SEED}"
    out.mkdir(exist_ok=False)
    previous = [DEV_MANIFEST] + sorted(HERE.glob("*/sample_manifest.csv"))
    excluded_shas = set()
    for manifest in previous:
        excluded_shas |= {row["file_sha"] for row in csv.DictReader(manifest.open(encoding="utf-8"))}

    con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    frame = con.execute(
        "SELECT repo_full_name, path, file_sha, name, content, has_scripts FROM artifacts "
        "WHERE dedup_primary = 1 AND content IS NOT NULL AND content != '' AND composition_fetched = 1 "
        "AND COALESCE(composition_truncated, 0) = 0 ORDER BY file_sha").fetchall()
    siblings = {}
    for repo, apath, entry, etype, fetched, content in con.execute(
            "SELECT repo_full_name, artifact_path, entry_name, entry_type, content_fetched, content FROM artifact_siblings"):
        siblings.setdefault((repo, apath), []).append((entry, etype, fetched, content))

    counts = {"previously_used": 0, "incomplete_text": 0, "unsafe_path": 0}
    strata = {k: [] for k in ALLOCATION}
    population = {k: 0 for k in ALLOCATION}
    for row in frame:
        repo, path, sha, name, content, has_scripts = row
        files = [s for s in siblings.get((repo, path), []) if s[1] == "file"]
        if any(f[2] != 1 or f[3] is None for f in files):
            counts["incomplete_text"] += 1
            continue
        if not all(safe_rel(f[0]) for f in files):
            counts["unsafe_path"] += 1
            continue
        stratum = "scripts" if has_scripts == 1 else ("supporting_no_scripts" if files else "skill_md_only")
        population[stratum] += 1
        if sha in excluded_shas:
            counts["previously_used"] += 1
            continue
        strata[stratum].append((row, files))

    manifest = []
    for stratum, n in ALLOCATION.items():
        rng = random.Random(SEED)
        keyed = sorted(((rng.random(), item) for item in strata[stratum]), key=lambda k: k[0])
        for key, ((repo, path, sha, name, content, _), files) in keyed[:n]:
            skill_id = f"{slug(name)}-{sha[:12]}"
            full = out / "R100" / skill_id / "full"
            full.mkdir(parents=True)
            (full / "SKILL.md").write_text(content, encoding="utf-8")
            for entry, _, _, text in files:
                target = full / entry
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(text, encoding="utf-8")
            manifest.append({"set": "R100", "stratum": stratum, "skill_id": skill_id, "repo": repo,
                             "skill_path": path, "file_sha": sha, "random_key": key, "n_files": 1 + len(files),
                             "design_weight": round(population[stratum] / n, 2)})
    with (out / "sample_manifest.csv").open("w", newline="", encoding="utf-8") as h:
        w = csv.DictWriter(h, fieldnames=list(manifest[0]))
        w.writeheader()
        w.writerows(manifest)
    assert not ({m["file_sha"] for m in manifest} & excluded_shas)
    meta = {"created_at": dt.datetime.now().astimezone().isoformat(), "seed": SEED, "allocation": ALLOCATION,
            "database_sha256": hashlib.sha256(DB.read_bytes()).hexdigest(), "frame_rows": len(frame),
            "excluded_manifests": [str(p.relative_to(REPO)) for p in previous],
            "excluded_file_shas": len(excluded_shas), "counts": counts,
            "eligible_population_per_stratum": population,
            "available_after_exclusion": {k: len(v) for k, v in strata.items()},
            "n_selected": len(manifest), "builder_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "note": "V3 rules were frozen before any skill in this sample was inspected."}
    (out / "sampling_metadata.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(json.dumps(meta, indent=2))


if __name__ == "__main__":
    main()
