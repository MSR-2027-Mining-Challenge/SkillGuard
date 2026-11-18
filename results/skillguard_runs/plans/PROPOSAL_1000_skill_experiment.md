# Proposal: 1,000-skill Cisco Static/Behavioral experiment with a SkillGuard comparison

**Status:** proposal only. No scans have been launched. Every number comes from `plan_1000_dryrun.py` → `dryrun_numbers.json` (read-only: notebook-03 sampling frame, GitSkills sample DB, Nov-3 and fresh-100 timings).

## 1. Research questions

| RQ | Question | Primary measure |
|---|---|---|
| RQ1 | How common are agent-specific capabilities in GitSkills skills? These are nested agent launches, agent-config/memory writes, env-marker removal, scheduling, permission bypass, credential access, and hidden or future-session instructions. | Design-weighted prevalence per capability, with 95% CIs, overall and per stratum |
| RQ2 | Does Cisco Static/Behavioral report these behaviors? | Share of SkillGuard behaviors that have a Cisco security finding within ±3 lines (and in the same file) |
| RQ3 | How much of each skill does each tool actually analyze? | Folder completeness, scan outcomes (complete, partial, failed, skipped), and files by format analyzed vs not analyzed |
| RQ4 | How accurate are both tools when the answer is known? | Precision and recall on a separate controlled ground-truth corpus (section 7) |

A capability is not a vulnerability. Findings from real skills are reported as capabilities and risk signals. Accuracy is measured only on controlled cases, where the ground truth is known by construction.

## 2. Population and sampling

- **Database:** the official GitSkills sample DB (`data/sample/agent_skills_sample.db`, sha256 `683888c9…`), opened read-only. Results describe this sample, not the full 44 GB release.
- **Unit:** one representative `SKILL.md` per distinct content hash (`dedup_primary = 1`), with its folder.
- **Strata:** the ordered rules from notebook 03, unchanged.

  | Stratum | N | Folders complete | Outside the frame |
  |---|---|---|---|
  | scripts | 1,404 | 997 (71%) | listing truncated and script presence unknown: 1,670 |
  | supporting_no_scripts | 2,634 | 2,399 (91%) | program source but no script: 22 |
  | skill_md_only | 7,260 | 7,260 (100%) | no listing: 10 |

  **1,702 of 13,000 representatives (13.1%) fall outside the frame.** This is a stated coverage limit of the study.

### Allocation options (n = 1,000)

| | A. Recommended: disproportionate | B. Proportional | C. Equal |
|---|---|---|---|
| scripts / supporting / md-only | 400 / 300 / 300 | 124 / 233 / 643 | 334 / 333 / 333 |
| Design weights | 3.51 / 8.78 / 24.2 | ≈11.3 each | 4.2 / 7.9 / 21.8 |
| 95% margin of error at p = 5%, scripts stratum | ±1.8 pp | ±3.7 pp | ±2.0 pp |
| 95% margin of error at p = 50%, scripts stratum | ±4.2 pp | ±8.4 pp | ±4.7 pp |
| Expected incomplete folders | 125 + 27 | 39 + 21 | 104 + 30 |

**Recommendation: A.** Agent-specific code behaviors sit almost entirely in the scripts and supporting strata. Over-sampling scripts gives usable precision where the behaviors are, while 300 SKILL.md-only skills still estimate the instruction-level rates. Population estimates use the design weights.

### Seed and overlap with earlier samples

- **Seed:** use notebook 03 with `SEED = 2030` and `STRATUM_SIZES = {scripts: 400, supporting_no_scripts: 300, skill_md_only: 300}`.
- **Why a new seed:** with seed 2027, the first 10 per stratum would reproduce the Nov-3 dev sample exactly.
- **Do not exclude the 220 skills used before** (dev 30, held-out 2028, fresh-100). Excluding them would make the sample a non-probability sample, and notebook 03 has no exclusion option.

  Instead, flag them: about 31 scripts, 8 supporting and 2 SKILL.md-only skills are expected to overlap. Report a sensitivity analysis without them, because SkillGuard was tuned on some of them.

## 3. Cisco scanner settings (unchanged from the Nov-3 baseline)

