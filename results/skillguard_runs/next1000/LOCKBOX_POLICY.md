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

**History rewrite (2026-11-23, approved by the repository owner).**
- **Scope:** only `skillguard-v3.2` was rewritten. No other branch, tag, pull request or fork contained the exposed commit, and every commit on the branch is by the same author. `main` and all other branches are untouched.
- **What changed:**
  - Commit `4d10ef5` was replaced by `d0674b3`: the same commit without its 44 `sealed/*.csv` files, and with the 9 `scans.csv` tables in their lockbox-free form.
  - The four later commits were re-created on top of it with byte-identical trees: `5220a7d`→`9bbd073`, `c8ad70f`→`fad484c`, `e55038c`→`aa9cf01`, `27b6655`→`cc8f0f4`. The branch tip's content is unchanged.
  - The push used `--force-with-lease` against the old tip `27b6655`.
- **Verification:** 39 exposed file versions with data were reachable from the old tip, and 0 are reachable from the new one. No rewritten commit contains lockbox skill IDs in a tool-output file. The tests pass, and the analysis tables and figures regenerate byte-identically.
- **Backup:** a local tag `backup/skillguard-v3.2-pre-rewrite-2026-11-23` (never pushed) and a verified Git bundle outside the repository keep the old history. They contain the exposed files and must stay private.

**What the rewrite cannot undo.** The outputs were publicly accessible:
- from about 04:00 to 20:45 (Pacific) on 2026-11-23 at the branch tip;
- until about 22:00 in the branch history.

After the rewrite:
- **GitHub by SHA:** GitHub still serves the old commit by its SHA (checked after the push), until GitHub garbage-collects unreachable objects. Purging them sooner requires a request to GitHub Support.
- **Copies:** any clone or fetch of `skillguard-v3.2` made during the window still holds the old commits. Anyone who fetched the branch must reset to the new history (`git fetch && git reset --hard origin/skillguard-v3.2`) instead of merging, or the old commits come back.
- **Wording:** we therefore **must not claim the lockbox outputs were never accessible**. The correct statement is: *item-level lockbox outputs were publicly accessible for about 18 hours on 2026-11-23; no team member opened them; they were then removed from the branch history.*

**Lockbox identities are public by design.** `manifests/lockbox_skill_ids.csv`, the batch manifests, the sample manifest and the export manifests (input file hashes, missing-file counts) were always meant to be public. They describe inputs, not tool outputs.

**Consequences for evaluation:**
- No team member or analysis has opened item-level lockbox findings. During the run, masked execution statuses of incomplete lockbox scans (no skill IDs, no findings) were printed once in the console.
- Because the outputs were publicly readable, a post-freeze evaluation should state this exposure.
- It should also confirm that the evaluated SkillGuard version was not tuned using these files. V3.2 was frozen (source sha256 `c15e43c3…`) before the run.

