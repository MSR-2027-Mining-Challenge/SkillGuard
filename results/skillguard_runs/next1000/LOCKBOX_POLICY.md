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

## Exposure record (2026-11-23)

**What happened.** The repository is public. Commit `4d10ef5`, pushed to `origin/skillguard-v3.2` on 2026-11-23, tracked the `sealed/` folders of the full run.
- **Sealed files:** 44 item-level files for lockbox skills (SkillGuard behaviors/chains/coverage, Cisco + ATR findings, MalSkills SSO findings and pattern verdicts, analysis rows).
- **Open `scans.csv` tables** (Cisco + ATR and MalSkills): these also contained the lockbox rows, i.e. per-skill scan statuses and MalSkills verdicts, patterns and SSO counts.
- **Earlier commits:** `6cda695` and `688c23e` tracked only empty, header-only sealed files from the open-only pilot.

**What was fixed on 2026-11-23:**
- **Open tables:** `seal_scan_tables.py` moved the lockbox rows of the existing `scans.csv` tables into `sealed/`. Rows are moved unchanged; open + sealed equals the original.
- **Runners:** both runners now split `scans.csv` this way.
- **Tracking:** all `sealed/` contents except `SHA256SUMS` were removed from tracking and are ignored (`.gitignore`). The files remain on the machine that ran the experiment.
- **Verification:** the three-way analysis re-ran byte-identically after the change.

**What cannot be repaired without rewriting Git history.**
- Commit `4d10ef5` is still in the branch history on GitHub. Anyone can read these files there, as can any clone or fork made since.
- Removing them would need a history rewrite plus a force-push of `skillguard-v3.2`. Even then, existing clones, forks and caches would keep them.
- This decision belongs to the repository owner and has not been taken.

**Lockbox identities are public by design.** `manifests/lockbox_skill_ids.csv`, the batch manifests, the sample manifest and the export manifests (input file hashes, missing-file counts) were always meant to be public. They describe inputs, not tool outputs.

**Consequences for evaluation:**
- No team member or analysis has opened item-level lockbox findings. During the run, masked execution statuses of incomplete lockbox scans (no skill IDs, no findings) were printed once in the console.
- Because the outputs were publicly readable, a post-freeze evaluation should state this exposure.
- It should also confirm that the evaluated SkillGuard version was not tuned using these files. V3.2 was frozen (source sha256 `c15e43c3…`) before the run.