| Setting | Value |
|---|---|
| Scanner | `skill-scanner 2.3.1` (re-check version and policy fingerprint `3f48e661…` before the run) |
| Command | `skill-scanner scan <folder> --format json --policy balanced` |
| Configurations | SKILL.md only × {default, `--use-behavioral`}; Full folder × {default, `--use-behavioral`} |
| LLM / Meta analyzers | **off** (Static/Behavioral only) |
| Timeout | 300 s per call (notebook 01 `SCAN_TIMEOUT_SECONDS`; the observed maximum is 11 s) |
| Incomplete folders | `ALLOW_INCOMPLETE_FOLDERS = True`. These scans are labeled preliminary (the notebook's existing flag), so every analysis can include or exclude them. |
| Rule classification | Notebook 01's existing `METADATA_QUALITY_RULES` / `SCAN_COVERAGE_RULES` / research categories, unchanged |

## 4. Expected scan count, runtime and storage (plan A)

| Item | Estimate |
|---|---|
| SKILL.md-only scans | 2,000 |
| Full-folder scans | 2,000 (1,696 complete + 304 on incomplete folders, labeled preliminary) |
| **Total Cisco calls** | **4,000** (3,696 if incomplete folders are skipped) |
| Time per call (measured) | 5.08 s mean (Nov-3: 5.43 s over 4 configurations; fresh-100: 4.88 s; max 11 s) |
| **Runtime, sequential** | **≈ 5.6 h** (5.2 h without incomplete folders) |
| SkillGuard V3.1 on the same exported folders | ≈ 17 ms per skill → under 30 s in total |
| Cisco reports | ≈ 4,000 × 4.8 KB ≈ 20 MB |
| Exported skill folders | ≈ 0.3 GB (scripts mean 0.52 MB, supporting 0.16 MB); 644 GB free |
| Machine | 10 cores, 32 GB RAM. Notebook 01 runs sequentially, which is fine at this size. |

**Execution plan:**
1. Split the 1,000-skill manifest into **4 stratified batch manifests of 250** (new files only).
2. Run notebook 01 once per batch (`SELECTION_MODE = "manifest"`, `RUN_MODE = "scan"`), headless under `caffeinate`. Each batch takes about 1.4 h.

   Notebook 01 cannot resume a run, so batches limit what an interruption can lose. A small merge script then combines the four runs' `scan_summary.csv` / `individual_findings.csv`.
3. **Pilot first:** run 12 skills (4 per stratum) through the identical setup. Check scanner version, policy fingerprint, outcomes and timings before starting the full batches.

## 5. Folder coverage reporting (RQ3)

For every skill and configuration, record:
- the notebook outcome (`complete` / `partial` / `failed` / `excluded_incomplete_folder` / `missing`)
- the files missing from the database
- Cisco's scan-coverage rules (for example `SKILL_LOAD_FALLBACK_USED`)

For SkillGuard, record per file whether it was analyzed as code, scanned only by the text heuristic, or not analyzed. In the eligible scripts stratum, only **54% of supporting files** are in formats SkillGuard analyzes (`.md`, `.py`, `.sh`, `.ps1`). The rest are mostly JS/TS, JSON, images and HTML. In the supporting stratum the figure is 78%. This is a stated SkillGuard limitation; Cisco covers JS/TS.

## 6. SkillGuard ↔ Cisco comparison (RQ1–RQ2)

- **Inputs:** identical. SkillGuard runs on the exact `full/` folders that notebook 01 exported, using the frozen V3.1 (`versions/skillguard_capabilities_v3.1_eebc59e7.py`).
- **Units:**
  - SkillGuard: *distinct behaviors* (V3.1 grouping), never raw rows.
  - Cisco: findings deduplicated by (skill, file, line, rule) across the two analyzer modes, keeping security kinds only.
- **Matching:** a SkillGuard behavior is "also reported by Cisco" if any Cisco security finding is within ±3 lines in the same file. Results are also reported at the file level and the skill level.
- **Outputs:**
  - per capability: weighted prevalence and CI, Cisco overlap rate, evidence level (code, generated, documentation, instruction), review priority
  - per Cisco research category: prevalence, plus the SkillGuard overlap in the reverse direction
- **Sensitivity analyses:**
  - without the 220 earlier skills
  - without incomplete folders
  - code-level SkillGuard behaviors only (dropping text-heuristic behaviors)

## 7. Accuracy without human labeling: controlled ground-truth corpus (RQ4)

This is a separate, small benchmark where the label is known by construction:
- **Positives:** one controlled case per capability (7) and carrier (Python, shell, PowerShell, Markdown code fence, Markdown prose, generated string, disguised file) where applicable, about 40 cases. Many already exist as SkillGuard regression-test inputs.
- **Negatives:** one matched benign look-alike for each positive, about 40 cases (negation, read-only use, existence checks, descriptive "silently", option tables, install docs).
- **Injection:** the snippets are injected into copies of benign skills drawn from the sample (seeded), so that skill context is realistic.
- **Runs:** both tools scan every case. Cisco uses the full-folder default and behavioral modes, about 160 calls (~15 min).
- **Metrics:** precision, recall and F1 per tool and per capability or carrier, with Wilson CIs.
- **Bias control:** the corpus is written *before* either tool is run on it and frozen with hashes. This addresses the bias of SkillGuard being tuned on its own tests: half of the cases should be new, in variants not present in the unit tests.

**AI assessments:** any judgment about real-skill findings (for example "this behavior looks legitimate") is labeled provisional AI and kept in separate files. It is never used as ground truth or mixed into the metrics.

## 8. Pre-registered outputs

New run folders only:
- `results/cisco_dataset_runs/agent_skills_sample/runs/<date>_sample1000-seed2030-batch{1..4}/` (notebook 01, unchanged format)
- `results/skillguard_runs/main1000/<run>/` with SkillGuard raw results, behaviors, coverage, comparison and summary JSON
- `results/skillguard_runs/ground_truth/<corpus>/` with the corpus, hashes and tool outputs

Nothing in `skill_security_study/`, earlier runs or Cisco baselines is modified.

## 9. Decisions needed before launch

1. Allocation **A** (400/300/300), or B/C?
2. Seed **2030**, with no exclusions plus flagging and sensitivity analysis? (The alternative is to exclude the 220 earlier skills.)
3. `ALLOW_INCOMPLETE_FOLDERS = True`, labeled preliminary (4,000 calls), or skip them (3,696)?
4. Run the 12-skill pilot, then 4 batches of 250?
5. Build the ground-truth corpus (section 7) before or in parallel with the scans?
