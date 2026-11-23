# Next 1,000-skill experiment (seed 2031): Cisco vs MalSkills vs SkillGuard

**Status:** prepared and piloted; **the full 1,000-skill scans have not been launched.** See "Pilot" below for the verified infrastructure.

## Design

| Item | Decision |
|---|---|
| Frame | GitSkills sample DB (sha256 `683888c9…`), notebook 03 frame and strata, unchanged |
| Exclusions | 2,174 previously used SKILL.md identities (`file_sha`) from every earlier sample (`exclusions/`): seed 2027 (30), held-out 2028/2029 (190), seed 2030 (1,000), notebook-01 pilots (5), and both MalSkills samples (1,098 of 1,100 resolved). 2 MalSkills entries cannot be mapped and are listed in `exclusions/unresolved.csv` |
| Sample | `results/samples/agent_skills_sample_seed2031_scripts400_supporting_no_scripts300_skill_md_only300/` drawn by `draw_sample.py`, which executes notebook 03's own code in memory with SEED=2031, 400/300/300, and one recorded exclusion line. 2,034 eligible representatives were removed; design weights refer to the reduced frame (`exclusion_provenance.json`). The harness reproduces the committed seed-2030 sample byte-identically (`draw_sample.py --check-seed2030`) |
| Lockbox | 250 skills (100/75/75) set aside for post-freeze evaluation, see [LOCKBOX_POLICY.md](LOCKBOX_POLICY.md) |
| Research corpora | 13 skills from known adversarial / scanner-fixture repositories are flagged (`manifests/research_corpus_flags.csv`), not excluded. Report rates with and without them |
| Identical inputs | Notebook 01 exports each skill once (bytes from the DB). `verify_export.py` checks every exported file against the DB, records missing and truncated listings, and stores a folder digest. Every tool runner re-checks the digest before and after scanning |
| Cisco | skill-scanner 2.3.1, policy balanced: the 4 main1000 configurations via notebook 01, plus "Full folder / behavioral + ATR" (`run_cisco_atr.py`, `--rule-packs atr`) |
| MalSkills | `malskills_runner.py`: byte-copied corpus named by `skill_id`, `scan-corpus --profile static` (no LLM), commit / semgrep / rules digest recorded, results imported with fence lines mapped back to source lines (verified on 295 earlier findings: 294 matched) and SKILL.md identity checked |
| SkillGuard | Frozen V3.1 (`eebc59e7`) and V3.2 (source sha256 recorded) on the same folders (`run_skillguard.py`) |
| Matching | Join key `skill_id` + repo-relative file + line (±3 lines for location agreement). Cisco absolute paths are made relative; MalSkills virtual fence paths are mapped back |
| Batches | 4 stratified batches of 250 (main1000 round-robin design); 12-skill pilot drawn from open skills only |

## How to run (after approval)

```bash
caffeinate -i .venv/bin/python -I results/skillguard_runs/next1000/run_next1000.py pilot --repeat
caffeinate -i .venv/bin/python -I results/skillguard_runs/next1000/run_next1000.py batch1   # then batch2..batch4
```

- **MalSkills:** set `MALSKILLS_BIN=/path/to/MalSkills/.venv/bin/malskills` on a machine that has MalSkills and semgrep.
- **Otherwise:** the orchestrator only prepares `results/malskills_corpus/<run>/` (byte copies plus `SHA256SUMS`, local and untracked). Run MalSkills on that corpus elsewhere and import the results:

```bash
.venv/bin/python -I results/skillguard_runs/next1000/malskills_runner.py run <corpus> <out> --malskills-bin <malskills>
.venv/bin/python -I results/skillguard_runs/next1000/malskills_runner.py import <out> <cisco_run_dir>
```

**Expected cost:** Cisco about 5,000 scans (around 4 h serially, based on main1000); MalSkills about 3 h at 4 workers (based on the earlier run); SkillGuard seconds.

## Outputs

| Folder | Content |
|---|---|
| `exports/<run>/` | `folder_manifests.jsonl` (file hashes, missing files, truncated listings, folder digest), `export_summary.csv` |
| `cisco_atr/<run>/` | `scans.csv`, `findings.csv` (+ `sealed/`), `raw/` (local only) |
| `skillguard/<run>/` | V3.1 / V3.2 behaviors, V3.2 chains and coverage, `per_skill.csv` (+ `sealed/`) |
| `malskills/<output>/` | `scans.csv`, `sso_findings.csv`, `pattern_verdicts.csv` (+ `sealed/`) |
| `run_log.jsonl` | One event per step |
| `provenance/` | Executed notebook copies (local only) |

## Pilot (2026-11-22, 12 open skills, run `2026-11-22_212530_next1000-seed2031-pilot`)

The whole pipeline ran end to end in 7.0 minutes; `run_log.jsonl` has every event.

| Step | Result |
|---|---|
| Notebook 01, 4 core Cisco configurations | 48/48 scans COMPLETE (mean 4.8 s per scan); status gate passed; tracked report index restored |
| Export verification | 12 skills, 64 files, **0 byte mismatches** with the DB; 2 folders with listed-but-missing files recorded |
| Cisco + ATR (5th configuration) | 12/12 COMPLETE. **1,292 findings, 1,276 of them ATR rules, in all 12 skills** (343 CRITICAL). 3 ATR rules produce 75%, and one skill alone has 694 findings. Core full-folder behavioral: 7 security findings in 3 skills |
| SkillGuard V3.1 / V3.2 | V3.1 7 behaviors; V3.2 13 behaviors, 1 chain, all 64 files covered by the coverage report |
| Determinism | SkillGuard (all 4 output tables) and Cisco+ATR (findings, statuses) **identical** on a second run |
| Folder digests | Unchanged before and after every scan |
| MalSkills | Corpus prepared (12 skills, 64 files, byte copies plus `SHA256SUMS`). **Not run:** MalSkills is not installed in this environment. The importer was verified on 40 skills of the earlier MalSkills output: line mapping 294/295, identity checks 0 mismatches |

Implications for the full run:

- **Report the ATR configuration separately and never pool it into the primary Cisco rates.** Its volume suggests a high false-alarm rate on ordinary skills, but that is an observation, not a measured precision.
- **Lockbox:** the pilot used only open skills, and no lockbox output has been produced.
- **Fixed after the pilot:** the ATR summary counted rule IDs with an `ATR-` prefix, but the real IDs are `ATR_2026_*`. The summary was corrected and re-run; the findings were identical.
