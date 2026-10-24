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
