# msr-2027-mining-challenge
Team repository for the MSR 2027 Mining Challenge research project.

## Environment Setup

Create a virtual environment:

```bash
python3 -m venv .venv
```

Activate it:

### macOS / Linux
```bash
source .venv/bin/activate
```

### Windows PowerShell
```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

In VS Code, select `.venv` as the Python interpreter and Jupyter kernel.

## Get the Database

The SQLite sample is not committed (it's ~280 MB). Download `agent_skills_sample.zip` from the GitSkills
dataset release, unzip it, and put the file here:

```
data/sample/agent_skills_sample.db
```

Optional check (should start with `683888c9`):

```bash
shasum -a 256 data/sample/agent_skills_sample.db
```

## Explore the Data

Open `notebooks/00_gitskills_exploration.ipynb` in VS Code, pick the `.venv` kernel, and run the cells top to
bottom. Change the variables at the top of a cell (`keyword`, `skill_index`, `query`, ...) and re-run it.

## Cisco Skill Scanner

`notebooks/01_cisco_scanner_dataset_ready.ipynb` runs the [Cisco AI Defense Skill Scanner](https://github.com/cisco-ai-defense/skill-scanner)
over skills exported from the database. The scanner is pinned in `requirements.txt` (`cisco-ai-skill-scanner==2.3.1`)
so every team member produces comparable findings; `pip install -r requirements.txt` installs it into `.venv`.

Verify the version before scanning (the notebook records it in every run):

```bash
.venv/bin/skill-scanner --version
```

Expected output: `skill-scanner 2.3.1`. Do not upgrade the scanner mid-study; a version change invalidates
finding-level comparisons with earlier runs.

## Where to Look: Researcher Reports

Every saved Cisco run gets a report in `results/reports/<database>/<run ID>/` (combined pilot reports from notebook 02:
`results/reports/<database>/combined/<ID>/`). Open `results/reports/index.html` (or `results/reports/README.md`) to see
all of them; ★ marks the report to open first for each experiment.

| folder | open it for |
|---|---|
| `01_IMPORTANT_RESULTS/` | `START_HERE.md` and `dashboard.html` (self-contained, opens offline in any browser), headline tables |
| `02_DETAILED_ANALYSIS/` | per-skill pages, rule / analyzer breakdowns, full finding tables, figures |
| `03_RAW_SCANNER_OUTPUT/` | index of the raw Cisco reports with SHA-256 (the reports stay in the git-ignored run folder) |
| `04_HUMAN_VALIDATION/` | what has been validated, worksheet snapshots |

Reports keep **scanner alerts**, **provisional** (AI-assisted) labels and **human-validated** findings apart.
Notebook 01 (Section 17) and notebook 02 build their report automatically; `notebooks/05_build_reports.ipynb`
rebuilds any or all of them. From the command line:

```bash
PYTHONPATH=src .venv/bin/python -m gitskills_reports
```

The run folders are only read. Report text is redacted where it looks like a secret and uses repository-relative
paths, and each report is audited for both before it is written, so `results/reports/` is safe to commit.
Validation tests (the 30-skill pilot plus a synthetic hostile skill):

```bash
PYTHONPATH=src .venv/bin/python -m unittest discover -s tests -v
```
