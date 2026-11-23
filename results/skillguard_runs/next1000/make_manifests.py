"""Derive lockbox, pilot and batch manifests for the next 1,000-skill experiment (seed 2031).

    .venv/bin/python -I results/skillguard_runs/next1000/make_manifests.py

Source: results/samples/agent_skills_sample_seed2031_scripts400_supporting_no_scripts300_skill_md_only300/
sample_manifest.csv (notebook 03 via draw_sample.py). Rows are copied unchanged so notebook 01's
manifest mode accepts them.

Lockbox (leakage control): 250 skills (100 / 75 / 75 per stratum), chosen with
random.Random(LOCKBOX_SEED).sample() over each stratum's skill_ids sorted alphabetically. All tools
scan all 1,000 skills, but item-level outputs for lockbox skills must not be inspected during
SkillGuard V3.2+ development; they are evaluated only after a version is frozen (see
LOCKBOX_POLICY.md). The list itself is not secret: the rule concerns looking at outputs.

Pilot (12 skills): per stratum the 3 lowest-ranked OPEN skills plus one open incomplete folder (if
none among them), as in main1000, so the pilot never touches the lockbox.
Batches: rank round-robin into 4 stratified batches of 100/75/75 (main1000 design).
research_corpus_flags.csv flags skills from known adversarial/scanner-fixture repositories
(flag, not exclusion; analyses report rates with and without them).
"""

import csv
import hashlib
import random
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
SAMPLE = REPO / "results/samples/agent_skills_sample_seed2031_scripts400_supporting_no_scripts300_skill_md_only300/sample_manifest.csv"
STRATA = ["scripts", "supporting_no_scripts", "skill_md_only"]
LOCKBOX_SEED = 203125
LOCKBOX_SIZE = {"scripts": 100, "supporting_no_scripts": 75, "skill_md_only": 75}
# Repositories identified in the local skill_security_study as adversarial research corpora or scanner fixtures.
RESEARCH_CORPUS = re.compile(r"(?i)MalSkillBench|prompthound|PoisonedSkills|agent-skill-security|skill-vaccine|clawvet"
                             r"|skillguard|clawguard|skill-veil|claudelint|morale-skills|skill-redaction-audit")


def write(path, rows, fields):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        raise SystemExit(f"refusing to overwrite {path}")
    with path.open("w", newline="", encoding="utf-8") as h:
        w = csv.DictWriter(h, fieldnames=fields, lineterminator="\n", extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    print(path.relative_to(REPO), len(rows), digest[:12])
    return digest


def main():
    with SAMPLE.open(encoding="utf-8") as h:
        reader = csv.DictReader(h)
        fields = reader.fieldnames
        rows = list(reader)
    assert len(rows) == 1000
    rng = random.Random(LOCKBOX_SEED)
    lockbox = set()
    for s in STRATA:
        ids = sorted(r["skill_id"] for r in rows if r["stratum"] == s)
        lockbox.update(rng.sample(ids, LOCKBOX_SIZE[s]))
    for r in rows:
        r["evaluation_split"] = "lockbox" if r["skill_id"] in lockbox else "open"
    digests = {}
    split_fields = ["skill_id", "stratum", "file_sha", "repo", "skill_path", "evaluation_split"]
    digests["lockbox"] = write(HERE / "manifests/lockbox_skill_ids.csv",
                               [r for r in rows if r["evaluation_split"] == "lockbox"], split_fields)
    digests["open"] = write(HERE / "manifests/open_skill_ids.csv",
                            [r for r in rows if r["evaluation_split"] == "open"], split_fields)
    by = {s: sorted((r for r in rows if r["stratum"] == s), key=lambda r: int(r["rank_in_stratum"])) for s in STRATA}
    pilot = []
    for s in STRATA:
        open_rows = [r for r in by[s] if r["evaluation_split"] == "open"]
        chosen = open_rows[:3]
        if not any(r["folder_complete"] != "True" for r in chosen):
            incomplete = [r for r in open_rows[3:] if r["folder_complete"] != "True"]
            chosen.append(incomplete[0] if incomplete else open_rows[3])
        else:
            chosen.append(open_rows[3])
        pilot.extend(chosen)
    write(HERE / "manifests/pilot12_manifest.csv", pilot, fields)
    for b in range(1, 5):
        batch = [r for s in STRATA for r in by[s] if (int(r["rank_in_stratum"]) - 1) % 4 + 1 == b]
        write(HERE / f"manifests/batch{b}_of4_manifest.csv", batch, fields)
    flags = [{"skill_id": r["skill_id"], "stratum": r["stratum"], "repo": r["repo"], "evaluation_split": r["evaluation_split"]}
             for r in rows if RESEARCH_CORPUS.search(r["repo"])]
    write(HERE / "manifests/research_corpus_flags.csv", flags, ["skill_id", "stratum", "repo", "evaluation_split"])
    (HERE / "manifests/SHA256SUMS").write_text("".join(f"{v}  {k}\n" for k, v in sorted(digests.items())))


if __name__ == "__main__":
    main()
