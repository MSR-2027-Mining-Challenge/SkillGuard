"""Draw held-out GitSkills skills that SkillGuard was NOT developed on.

    .venv/bin/python -I results/skillguard_runs/heldout/build_heldout_sample.py

Source: data/sample/agent_skills_sample.db opened read-only. The frame is the same
13,000 representatives (dedup_primary = 1) as the Nov-3 sample. Nothing from
skill_security_study/ is read or reused. Skill content is only written to disk
as text files for static scanning; nothing is executed.

Exclusions: the 30 development skills (Nov-3 sample, matched by file_sha);
incomplete folders (truncated listing, or any sibling file without stored text)
so that coverage is not confounded by missing files; unsafe relative paths.

Two sets, drawn without replacement with the Nov-3 key method
(frame ordered by file_sha, key = random.Random(SEED).random(), smallest keys):
  H1 "random": stratified random. scripts 40, supporting_no_scripts 10,
     skill_md_only 10. Unbiased within strata. Used for prevalence and recall-style
     reading of misses.
  H2 "enriched": 30 skills with supporting files whose text matches a broad
     agent-keyword regex (ENRICH). This is deliberately biased toward positives and is
     used ONLY to estimate precision; it must not be used for prevalence or recall.
Stratum rule (simplified from the Nov-3 notebook): has_scripts = 1 -> scripts;
else sibling_count > 0 -> supporting_no_scripts; else skill_md_only.
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

REPO = Path(__file__).resolve().parents[3]
DB = REPO / "data/sample/agent_skills_sample.db"
DEV_MANIFEST = REPO / ("results/cisco_dataset_runs/agent_skills_sample/runs/"
                       "2026-11-03_173516_sample30-seed2027/sample/sample_manifest.csv")
SEED = 2028
H1_ALLOCATION = {"scripts": 40, "supporting_no_scripts": 10, "skill_md_only": 10}
H2_SIZE = 30
ENRICH = re.compile(
    r"(?i)\b(claude|cursor|codex|opencode|gemini|crontab|cronjob|subagents?|AGENTS\.md|CLAUDE\.md"
    r"|dangerously|--trust|launchctl|schtasks)\b")


def slug(text):
    return re.sub(r"[^a-z0-9]+", "-", (text or "skill").lower()).strip("-")[:40] or "skill"


def safe_rel(name):
    p = PurePosixPath(name)
    return not (p.is_absolute() or ".." in p.parts or name.startswith("~") or "\\" in name)


def main():
    out = Path(__file__).resolve().parent / f"{dt.date.today():%Y-%m-%d}_heldout-seed{SEED}"
    out.mkdir(exist_ok=False)
    con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    dev = {row["file_sha"] for row in csv.DictReader(DEV_MANIFEST.open(encoding="utf-8"))}

    frame = con.execute(
        "SELECT repo_full_name, path, file_sha, name, content, has_scripts, sibling_count "
        "FROM artifacts WHERE dedup_primary = 1 AND content IS NOT NULL AND content != '' "
        "AND composition_fetched = 1 AND COALESCE(composition_truncated, 0) = 0 ORDER BY file_sha").fetchall()
    siblings = {}
    for repo, apath, entry, etype, fetched, content in con.execute(
            "SELECT repo_full_name, artifact_path, entry_name, entry_type, content_fetched, content "
            "FROM artifact_siblings"):
        siblings.setdefault((repo, apath), []).append((entry, etype, fetched, content))

    excluded = {"dev_sample": 0, "incomplete_text": 0, "unsafe_path": 0}
    strata = {"scripts": [], "supporting_no_scripts": [], "skill_md_only": []}
    for row in frame:
        repo, path, sha, name, content, has_scripts, sib_count = row
        if sha in dev:
            excluded["dev_sample"] += 1
            continue
        files = [s for s in siblings.get((repo, path), []) if s[1] == "file"]
        if any(f[2] != 1 or f[3] is None for f in files):
            excluded["incomplete_text"] += 1
            continue
        if not all(safe_rel(f[0]) for f in files):
            excluded["unsafe_path"] += 1
            continue
        stratum = "scripts" if has_scripts == 1 else ("supporting_no_scripts" if files else "skill_md_only")
        strata[stratum].append((row, files))

    def draw(pool, n, rng_seed, exclude=frozenset()):
        rng = random.Random(rng_seed)
        keyed = [(rng.random(), item) for item in pool]  # one key per frame row, frame order fixed
        keyed = [k for k in keyed if k[1][0][2] not in exclude]
        return [item for _, item in sorted(keyed, key=lambda k: k[0])[:n]]

    chosen = []
    for stratum, n in H1_ALLOCATION.items():
        for item in draw(strata[stratum], n, SEED):
            chosen.append(("H1_random", stratum, item))
    taken = {item[0][2] for _, _, item in chosen}
    enrich_pool = [item for s in ("scripts", "supporting_no_scripts") for item in strata[s]
                   if ENRICH.search(item[0][4]) or any(ENRICH.search(f[3] or "") for f in item[1])]
    for item in draw(enrich_pool, H2_SIZE, SEED + 1, exclude=taken):
        stratum = "scripts" if item[0][5] == 1 else "supporting_no_scripts"
        chosen.append(("H2_enriched", stratum, item))

    manifest = []
    for set_name, stratum, ((repo, path, sha, name, content, _, _), files) in chosen:
        skill_id = f"{slug(name)}-{sha[:12]}"
        full = out / set_name / skill_id / "full"
        full.mkdir(parents=True)
        (full / "SKILL.md").write_text(content, encoding="utf-8")
        for entry, _, _, text in files:
            target = full / entry
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(text, encoding="utf-8")
        manifest.append({"set": set_name, "stratum": stratum, "skill_id": skill_id, "repo": repo,
                         "skill_path": path, "file_sha": sha, "n_files": 1 + len(files),
                         "skill_md_sha256": hashlib.sha256(content.encode()).hexdigest()})

    with (out / "sample_manifest.csv").open("w", newline="", encoding="utf-8") as h:
        w = csv.DictWriter(h, fieldnames=list(manifest[0]))
        w.writeheader()
        w.writerows(manifest)
    meta = {
        "created_at": dt.datetime.now().astimezone().isoformat(), "seed": SEED, "database": str(DB.relative_to(REPO)),
        "database_sha256": hashlib.sha256(DB.read_bytes()).hexdigest(),
        "frame_rows": len(frame), "excluded": excluded,
        "eligible_per_stratum": {k: len(v) for k, v in strata.items()},
        "enriched_pool_size": len(enrich_pool), "enrich_regex": ENRICH.pattern,
        "h1_allocation": H1_ALLOCATION, "h2_size": H2_SIZE,
        "n_selected": dict((s, sum(m["set"] == s for m in manifest)) for s in ("H1_random", "H2_enriched")),
        "note": "H2 is keyword-enriched (biased); use only for precision.",
        "builder_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    (out / "sampling_metadata.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(json.dumps(meta, indent=2))


if __name__ == "__main__":
    main()
