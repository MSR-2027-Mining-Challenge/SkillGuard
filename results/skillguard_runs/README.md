# SkillGuard runs and the 1,000-skill experiment

This folder holds every SkillGuard experiment (development, held-out evaluations, frozen versions) and the 1,000-skill Cisco + SkillGuard experiment. Every script is run from the repository root with `.venv/bin/python -I <script>`. Scripts read skill files only as text and never execute skill code.

| Folder | What it is | Open first |
|---|---|---|
| [`main1000/`](#main1000) | **1,000-skill experiment** (seed 2030), Nov 15–16 | [`main1000/REPORT_main1000.md`](main1000/REPORT_main1000.md) |
| [`comparisons/`](comparisons/) | SkillGuard V2 and V3 evaluations against Cisco: dev30, held-out seed 2028, fresh-100 seed 2029 | [`REPORT_v3_2026-11-13.md`](comparisons/REPORT_v3_2026-11-13.md), [`REPORT_v2_2026-11-13.md`](comparisons/REPORT_v2_2026-11-13.md) |
| [`sample30-seed2027/`](sample30-seed2027/) | SkillGuard V1 on the Nov-3 30-skill Cisco sample | [`…skillguard-v1/REPORT.md`](sample30-seed2027/2026-11-13_221401_skillguard-v1/REPORT.md) |
| [`heldout/`](heldout/) | sample manifests and sampling metadata for the held-out sets (seeds 2028 and 2029) | `*/sampling_metadata.json` |
| [`versions/`](versions/) | frozen copies of SkillGuard V1, V2, V3 and **V3.1** and their tests; the file name carries the sha256 prefix | V3.1 = `skillguard_capabilities_v3.1_eebc59e7.py` (identical to `src/skillguard_capabilities.py`) |
| [`plans/`](plans/) | the 1,000-skill proposal and its dry-run numbers, written **before** launch | `PROPOSAL_1000_skill_experiment.md` |

**Top-level scripts:**

- `run_skillguard_compare.py`: V1/V2 comparisons.
- `run_skillguard_eval_v3.py`: V3 fresh-100 evaluation.
- `sample30-seed2027/run_skillguard_sample30.py`: V1 run on the 30-skill sample.

## main1000

| Path | Contents |
|---|---|
| `REPORT_main1000.md` | consolidated report: statistics, SKILL.md-only vs full folder, categories, coverage, sensitivity, limitations |
| `consolidated/2026-11-16_012423_4runs/` | `summary.json`, `tables/*.csv`, `figures/fig1–fig6.png` |
| `SCAN_STATUS_INVESTIGATION.md` | why the run paused after batches 1, 3 and 4, and how the status gate was revised; no scan was repeated |
| `PILOT_REPORT.md`, `pilot_checks/` | 12-skill pilot: run-to-run reproducibility and hard-kill crash recovery |
| `manifests/` | pilot and 4 batch manifests (a stratified round-robin split of the 1,000-skill sample) and the 44 skills that overlap earlier samples |
| `skillguard/<cisco run>/` | frozen SkillGuard V3.1 output per run: `behaviors.csv`, `coverage.csv`, `per_skill.csv`, `summary.json` |
| `main_run_log.jsonl` | timestamped event log of the whole run, including every gate decision |

**How the experiment was run** (in this order):

| Step | Script |
|---|---|
| Sample | notebook 03 with `SEED=2030`, sizes 400/300/300 → `results/samples/agent_skills_sample_seed2030_…/` |
| Batch and pilot manifests | `make_manifests.py` |
| All 4 batches: notebook 01 (via `run_notebook.py`), status gate, SkillGuard, index restore | `run_main1000.py [first_batch]` |
| Execute a notebook headless with in-memory setting overrides (the `.ipynb` on disk is never changed) | `run_notebook.py` |
| Frozen V3.1 on a Cisco run's exported folders (hash-checked) | `run_skillguard_on_run.py <cisco run dir>` |
| Consolidated analysis (writes a new timestamped folder, never overwrites) | `analyze_main1000.py <batch1..4 run dirs>` |
| Reproducibility check between two runs | `compare_runs.py <run a> <run b>` |
| Crash recovery for an interrupted batch | `recover_batch.py plan` / `merge` |

## Tracked vs local

Tracked: reports, scripts, manifests, sampling metadata, and every derived CSV/JSON table.

Kept local (see `.gitignore`):

- exported skill folders and raw Cisco reports of the held-out sets (untrusted content)
- per-skill raw SkillGuard JSON in `raw/`, `raw_v2/` and `raw_v3/` (it contains absolute local paths; all values are in the CSV tables next to it)
- executed-notebook copies in `main1000/provenance/`
- `main_run_stdout.txt`, which duplicates the run log
- the blind-review answer key

The Cisco inputs to the 1,000-skill analysis (`scan_summary.csv`, findings) are in the tracked per-batch reports under `results/reports/agent_skills_sample/*sample1000*/`. The raw run folders themselves are in `results/cisco_dataset_runs/`, which is local only.
