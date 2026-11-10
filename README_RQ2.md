# SkillGuard — RQ2 Replication & Automation

**MSR 2027 Mining Challenge · GitSkills · RQ2**

> **RQ2:** What problems exist in agent skills, what effects might they have, and how can we address them?
>
> This package automates **repeatable screening, evidence gathering, report generation, and safe repair probes**. Researcher judgments remain explicit and separate from machine suggestions; the script never calls a warning a confirmed defect without a saved human assessment.

## Start here

From your existing `SkillGuard/` clone, install this package **without replacing your main README**. It includes the updated RQ2 notebook, existing taxonomy, your `rq2_edit.py`, the automation driver, and tests. Your existing candidate CSV and exported Cisco run remain in place.

```bash
# Within SkillGuard (use your existing .venv)
python -m pip install -r requirements-rq2.txt

# A. Generate reports from your current CSV, preserving all your saved annotations.
python scripts/rq2_pipeline.py

# B. To rerun the detector notebook AND generate reports (backs up CSV first):
python scripts/rq2_pipeline.py --execute-notebook

# C. Open the dashboard locally (no server required):
open results/rq2/reports/index.html
```

The report generator works without notebook dependencies when the candidate CSV already exists. For a clean rerun, `--execute-notebook` uses **`notebooks/06_rq2_defect_detection_automated.ipynb`**, a preserved copy of your updated RQ2 notebook. It does not rerun Cisco or download GitSkills; the **saved Cisco export must already exist**.

You can override any path, for example:

```bash
python scripts/rq2_pipeline.py \
  --source-run results/cisco_dataset_runs/agent_skills_sample/runs/YOUR_RUN \
  --csv results/rq2/seed2027_defect_screening/rq2_defect_candidates.csv \
  --execute-notebook
```

## Research workflow

| Stage | What runs automatically | What still requires research judgment |
|---|---|---|
| **1 — Taxonomy** | Loads your published versioned `rq2_defect_taxonomy_v0_1.json` (40 defined rules) | Decide whether the taxonomy needs revision |
| **2 — Screening** | Executes your original rule-based notebook on exported full skill folders; emits stable candidate IDs, coverage, summaries, metadata, `.tex` macros | Interpret incomplete exports and heuristic thresholds |
| **3 — Triage** | Inspects source context, marks comment/documentation vs executable code, suggests where to investigate, drafts evidence sheets | Confirm defects, false positives, and actual impact |
| **4 — Fix experiments** | Runs a *safe, isolated, no-crontab* P5 date/year demonstration | Implement real patches in isolated copies and run appropriate integration tests |
| **5 — Reports** | Produces an offline HTML dashboard, review queues, summary tables, source checksums, and human-annotation snapshots | Researcher validation of potential defects |

**Not automated:** External GitHub history verification, actual skill execution, researcher judgments, effects on real agent behavior, and production-safe repairs. These are substantial scientific evaluation steps, not safe to infer from regex matches.

## Results and reports

**Start here:** open `results/rq2/reports/index.html` in a web browser after running (or read `results/rq2/reports/README.md` on GitHub). The dashboard is a **single self-contained HTML file** that works offline; it includes summary metrics, search, rule and status filters, and preliminary triage evidence. The existing candidate statuses are shown separately from machine suggestions.

Every RQ2 report folder has the same four parts:

| Folder | What you find there |
|---|---|
| `01_IMPORTANT_RESULTS/` | `START_HERE.md`, `dashboard.html`, rule-summary CSV, regenerated LaTeX macros |
| `02_DETAILED_ANALYSIS/` | Searchable review queue, automated triage hints, and redacted per-candidate evidence pages |
| `03_RAW_SCANNER_OUTPUT/` | Manifest/hash index, input checksums, run metadata, and the path to the original local scanner export |
| `04_HUMAN_VALIDATION/` | Existing preliminary assessments, unreviewed queue, status totals, and annotations lost from candidate-ID churn |

Other folders under `results/rq2/`:

| Folder | Contents | Commit/share guidance |
|---|---|---|
| `seed2027_defect_screening/` | Notebook outputs: candidates CSV, inventory, coverage, rule summary, original `.tex` macros | Review before publishing; the candidate CSV may contain notes |
| `reports/` | Regenerated summarized dashboard, tables, and redacted evidence | Inspect researcher-entered text before publishing |
| `backups/` | Timestamped **pre-rerun** copies of the candidate CSV | **Do not commit**; contains researcher notes |
| `fix_experiments/` | Safe P5 probe and future isolated repair experiments | Do not mistake demonstrations for validated live fixes |
| `../cisco_dataset_runs/` | Existing exported skill folders, raw reports, and manifests | Keep local / git-ignored: can contain untrusted skill content |

No repository-root `README.md`, RQ1 results, or existing notebook is overwritten. The included notebook uses a **new filename** so you can compare it with your original. `rq2_edit.py` is the same editing utility you have been using.

## Existing code and files used

