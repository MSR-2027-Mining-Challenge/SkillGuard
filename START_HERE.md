# Start here

This is a map of the repository: what the project is, what has been done, and where each result lives. For setup instructions and the notebook workflow, see [README.md](README.md).

## The research in two sentences

Agent skills (`SKILL.md` plus bundled scripts and documents) tell AI coding agents what to do, so they can carry security risks. Using the GitSkills dataset, we measure what an existing scanner, **Cisco AI Defense skill-scanner 2.3.1**, reports on real skills. Alongside it we build **SkillGuard**, a static inventory of *agent-specific capabilities* that such scanners do not target: starting other agents, editing agent configuration, and instructions to skip approval.

> Scanner alerts are not confirmed vulnerabilities, and a SkillGuard capability is not a vulnerability. No result in this repository has been human-validated. Labels marked *provisional* are AI-assisted.

## Latest: three-scanner experiment on 1,000 new skills (Nov 22–23, 2026; branch `skillguard-v3.2`)

Cisco skill-scanner, MalSkills and SkillGuard (frozen V3.1 and the new V3.2) scanned the **same** 1,000 skills. The sample was a new seed-2031 sample of 400 / 300 / 300 skills that excludes every skill used before. 250 of the skills form an evaluation lockbox.

| What | Where |
|---|---|
| **Mentor/meeting briefing: read this first** | [`results/skillguard_runs/next1000/MENTOR_BRIEF.md`](results/skillguard_runs/next1000/MENTOR_BRIEF.md) |
| Research report (design, execution, results, limitations) | [`REPORT_next1000.md`](results/skillguard_runs/next1000/REPORT_next1000.md) |
| Findings analysis (worked examples per tool, SkillGuard-only skills, V3.1 vs V3.2) | [`ANALYSIS_next1000.md`](results/skillguard_runs/next1000/ANALYSIS_next1000.md) |
| Figures | [`next1000/figures/`](results/skillguard_runs/next1000/figures/) |
| Guide to all data, tables and scripts | [`next1000/README.md`](results/skillguard_runs/next1000/README.md) |
| Lockbox rules and the 2026-11-23 exposure record | [`next1000/LOCKBOX_POLICY.md`](results/skillguard_runs/next1000/LOCKBOX_POLICY.md) |

**Headline numbers** (weighted share of skills, 95% CI):

| Tool | Measure | Weighted share |
|---|---|---|
| Cisco | flags the full folder (198 of 930 comparable skills) | **8.1%** (6.5–9.7) |
| MalSkills | any security-sensitive operation | **30.7%** |
| MalSkills | "malicious" verdict, 5 skills, all installer-style `curl … \| sh` lines in the open cases | **0.37%** |
| SkillGuard V3.2 | any reviewable agent-control behavior | **15.5%** (12.7–18.2) |
| SkillGuard V3.2 | high priority | **0.26%** |

Cisco and MalSkills overlap heavily, while SkillGuard reports a different class of behavior: pre-approval, bypass instructions, external agent launches and agent configuration. No result is human-validated.

## Previous main result: the 1,000-skill experiment (Nov 15–16, 2026)

A stratified random sample of 1,000 skills (seed 2030; 400 with scripts / 300 with supporting files only / 300 `SKILL.md` only). Cisco was run in 4 configurations (4,000 scans), and frozen SkillGuard V3.1 analyzed the same folders.

