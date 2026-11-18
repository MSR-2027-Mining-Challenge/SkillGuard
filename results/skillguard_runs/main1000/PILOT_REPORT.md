# 12-skill pilot for the 1,000-skill experiment (seed 2030)

The approved setup is unchanged: allocation 400/300/300, seed 2030, previously examined skills flagged rather than excluded, and incomplete folders scanned as partial coverage. The full 1,000-skill run has **not** been started.

## What was run

| Step | Output |
|---|---|
| 1,000-skill sample (notebook 03, `SEED=2030`, sizes 400/300/300) | `results/samples/agent_skills_sample_seed2030_scripts400_supporting_no_scripts300_skill_md_only300/` |
| Draw reproducibility check (notebook 03 re-run) | "Reproducibility check passed: the regenerated sample is byte-identical" |
| Pilot and batch manifests | `manifests/pilot12_manifest.csv`, `manifests/batch{1..4}_of4_manifest.csv`, `manifests/overlap_with_previous_samples.csv` (`make_manifests.py`) |
| Cisco pilot run 1 (notebook 01, 4 configurations) | `results/cisco_dataset_runs/agent_skills_sample/runs/2026-11-15_213631_pilot12-seed2030-run1/` |
| Cisco pilot run 2 (reproducibility) | `…/2026-11-15_214127_pilot12-seed2030-run2/` |
| Crash test: run 3 hard-killed, recovery scan, reanalysis, merge | `…/2026-11-15_214620_…-run3-crashtest/`, `…/214803_…-run3-recovery/`, `…/215105_…-run3-crashtest-reanalysis/`; merged output in `pilot_checks/crashtest_merged/` |
| SkillGuard V3.1 (frozen `eebc59e7`) on the exported folders | `skillguard/<run>/` (`run_skillguard_on_run.py`) |
| Executed notebook copies (provenance) | `provenance/*.ipynb` |

**How notebooks were run.** They were executed headless by `run_notebook.py`, which overrides settings in an in-memory copy. The notebook files on disk were not modified; this is asserted after each run, and `git status` shows `notebooks/` clean.

## Sample, design weights and overlap

| Stratum | n / N | Design weight | Incomplete folders | Previously examined skills (flagged) |
|---|---|---|---|---|
| scripts | 400 / 1,404 | 3.51 | 112 (89 with files lacking stored text, 23 with truncated listings) | 34 (dev30: 3, held-out 2028: 14, fresh-100: 17) |
| supporting_no_scripts | 300 / 2,634 | 8.78 | 36 (files lacking stored text) | 7 (dev30: 1, held-out 2028: 5, fresh-100: 1) |
| skill_md_only | 300 / 7,260 | 24.20 | 0 | 3 (fresh-100) |

- **Overlap with earlier samples:** 44 skills in total; the plan expected about 41. 23 of them were used during SkillGuard development or V2 held-out testing. These are flagged in `overlap_with_previous_samples.csv` for the planned sensitivity analysis.
- **Overlap with the earlier hand-picked pilots:** notebook 03 also reports 1 skill: `implementing-canary-tokens-for-netw-07811ef04df1`, which is in this pilot.
- **Batches:** the 4 batches partition the 1,000 skills exactly (1,000 unique), each with 100 / 75 / 75. A rank round-robin makes each batch a stratified random subsample.

## Pilot results

**Pilot selection.** Ranks 1–3 in each stratum. The 4th slot is the lowest-ranked incomplete folder if ranks 1–3 have none, which replaced scripts rank 4 with rank 9, `quiz-generator`. The pilot therefore covers both kinds of incomplete folder: `dot-matrix-xhs` (a listed file without stored text) and `quiz-generator` (a truncated listing).