| Path | Purpose |
|---|---|
| `notebooks/06_rq2_defect_detection_automated.ipynb` | Your updated 06 detector notebook; executed headlessly when requested |
| `docs/rq2/rq2_defect_taxonomy_v0_1.json` | Machine-readable taxonomy: S (spec preflight), R (research-derived), P (project-specific) |
| `docs/rq2/rq2_defect_taxonomy_v0_1.md` | Human-readable codebook |
| `scripts/rq2_edit.py` | Existing command-line researcher assessment editor (uses only the four researcher assessment fields) |
| `scripts/rq2_pipeline.py` | New notebook runner, evidence triage, and report/dashboard generator |
| `scripts/rq2_p5_probe.py` | New safe, non-destructive P5 demonstration |
| `tests/test_rq2_pipeline.py` | New fixtures and automated regression tests |

## Run the P5 fix investigation safely

```bash
python scripts/rq2_p5_probe.py
cat results/rq2/fix_experiments/P5_set_reminder/TEST_PLAN.md
```

It demonstrates that `2027-01-01 09:00` and `2028-01-01 09:00` produce the same five-field cron expression, then evaluates a proposed year-aware guard for early/on-time/late runs. It **only parses source code** and tests a separate pure-Python model. It does **not** change a crontab, execute the skill, or claim to be a validated patch.

## Human assessment (do not skip)

```bash
# View the next unreviewed items
open results/rq2/reports/04_HUMAN_VALIDATION/unreviewed_candidates.csv

# Enter a preliminary classification (your existing editor)
python scripts/rq2_edit.py --ids YOUR_CANDIDATE_ID

# Update reports after editing the CSV
python scripts/rq2_pipeline.py
```

The reporting pipeline never overwrites `candidate_status`, `investigation_notes`, `impact`, or `recommended_fix`. To prevent loss of work when regenerating the CSV, it backs up the original first, and produces `orphaned_previous_annotations.csv` when a previously labeled candidate no longer has the same stable ID. **Do not count candidate locations as distinct defects.** Several P1 and R6.4 warnings correspond to the same underlying issue.

## Remove old review columns (optional, backup-first)

If an earlier CSV contains columns from an unused multi-person review workflow, simplify it to the four RQ2 researcher fields **without touching existing investigation notes**:

```bash
python scripts/rq2_edit.py --clean-legacy-columns
```

Confirm the prompt to create a `.bak` copy and remove those old columns. The new detector notebook also writes only the four researcher fields on regeneration.

## Tables and paper macros

The notebook already exports `rq2_auto_macros.tex`. The report generator also creates a concise, regenerated version at:

`results/rq2/reports/01_IMPORTANT_RESULTS/rq2_auto_macros.tex`

Copy the generated file into Overleaf, then use:

```latex
\input{rq2_auto_macros.tex}
We screened \rqTwoSkillsFlagged{} skills with candidate findings, producing
\rqTwoCandidateLocations{} candidate locations across
\rqTwoRulesTriggered{} triggered rules.
```

**Important:** `\rqTwoSkillsFlagged` counts skills **with candidate findings**, not all skills screened. For all screened skills, use the notebook's original `\rqTwoSkillsScreened` macro. Recompile Overleaf after replacing the `.tex` file.

## Reproducibility, safety, and limitations

- **Input:** `data/sample/agent_skills_sample.db` was previously sampled and exported by the Cisco notebook; this package starts from that **existing saved run** (by default `sam-sample30-seed2027`). It does not claim the sample is representative of the entire GitSkills population.
- **Traceability:** Keep the sample run name, original `manifest.json` files, and SHA-256 checksums in `03_RAW_SCANNER_OUTPUT/` so colleagues can tie reports to a specific snapshot.
- **Screening ≠ ground truth:** Some rules are manual-only, some are heuristics, and some are specification checks. The report shows those distinctions and keeps original notebook outputs available.
- **Safe by default:** Read-only reporting; no external network calls; no execution of sampled skill scripts; no `crontab` changes; no process termination; no automatic fixes on the original samples.
- **Data sensitivity:** Evidence is regex-redacted, but redaction is not guaranteed to catch every secret. Inspect files before publishing. Source exports may be untrusted and should remain git-ignored.
- **No fabricated evaluation:** The P5 probe is not a full integration test; proposed fixes still require controlled before/after evaluation and regression testing.

## Tests

```bash
python -m unittest discover -s tests -p 'test_rq2_pipeline.py' -v
```

The tests generate their own tiny synthetic repository and do not need the 277 MB SQLite sample or the real Cisco run.

## Research contribution and connection to RQ1/RQ3

**RQ1** asks whether analysis of the full skill folder reveals findings missed by `SKILL.md`-only analysis. **RQ2** uses full-folder evidence to study *what kinds of defects exist, which warnings are genuine, and what repairs might address them*. **RQ3** can turn the validated rules and repairs into a reusable linter/fixer.

The goal of this package is a repeatable empirical process—not inflated defect counts: candidate detection, transparent evidence, explicit human validation, and measurable repair experiments.