| What | Where |
|---|---|
| **Report: read this first** | [`results/skillguard_runs/main1000/REPORT_main1000.md`](results/skillguard_runs/main1000/REPORT_main1000.md) |
| The six figures | [`…/consolidated/2026-11-16_012423_4runs/figures/`](results/skillguard_runs/main1000/consolidated/2026-11-16_012423_4runs/figures/) |
| Consolidated tables (weighted rates, categories, rules, coverage, sensitivity) | [`…/consolidated/2026-11-16_012423_4runs/tables/`](results/skillguard_runs/main1000/consolidated/2026-11-16_012423_4runs/tables/) and `summary.json` |
| Cisco vs SkillGuard comparison | report §7; [`tables/skillguard_behaviors_all.csv`](results/skillguard_runs/main1000/consolidated/2026-11-16_012423_4runs/tables/skillguard_behaviors_all.csv) |
| Scan-status limitations (81 skills outside the primary set, and why) | report §1; [`SCAN_STATUS_INVESTIGATION.md`](results/skillguard_runs/main1000/SCAN_STATUS_INVESTIGATION.md); [`tables/scan_status_non_complete.csv`](results/skillguard_runs/main1000/consolidated/2026-11-16_012423_4runs/tables/scan_status_non_complete.csv) |
| Pilot (reproducibility and crash-recovery checks) | [`PILOT_REPORT.md`](results/skillguard_runs/main1000/PILOT_REPORT.md) |
| Per-batch Cisco reports and dashboards | [`results/reports/`](results/reports/README.md) (`…sample1000-seed2030-batch1` … `batch4`) |
| Sample, seed and design weights | [`results/samples/agent_skills_sample_seed2030_…/`](results/samples/agent_skills_sample_seed2030_scripts400_supporting_no_scripts300_skill_md_only300/) |
| Code that ran it | [`results/skillguard_runs/main1000/`](results/skillguard_runs/README.md#main1000) |

**Headline numbers** (estimated share of skills, 95% CI): Cisco flags **9.6%** (8.3–10.9) of skills in a full-folder scan but only **1.7%** in a `SKILL.md`-only scan. 83% of flagged skills are flagged only when bundled files are scanned. SkillGuard finds at least one agent capability in **11.0%** (8.9–13.1) of skills, 75% of them in Markdown instructions rather than code. The two tools rarely point at the same place: only 4 of 244 behaviors have a Cisco finding within 3 lines.

## All completed experiments

| Date | Experiment | Main document | Data and tables |
|---|---|---|---|
| Nov 3 | Three single-skill Cisco pilots | [reports index](results/reports/README.md) (`pilot-*`, `combined/`) | `results/reports/agent_skills_sample/` |
| Nov 3 | **30-skill Cisco experiment** (seed 2027; static + behavioral; `SKILL.md` vs full folder) | [reports index](results/reports/README.md) (`sample30-seed2027-reanalysis` ★) | [sample](results/samples/agent_skills_sample_seed2027_scripts10_supporting_no_scripts10_skill_md_only10/sampling_report.md), [review worksheet](results/manual_review/sample30-seed2027/) |
| Nov 7 | 30-skill Cisco LLM / Meta-Analyzer run (local Qwen3:4B) | [docs/cisco_llm_meta_analyzers.md](docs/cisco_llm_meta_analyzers.md) | report `sample30-seed2027-llm-meta-qwen3-4b` |
| Nov 10 | **30-skill security gap analysis** (what Cisco missed or misread) | [docs/cisco_security_gap_analysis.md](docs/cisco_security_gap_analysis.md) | [results/gap_analysis/sample30-seed2027/](results/gap_analysis/sample30-seed2027/) |
| Nov 13 | SkillGuard V1 on the 30-skill sample | [REPORT.md](results/skillguard_runs/sample30-seed2027/2026-11-13_221401_skillguard-v1/REPORT.md) | same folder |
| Nov 13 | SkillGuard V2: dev set plus held-out set (seed 2028) | [REPORT_v2_2026-11-13.md](results/skillguard_runs/comparisons/REPORT_v2_2026-11-13.md) | `results/skillguard_runs/comparisons/` |
| Nov 13–14 | SkillGuard V3: fresh 100-skill held-out set (seed 2029; provisional AI labels) | [REPORT_v3_2026-11-13.md](results/skillguard_runs/comparisons/REPORT_v3_2026-11-13.md) | `results/skillguard_runs/comparisons/2026-11-13_234328_…` |
| Nov 15 | SkillGuard V3.1 frozen; 1,000-skill plan and pilot | [PROPOSAL](results/skillguard_runs/plans/PROPOSAL_1000_skill_experiment.md) (written before launch), [PILOT_REPORT.md](results/skillguard_runs/main1000/PILOT_REPORT.md) | `results/skillguard_runs/plans/`, `main1000/manifests/` |
| Nov 15–16 | **1,000-skill Cisco + SkillGuard experiment** | [REPORT_main1000.md](results/skillguard_runs/main1000/REPORT_main1000.md) | see above |
| Nov 22 | SkillGuard V3.2 development evaluation (benchmark, regression vs V3.1) | [REPORT_v32.md](results/skillguard_runs/v32_regression/REPORT_v32.md) | `results/skillguard_runs/v32_regression/`, `benchmarks/skillguard_v32/` |
| Nov 22–23 | **Three-scanner experiment on 1,000 new skills** (Cisco, MalSkills, SkillGuard V3.1/V3.2; seed 2031) | [REPORT_next1000.md](results/skillguard_runs/next1000/REPORT_next1000.md), [ANALYSIS_next1000.md](results/skillguard_runs/next1000/ANALYSIS_next1000.md) | `results/skillguard_runs/next1000/` |

## SkillGuard V3.2 (Nov 22, 2026; branch `skillguard-v3.2`)

| What | Where |
|---|---|
| Overview, taxonomy, detections, limitations | [docs/skillguard_v3.2.md](docs/skillguard_v3.2.md) |
| Output schema 5.0 | [docs/skillguard_v3.2_schema.md](docs/skillguard_v3.2_schema.md) |
| Code (frozen V3.1 untouched) | [`src/skillguard/`](src/skillguard/) — `PYTHONPATH=src .venv/bin/python -m skillguard <folder> [--json]` |
| Controlled benchmark (65 synthetic cases) | [benchmarks/skillguard_v32/](benchmarks/skillguard_v32/) |
| V3.1 vs V3.2 report | [results/skillguard_runs/v32_regression/REPORT_v32.md](results/skillguard_runs/v32_regression/REPORT_v32.md) |
| Three-scanner experiment on 1,000 new skills (completed) | [results/skillguard_runs/next1000/README.md](results/skillguard_runs/next1000/README.md) |

## Code

| What | Where |
|---|---|
| **SkillGuard V3.2** (current development version, package sha256 `c15e43c3…`) | [`src/skillguard/`](src/skillguard/) |
| SkillGuard V3.1 (frozen baseline, sha256 `eebc59e7…`) | [`src/skillguard_capabilities.py`](src/skillguard_capabilities.py) |
| SkillGuard tests (55 controlled cases) | [`tests/test_skillguard_capabilities.py`](tests/test_skillguard_capabilities.py) |
| Frozen copies of every SkillGuard version (V1, V2, V3, V3.1) with their tests | [`results/skillguard_runs/versions/`](results/skillguard_runs/versions/) |
| Research notebooks 00–06 (exploration, Cisco scans, sampling, review, reports, LLM/Meta) | [`notebooks/`](notebooks/) (described in the [README](README.md#research-workflow-notebooks)) |
| Report and dashboard generator | [`src/gitskills_reports/`](src/gitskills_reports/) |
| LLM/Meta experiment runner and gap-analysis pattern search | [`src/gitskills_cisco_llm/`](src/gitskills_cisco_llm/) |
| Experiment scripts for SkillGuard runs and the 1,000-skill experiment | [`results/skillguard_runs/`](results/skillguard_runs/README.md) |

Run all tests from the repository root:

```bash
PYTHONPATH=src .venv/bin/python -m unittest discover -s tests
```

## Important vs generated files

- **Read these:** this file, the [README](README.md), the next1000 documents (`MENTOR_BRIEF.md`, `REPORT_next1000.md`, `ANALYSIS_next1000.md`), `REPORT_v32.md`, the earlier reports linked above (`REPORT_main1000.md`, `REPORT_v3`, `REPORT_v2`, the V1 `REPORT.md`), the documents in [`docs/`](docs/), and [`results/reports/README.md`](results/reports/README.md).
- **Generated, kept for traceability:** everything under `results/reports/agent_skills_sample/` (one folder per Cisco run, written by notebooks 01 and 05), `consolidated/…/tables/`, per-run SkillGuard tables (`main1000/skillguard/<run>/`), manifests, and `main_run_log.jsonl`. Do not edit these by hand; regenerate them with the scripts.
- **Superseded but kept:** older reanalyses in the reports index (marked "superseded") and SkillGuard V1–V3, which are frozen in `versions/` for comparison only.

## Not on GitHub (local only)

| What | Why |
|---|---|
| `data/sample/agent_skills_sample.db` | dataset; download it as described in the [README](README.md#2-get-the-database) |
| `results/cisco_dataset_runs/` | raw Cisco runs: exported, **untrusted** skill files and raw JSON reports |
| Held-out skill exports and raw Cisco reports under `results/skillguard_runs/heldout/*/` | untrusted skill content |
| Per-skill raw SkillGuard JSON (`raw/`, `raw_v2/`, `raw_v3/`) and executed-notebook copies (`main1000/provenance/`) | contain absolute local paths; every value is also in the tracked CSV tables, and the run settings are in `run_main1000.py` and the run log |
| The blind-review answer key (`review_key_DO_NOT_OPEN_BEFORE_LABELING.csv`) | kept private so that a later blind review stays possible |
| `.venv/` and `*.zip` archives | local environment and personal working copies |

To re-create the raw data, download the database and re-run notebook 01 with the committed manifests. The run settings are in `results/skillguard_runs/main1000/run_main1000.py`.

## Current status and next steps

- **Done:** the main1000 experiment; SkillGuard V3.2, which adds JS/TS, JSON/YAML/TOML config parsing and cross-file chains; and the three-scanner experiment on 1,000 new skills.
- **Open threads** (see `REPORT_next1000.md` §10 and `MENTOR_BRIEF.md` §9):
  - **Human validation:** a protocol-based review of alerts, then an evaluation of a frozen version on the lockbox.
  - **Instruction detectors:** precision problems with negation and with "mentions vs writes" of agent config.
  - **Chain reporting:** chains need per-skill deduplication.
  - **Lockbox exposure:** item-level lockbox outputs were publicly accessible for about 18 hours on 2026-11-23. They were removed from the branch history the same day (rewrite of `skillguard-v3.2`). The lockbox was exposed, so never claim it was not; see `LOCKBOX_POLICY.md`. Teammates who fetched the branch before the rewrite should reset to `origin/skillguard-v3.2`.
- **Paper:** MSR 2027 Mining Challenge (abstract due 18 Dec 2026, paper 23 Dec 2026).