| Check | Result |
|---|---|
| Scanner | `skill-scanner 2.3.1`; policy fingerprint `3f48e661…` (same as the Nov-3 baseline); `--policy balanced`; no LLM or OSV analyzers |
| Cisco scans | **48/48 COMPLETE** (12 skills × 4 configurations); 0 failures, 0 timeouts, 0 partial; all rule-contract checks passed |
| Runtime per scan | mean **4.89 s**, max 5.16 s (the plan assumed 5.08 s); 242 s wall for the whole pilot run, including export |
| Incomplete folders | Both were exported with the files available and scanned in all 4 configurations. They are flagged `folder_complete = False` (and `listing_complete = False` for the truncated one). |
| Cisco findings | 10 security findings in 2 skills (8 in `implementing-canary-tokens`, 2 in `taxonomy`), plus metadata-quality notes |
| SkillGuard V3.1 | 0 behaviors in the 12 skills; 0.096 s total (8 ms per skill) |
| SkillGuard file coverage | 33 exported files: 13 analyzed as code, 16 covered only by the text heuristic, 4 not analyzed (unsupported or data formats); 3 Python blocks failed to parse (`implementing-canary-tokens` SKILL.md lines 261/271/280) |
| **Reproducibility** (run 1 vs run 2) | Identical exported files (45/45 sha256), identical Cisco findings in all 48 reports (rule, file, line, severity), identical scan statuses, identical SkillGuard outputs (12/12) |
| **Crash recovery** | Run 3 was hard-killed (SIGKILL on the whole process group) after 80 s. 3 skills had all 4 reports; `quiz-generator` had 3 of 4 and was re-scanned in full; 8 had not started. No stray processes remained. Recovery scan of 9 skills plus reanalysis of the crashed folder, merged with `recover_batch.py`: **identical to run 1** (48/48 statuses, 50/50 finding rows) |
| Storage | about 1.1 MB per 12-skill run, so roughly 0.1 GB for the 1,000-skill run |

## Problems found

1. **Truncated listings show 0 missing files.** For the 23 truncated-listing script skills, the true file count is unknown, so `missing_files = 0` understates the gap. The analysis must use `listing_complete` (not only `missing_files`) and report these skills as having unknown coverage.
2. **Reanalysis setting.** Reanalysis of a crashed batch must set `ALLOW_INCOMPLETE_FOLDERS=True`, the same as the scan. Otherwise missing full-folder reports of incomplete skills are labeled `SKIPPED_INCOMPLETE_FOLDER` instead of `MISSING_REPORT`. The merge is unaffected because unfinished skills are always taken from the recovery run, but the setting keeps the reanalysis tables honest. This is now part of the runbook.
3. **Notebook 01 cannot resume.** Mitigation tested: 4 batches plus `recover_batch.py`. The most a crash can cost is re-scanning the unfinished skills of the batch in progress.
4. **Small sample.** 12 skills with 0 SkillGuard behaviors is expected (they are rare), but the pilot says nothing about detection rates; that is what the full run is for.
5. **Notebook 01 edits tracked report-index files.** Its last section adds every run to `results/reports/README.md` and `results/reports/index.html`, and writes `results/reports/agent_skills_sample/<run>/`. For the pilot, the two index files were restored to their committed state; the pilot report folders were kept, as new files only. **Decision needed for the full run:** let it index the 4 batch runs (an expected, meaningful change to two tracked files), or restore the index afterwards.
6. **Cosmetic:**
   - nbclient warns that the local kernel uses unencrypted TCP. It is localhost only and harmless.
   - Notebook 01 also writes its usual `manual_review_template.csv` and figures. These are not used, and no manual labeling is planned.

## Projection for the full run

| | |
|---|---|
| Cisco calls | 4,000 (1,000 × 4); the 148 incomplete folders are scanned as partial coverage |
| Runtime | 4,000 × 4.89 s ≈ **5.4 h** sequential, about **82 min per 250-skill batch** |
| SkillGuard | about 10–20 s in total |
| Storage | about 0.1–0.3 GB |

## Recommendation

**Ready to launch**, using this runbook (stop for approval first):

1. **Run each batch** (b = 1..4) with notebook 01, via `run_notebook.py`:
   - `RUN_MODE="scan"`, `SELECTION_MODE="manifest"`, `SAMPLE_MANIFEST="results/skillguard_runs/main1000/manifests/batch{b}_of4_manifest.csv"`
   - `EXPERIMENT_NAME="sample1000-seed2030-batch{b}"`, `ALLOW_INCOMPLETE_FOLDERS=True`, `POLICY="balanced"`, `LENIENT=False`, `ENABLE_OSV=False`, `ENABLE_LLM_CONFIGS=False`
   - Run headless under `caffeinate`, one batch at a time.
2. **After each batch:**
   - check that its `scan_summary.csv` has 1,000 rows, all with an executed status
   - run `run_skillguard_on_run.py` on the batch folder
3. **If a batch crashes:**
   - `recover_batch.py plan` → recovery manifest
   - notebook 01 scan on the recovery manifest
   - notebook 01 reanalysis of the crashed folder, with `ALLOW_INCOMPLETE_FOLDERS=True`
   - `recover_batch.py merge`
4. **After all 4 batches:** combine them and run the comparison and sensitivity analyses from the proposal (weighted prevalence; overlap ±3 lines; without the 44 previously examined skills; without incomplete folders).

The pilot runs above are tests and are not part of the 1,000-skill dataset.
