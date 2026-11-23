# Lockbox policy (next 1,000-skill experiment, seed 2031)

**Purpose:** keep an untouched evaluation subset so that a future SkillGuard version (V3.3+, or any change to V3.2 after its freeze) can be evaluated on skills whose outputs did not influence its development.

## Rules

1. **Lockbox membership:** 250 of the 1,000 skills (100 scripts / 75 supporting / 75 SKILL.md-only).
   - Drawn by `make_manifests.py` with `random.Random(203125)` per stratum.
   - Listed in `manifests/lockbox_skill_ids.csv`; its sha256 is in `manifests/SHA256SUMS`.
2. **All tools scan all 1,000 skills,** so the three-way comparison uses the full sample.
3. **Item-level outputs for lockbox skills** go to `sealed/` subfolders of each output directory, with sha256 recorded in `sealed/SHA256SUMS`. Covered tools: SkillGuard V3.1 and V3.2, Cisco + ATR, and MalSkills after import.
   - Notebook 01 also writes per-skill Cisco reports into its local run folders. These are not split, so treat lockbox skills there the same way.
4. **During development, do not open item-level lockbox results.** This covers the `sealed/` files and lockbox skills in raw reports, and also means not reading those skills' files to design rules. The restriction applies until:
   - the version under evaluation is frozen (its source sha256 is recorded), and
   - its evaluation script is committed.
5. **Aggregate statistics over all 1,000 skills are allowed in reports and the paper.** Examples: flag rates, overlap counts, weighted prevalence.
6. **If a lockbox result is opened early,** record it in this file (date, who, why), and treat the affected skills as development data in later evaluations.

**Status (2026-11-22):** no lockbox output has been produced or opened yet. SkillGuard V3.2 was developed using only previously used samples and synthetic fixtures.
