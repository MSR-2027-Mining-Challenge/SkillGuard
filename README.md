# Security of Agent Skills: an MSR 2027 Mining Challenge study

Team repository for our MSR 2027 Mining Challenge project on the **cybersecurity of agent skills**, using the
GitSkills dataset.

## Project overview

**Agent skills** are small packages that teach an AI coding agent (such as Claude Code, Cursor or Codex) how to do a
task. A skill is a `SKILL.md` file with instructions, often bundled with scripts, reference documents and templates.
When an agent uses a skill, it follows those instructions and may run the bundled code on the user's machine.

**GitSkills** is a dataset of agent skills mined from public GitHub repositories. The full dataset has about
3.8 million `SKILL.md` files from 282,200 repositories. Our experiments so far use its **official sample**: 13,000
distinct `SKILL.md` files (29,786 occurrences) from 11,841 repositories. The sample has the same structure as the
full dataset but was not drawn to be representative of it, so our results describe the sample, not all of
GitSkills.

Because a skill can tell an agent to run commands, read files or contact servers, a skill can also be a security
risk. We want to understand:

- what an existing security scanner, the [Cisco AI Defense Skill Scanner](https://github.com/cisco-ai-defense/skill-scanner),
  detects in real skills;
- how much its results depend on context (only `SKILL.md` vs the whole skill folder) and on the analyzers used
  (static rules, behavioral dataflow, LLM, Meta-Analyzer);
- which alerts are misleading, which behaviors go unreported, and what a better skill-security tool would need.

> **Scanner alerts are not confirmed vulnerabilities.** Every alert in this repository is scanner output. Our
> security-review labels are **provisional** (AI-assisted, not yet independently human-validated).

## Research workflow (notebooks)

| notebook | what it does | what it produces |
|---|---|---|
| [00 · GitSkills exploration](notebooks/00_gitskills_exploration.ipynb) | A hands-on playground for browsing the dataset: database overview, viewing skills, keyword search, supporting files, custom SQL. | Interactive exploration only (no saved results). |
| [01 · Cisco scanner experiments](notebooks/01_cisco_scanner_dataset_ready.ipynb) | Exports skills from the database and scans each one with Cisco in four configurations (SKILL.md only vs full folder, static vs static + behavioral). | A run folder with every raw report, a per-scan status, finding tables, comparisons, figures and a results summary. |
| [02 · Cisco pilot comparison](notebooks/02_cisco_pilot_comparison.ipynb) | Combines several finished runs (our three pilots) into one comparison. It does not scan anything. | Combined tables, charts and a written comparison report. |
| [03 · Stratified sampling](notebooks/03_stratified_sample.ipynb) | Draws a reproducible random sample (fixed seed 2027), stratified by what each skill folder contains: scripts, other supporting files, or `SKILL.md` alone. | A sample manifest that notebook 01 can scan ([results/samples/](results/samples/)). |
| [04 · Manual security review](notebooks/04_manual_review_worksheet.ipynb) | Turns the security alerts of one run into a review worksheet that shows the exact code or instructions behind each alert. | A worksheet with blank reviewer columns and suggested interpretations ([results/manual_review/](results/manual_review/)). |
| [05 · Automated research reports](notebooks/05_build_reports.ipynb) | Builds readable reports and offline dashboards for every saved run. It only reads the runs. | [results/reports/](results/reports/) (see below). |
| [06 · Cisco LLM and Meta-Analyzer](notebooks/06_cisco_llm_meta_experiment.ipynb) | Re-runs a finished scan with Cisco's LLM Analyzer and Meta-Analyzer on every skill, reusing the original baseline. It is resumable and budget-guarded. | A new run folder, LLM/Meta comparison tables, a cost estimate, and a report. |

## Research progress

| step | status |
|---|---|
| Dataset exploration and three single-skill scanner pilots | done |
| Systematic 30-skill experiment (static + behavioral, SKILL.md vs full folder) | done: 114 scans executed, 6 excluded by design |
| Provisional review of the 11 distinct security-alert locations | done (provisional labels, 0 human-validated) |
| 30-skill LLM / Meta-Analyzer experiment with a local Qwen3:4B model | done: 171 new scans, no API cost |
| Automated reports and dashboards for all runs | done |
| Security gap analysis of the 30 skills | done (provisional) |

High-level observations so far (details and evidence are in the linked documents):

- **Few alerts, mostly explainable.** Cisco's security alerts came from 4 of the 30 skills. On review, most look like
  intended functionality or scanner artifacts, for example misreading a scoped `allowed-tools` entry.
- **Inconsistent code detection.** The same code was flagged when it appeared in a Markdown example but not when it
  appeared in an executable script.
- **Agent-specific behaviors went unreported** by the deterministic analyzers: editing the user's crontab, starting
  other AI agents with trust-skipping flags, and writing into agent configuration folders.
- **Local LLM analysis was limited.** Qwen3:4B flagged possible prompt injection in 25 of 30 skills, including
  ordinary or even defensive instructions. Cisco's Meta-Analyzer rarely returned usable results with this small
  model. Cisco's default model (Claude) has not been tested.

## Results and reports

**Start here:** open [`results/reports/index.html`](results/reports/index.html) in a web browser after cloning (or
read [`results/reports/README.md`](results/reports/README.md) on GitHub). It lists every report; ★ marks the one to
open first for each experiment. Each report's `dashboard.html` is a single self-contained file that works offline.
It contains coverage charts, severity tables, a searchable alert explorer, per-skill evidence, configuration
comparisons and validation status.

Every report folder has the same four parts:

| folder | what you find there |
|---|---|
| `01_IMPORTANT_RESULTS/` | `START_HERE.md`, the dashboard, and the main summary tables and findings |
| `02_DETAILED_ANALYSIS/` | detailed tables, per-skill evidence pages, figures, and (for the LLM/Meta run) all comparison tables |
| `03_RAW_SCANNER_OUTPUT/` | an index of the original Cisco reports with SHA-256 hashes, plus run metadata |
| `04_HUMAN_VALIDATION/` | the security-review decisions and what has (and has not) been validated |

Other folders under `results/`:

| folder | contents | on GitHub? |
|---|---|---|
| `cisco_dataset_runs/` | raw Cisco runs: exported skill files, every raw JSON report, checkpoints | **no**: local only, git-ignored (it contains untrusted skill content) |
| [`gap_analysis/`](results/gap_analysis/) | security gap-analysis tables: pattern-search hits, classified candidates, research insights | yes |
| [`manual_review/`](results/manual_review/) | manual-review worksheets with provisional labels | yes |
| [`samples/`](results/samples/) | sample manifests and sampling reports from notebook 03 | yes |
| [`reports/`](results/reports/) | generated reports and dashboards (redacted, safe to share) | yes |
| `figures/`, `tables/` | placeholders for exported paper figures and tables (currently empty; each run keeps its own figures and tables) | yes |

Someone who clones the repository gets the reports, samples, worksheets and gap-analysis tables, **but not the raw
scans**. To re-create those, run notebooks 01 and 06 (they need the database and, for 06, an LLM).

## Getting started

### 1. Clone and set up Python

Requires Python 3.11 to 3.14 (needed by the pinned scanner).

macOS / Linux:

```bash
git clone https://github.com/D1Adamm/msr-2027-mining-challenge.git
cd msr-2027-mining-challenge
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Windows (PowerShell):

```powershell
git clone https://github.com/D1Adamm/msr-2027-mining-challenge.git
cd msr-2027-mining-challenge
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

The Cisco scanner is installed as a Python package (`cisco-ai-skill-scanner==2.3.1`). It is pinned so everyone gets
comparable results; do not upgrade it mid-study. With the environment activated, check it on any platform:

```bash
skill-scanner --version
```

The expected output is `skill-scanner 2.3.1`.

### 2. Get the database

The database is not committed. There are two versions:

| version | where to get it | size | used by |
|---|---|---|---|
| **official sample** (what we use) | `agent_skills_sample.zip` in the authors' sample repository, [github.com/giuseppedestefanis/gitskills-sample](https://github.com/giuseppedestefanis/gitskills-sample) | about 277 MB unzipped | all notebooks and results in this repository |
| full dataset | `agent_skills_release.db` on Zenodo, [doi.org/10.5281/zenodo.21875637](https://doi.org/10.5281/zenodo.21875637) (CC BY 4.0) | 44.4 GB | not used yet (future, larger experiments) |

Download `agent_skills_sample.zip`, unzip it, and place `agent_skills_sample.db` at:

```
data/sample/agent_skills_sample.db
```

Optional integrity check. Our results were produced with a file whose SHA-256 starts with `683888c9`:

| platform | command |
|---|---|
| macOS | `shasum -a 256 data/sample/agent_skills_sample.db` |
| Linux | `sha256sum data/sample/agent_skills_sample.db` |
| Windows (PowerShell) | `Get-FileHash -Algorithm SHA256 data\sample\agent_skills_sample.db` |

### 3. Run the notebooks

Open the repository in VS Code (or Jupyter), select the `.venv` interpreter as the kernel, open a notebook, and run
its cells from top to bottom. Each notebook has a **Settings** cell at the top. Notebook 00 is the best place to start
exploring.

- **Notebook 01** runs the Cisco scanner locally.
- **Notebook 06** additionally needs an LLM:
  - **Local (free):** install [Ollama](https://ollama.com), then create the model once with:

    ```bash
    ollama create skillscan-qwen3-4b-ctx64k -f configs/ollama/skillscan-qwen3-4b-ctx64k.Modelfile
    ```

  - **Hosted model:** set `SKILL_SCANNER_LLM_API_KEY` and an approved budget. Never commit keys.

Notebook 06's work can also be run from the command line. The commands below are for macOS / Linux, run from the
repository root with the environment activated. On Windows PowerShell, run `$env:PYTHONPATH = "src"` once and then
the same commands without the `PYTHONPATH=src` prefix.

```bash
PYTHONPATH=src python -m gitskills_cisco_llm prepare --source <notebook-01 scan run> --name <name> --model ollama/skillscan-qwen3-4b-ctx64k
PYTHONPATH=src python -m gitskills_cisco_llm run <run folder>
PYTHONPATH=src python -m gitskills_cisco_llm analyze <run folder>
```

### 4. Open or rebuild the reports

The existing reports need nothing installed: open [`results/reports/index.html`](results/reports/index.html). To
rebuild them from local run folders, use notebook 05 or run (macOS / Linux; on Windows, set `PYTHONPATH` as shown
above):

```bash
PYTHONPATH=src python -m gitskills_reports
```

Run the validation tests with the command below. Tests that need the local run folders are skipped automatically
when the folders are absent.

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
```

## Repository structure

| path | contents |
|---|---|
| [`notebooks/`](notebooks/) | the seven research notebooks (00-06) |
| [`src/gitskills_reports/`](src/gitskills_reports/) | report and dashboard generator (notebook 05) |
| [`src/gitskills_cisco_llm/`](src/gitskills_cisco_llm/) | LLM/Meta experiment runner and analysis (notebook 06), and the gap-analysis pattern search |
| [`docs/`](docs/) | methodology and findings documents |
| [`configs/ollama/`](configs/ollama/) | local model definition for notebook 06 |
| [`tests/`](tests/) | validation tests for the reporting and experiment code |
| `data/` | where the GitSkills database goes (not committed) |
| [`results/`](results/) | samples, worksheets, reports and analysis tables (see above) |

## Research documentation

- [Cisco LLM Analyzer and Meta-Analyzer: how they work](docs/cisco_llm_meta_analyzers.md): behavior of Cisco 2.3.1's
  LLM-based analyzers, verified against the installed code (flags, providers, local models, cost, failure modes).
- [Security gap analysis of the 30-skill sample](docs/cisco_security_gap_analysis.md): what Cisco detected, what it
  may have missed, why some alerts are misleading, candidate tool improvements, and threats to validity.
- [Sampling report](results/samples/agent_skills_sample_seed2027_scripts10_supporting_no_scripts10_skill_md_only10/sampling_report.md):
  how the 30-skill sample was drawn.

## Current direction

These are **proposed research directions**, not completed work:

- **Agent-specific capability detection:** recognizing behaviors that matter for AI agents (scheduled jobs, starting
  other agents, changing agent settings), not only generic malware patterns.
- **Consistent analysis across files:** giving the same verdict to the same behavior whether it appears in
  `SKILL.md`, a reference document or an executable script.
- **Context-aware judgments:** telling suspicious behavior apart from legitimate functionality, with evidence tied to
  exact lines.
- **Larger reproducible experiments:** scaling the same pipeline from 30 to 100, 300 and eventually 1,000+ skills.
