# Next 1,000 skills (seed 2031): Cisco vs MalSkills vs SkillGuard

**Run:** 2026-11-22 22:35 to 2026-11-23 04:00, plus one MalSkills re-run of batch 1 (see Blockers). Four stratified batches of 250 skills. Analysis folder: [`analysis/2026-11-23_040133/`](analysis/2026-11-23_040133/). Every step is in [`run_log.jsonl`](run_log.jsonl). Design and setup are in [README.md](README.md).

**How to read this report:**
- **Unit of analysis:** one skill, meaning one representative SKILL.md and its exported folder, unless a table says otherwise.
- **Alerts:** an alert is a tool output, not a confirmed vulnerability. None of the numbers below measures accuracy, precision or recall; no ground-truth labels exist for these skills.
- **Agreement:** agreement between tools only describes overlap.
- **Weighted rates:** these estimate the share of the 9,264-skill reduced GitSkills frame (11,298 representatives minus the 2,034 excluded as previously used). They use stratified weights with a finite-population correction and normal 95% CIs, as in main1000. Per-stratum Wilson intervals are in `prevalence.csv`.

## 1. Execution: completed and incomplete scans

| Tool | Scans | Complete / ok | Incomplete | Notes |
|---|---|---|---|---|
| Cisco skill-scanner 2.3.1, 4 core configurations | 4,000 | 3,753 COMPLETE | 236 PARTIAL, 11 CONTRACT_ONLY | 930 of 1,000 skills have all 4 configurations COMPLETE; 70 skills have at least one incomplete configuration |
| Cisco, full folder + behavioral + ATR pack | 1,000 | 941 COMPLETE | 59 PARTIAL | — |
| MalSkills `46d60f09`, static profile | 1,000 | 1,000 ok | 0 | 0 SKILL.md identity mismatches, 0 nested skill-file selections (after the fix), corpus unchanged in every batch |
| SkillGuard V3.1 (frozen `eebc59e7`) and V3.2 (`c15e43c3…`) | 1,000 each | 1,000 | 0 | V3.2 coverage report lists every file; see section 6 |

**Incomplete Cisco scans:**
- **Causes:** these come from the same causes as in main1000.
  - Folders whose DB listing has files without stored text: 122 skills.
  - Truncated listings: 27 skills.
  - Frontmatter that Cisco cannot load fully: 59 skills.
- **Policy:** incomplete folders were allowed and flagged, as in main1000. Cisco rates use only skills whose scan is usable for that configuration, and the denominators are given.
- **Item-level list:** open skills are in `incomplete_scans.csv` (46 skills). The 24 lockbox skills are in `sealed/` (by stratum: scripts 14, supporting 3, SKILL.md only 7).
- **Other tools:** MalSkills and SkillGuard scanned every skill, including the incomplete ones.

**Identical inputs:**
- Notebook 01 exported each skill once, and `verify_export.py` found **0 byte mismatches** against the DB.
- Every runner checked the folder digest before and after scanning.
- MalSkills scanned a byte copy that was verified against `SHA256SUMS` after each run.

**Wall time:**
- Batches took 92.5, 87.5, 72.9 and 72.5 minutes.
- Within each batch: Cisco core 41–61 min, Cisco + ATR about 14 min, MalSkills about 17 min (4 workers), SkillGuard about 7 s.

## 2. Blockers and how they were resolved

1. **MalSkills on macOS dropped all findings in Markdown code fences.**
   - Cause: the temp folder is a symlink, which breaks result-path mapping.
   - Fix: the runner sets `TMPDIR` to a folder without symlinks. MalSkills' code is unchanged.
   - Validated before the run: Rio's earlier run is reproduced on 40 skills, 40/40 identical (18/40 before the fix). Details are in the README.
2. **MalSkills scanned 3 batch-1 skills from the wrong SKILL.md** (found during the run).
   - Cause: MalSkills picks its skill file among all `SKILL.md` files in a folder by (exact name, newest mtime, …) and scans only that file's directory. In 3 of 250 batch-1 folders that contain nested `SKILL.md` files, it picked a nested one and scanned a subfolder. The importer's identity check caught this (3 mismatches).
   - Fix: the runner now gives every file one fixed mtime and the top-level SKILL.md one second more, so MalSkills selects it and scans the whole folder. Only timestamps change; file bytes are untouched. This is applied at both prepare and run time. The import now **fails** if any scan used a nested skill file or does not match the SKILL.md identity.
   - Batch 1 was re-run. The first output is kept as `malskills/…batch1__malskills_output__run1_nested_selection/`.
   - Differences between the two runs:
     - Of the 3 skills scanned from a subfolder, 2 changed: SSO count 0→23 and 0→26, verdict benign in both runs. The third gave the same result.
     - The other 247 are identical.
   - Batches 2–4 ran with the fix and show 0 nested selections and 0 identity mismatches.
   - The 12-skill pilot had no nested SKILL.md files, so its validation is unaffected.
3. **No unresolved blockers.** Every tool produced a usable result for every skill, except the incomplete Cisco scans listed above.

## 3. Prevalence by tool (all usable skills)

| Measure (skill flagged if…) | Usable n | Flagged | Scripts | Supporting | SKILL.md only | Weighted (95% CI) |
|---|---|---|---|---|---|---|
| Cisco core, full folder behavioral: any security finding | 930 | 198 | 47.3% | 5.6% | 3.6% | **8.07% (6.48–9.67)** |
| Cisco core, SKILL.md only default | 930 | 19 | 2.8% | 1.1% | 2.1% | 1.95% (0.79–3.11) |
| Cisco + ATR: any ATR rule | 941 | 899 | 98.4% | 94.4% | 92.9% | 93.73% (91.64–95.82) |
| MalSkills: verdict malicious | 1,000 | 5 | 0.8% | 0.3% | 0.3% | 0.37% (0.00–0.83) |
| MalSkills: any security-sensitive operation (SSO) | 1,000 | 491 | 81.3% | 32.0% | 23.3% | 30.65% (27.25–34.04) |
| SkillGuard V3.1: any behavior | 1,000 | 157 | 18.8% | 17.0% | 10.3% | 12.60% (10.12–15.08) |
| **SkillGuard V3.2: any reviewable behavior** | 1,000 | 185 | 21.8% | 19.3% | 13.3% | **15.45% (12.71–18.20)** |
| SkillGuard V3.2: high review priority | 1,000 | 9 | 2.0% | 0.3% | 0.0% | 0.26% (0.10–0.42) |
| SkillGuard V3.2: agent-specific category (T2/T3, agent credentials/endpoints) | 1,000 | 140 | 18.3% | 14.7% | 7.7% | 10.21% (8.02–12.40) |

**Robustness:**
- Excluding the 13 research-corpus skills changes no weighted rate by more than 0.2 points.
- Restricting to folders with complete exports lowers Cisco core to 7.47% and V3.2 reviewable to 14.62% (`prevalence.csv`).
- Cisco core full-folder behavioral (8.07%) is close to main1000 on a disjoint sample (9.63%, 8.34–10.92).

**The measures are not comparable.** Each tool flags a different thing:
- MalSkills' "any SSO" counts operations such as file writes or network calls, not suspicious behavior.
- Its malicious verdict is a formal-pattern decision.
- SkillGuard "reviewable" excludes supporting capabilities such as plain network fetches.
- Cisco core counts any non-metadata security finding.

**ATR (reported separately, never pooled):**
- ATR rules fire in 899 of 941 skills (39,352 findings).
- One rule, `ATR_2026_00099`, produces 21,384 of them, and the top three produce 77%.
- This volume on ordinary skills suggests the pack is unsuitable as a prevalence measure without filtering. That is an observation, not a measured false-positive rate.

## 4. Overlap between the three tools

Restricted to the 930 skills usable by all three tools: Cisco core full-folder behavioral, MalSkills any SSO, and SkillGuard V3.2 reviewable.

| Cisco | MalSkills SSO | SG V3.2 | Skills |
|---|---|---|---|
| – | – | – | 407 |
| – | – | ✓ | 53 |
| – | ✓ | – | 209 |
| – | ✓ | ✓ | 63 |
| ✓ | – | – | 12 |
| ✓ | – | ✓ | 3 |
| ✓ | ✓ | – | 129 |
| ✓ | ✓ | ✓ | 54 |

**What the overlap shows:**
- **Cisco and MalSkills overlap heavily:** 183 of 198 Cisco-flagged skills also have a MalSkills SSO. Both mostly respond to code operations in scripts.
- **SkillGuard V3.2 flags 53 skills that neither other tool flags.** These are mostly agent-environment behaviors such as config modification, tool pre-approval and approval-bypass instructions, which the other tools do not target (section 5).
- **Strictest outputs:** MalSkills malicious (5 skills) and SG V3.2 high priority (9 skills) do not overlap.
  - All 4 MalSkills-malicious skills usable by Cisco are Cisco-flagged.
  - 5 of the 8 SG-high skills usable by Cisco are Cisco-flagged.
  - Among open skills, 3 of the 4 MalSkills-malicious skills are SG V3.2 reviewable (each with `remote_fetch_execute`). The MalSkills patterns are `Malware_Delivery` + `Remote_Code_Execution` in all four. None of these skills has been manually reviewed, so none is a confirmed malicious skill.

## 5. Categories and locations

**Category crosswalk.** Values are skills with at least one alert in the category, across all 1,000 skills. Cisco and MalSkills categories are mapped to the SkillGuard taxonomy by `analyze_next1000.py`; the mapping is approximate.

| SkillGuard category | Cisco core | MalSkills SSO | SG V3.2 |
|---|---|---|---|
| T1 Instruction manipulation | 13 | 0 | 0 |
| T2 Autonomy and oversight control | 87 | 0 | 99 |
| T3 Agent-environment persistence and config tampering | 0 | 61 | 88 |
| T4 Credential and secret access | 14 | 206 | 7 |
| T5 Data egress | 84 | 158 | 0* |
| T6 Code execution and destructive operations | 63 | 204 | 6 |
| T7 Supply chain and provenance | 32 | 123 | 2 |
| T9 Evasion artifacts | 33 | 35 | 0 |
| MalSkills `file_operation` (no T mapping) | – | 288 | – |

\* In SkillGuard, network send/fetch are supporting capabilities and are excluded from the reviewable counts by design.

The tools emphasize different things:
- **SkillGuard:** agent-control and agent-environment categories (T2/T3).
- **MalSkills:** generic code operations (T4–T7).
- **Cisco:** both, with fewer T3 alerts.

**Location agreement.** This covers open skills only: the 246 reviewable V3.2 behaviors, where another tool counts as agreeing if it has an alert within ±3 lines in the same file.
- Cisco core: 5 (2%).
- MalSkills: 32 (13%).
- Cisco + ATR: 97 (39%). ATR's volume makes chance co-location likely.
- Cisco core vs MalSkills: 312 of 713 Cisco core alert locations (44%) have a MalSkills SSO nearby.

| V3.2 capability | Behaviors | Cisco core near | ATR near | MalSkills near |
|---|---|---|---|---|
| agent_config_modification | 82 | 2 | 34 | 11 |
| tool_preapproval | 50 | 0 | 6 | 0 |
| approval_bypass_instruction | 36 | 0 | 18 | 0 |
| external_agent_launch | 28 | 0 | 13 | 3 |
| scheduler_invocation | 14 | 1 | 8 | 9 |
| mcp_server_definition | 13 | 0 | 4 | 0 |
| remote_fetch_execute | 6 | 2 | 3 | 5 |
| other (7 capabilities) | 17 | 0 | 11 | 4 |

## 6. SkillGuard V3.1 vs V3.2 on the new sample

| | V3.2 reviewable: no | V3.2 reviewable: yes |
|---|---|---|
| **V3.1 any: no** | 785 | 58 |
| **V3.1 any: yes** | 30 | 127 |

**Changes:**
- **Overall:** V3.2 flags 185 skills, against 157 for V3.1.
- **Newly flagged by V3.2 (58 skills):** in the 42 open skills among them, the main source is `tool_preapproval` (32 skills; `allowed-tools` grants such as broad shell access). The rest are scattered single cases: endpoint override, scheduler, MCP server definition, config modification, persistence, credential access, embedded secret, unpinned package, remote fetch-execute.
- **No longer flagged (30 skills):** all 21 open skills among them were flagged by V3.1 only for `nested_agent_invocation`. V3.2 classifies these as `in_host_delegation` (the agent delegating to its own sub-agents), a context signal with no review priority, kept separate from `external_agent_launch` by design.
- **Reviewable behaviors by capability, all 1,000 skills:** agent config modification 90, tool pre-approval 53, approval-bypass instruction 36, external agent launch 31, scheduler 17, MCP server definition 15, remote fetch-execute 7, others 22.
- **Chains:** 50. bypass + external agent 30, instruction runs sensitive script 12, pre-approved shell runs sensitive script 4, nesting guard removed for agent launch 3, scheduled agent run 1.

**Coverage**, open-skill files: 2,249 parsed as code or config; 1,366 Markdown instructions only; 317 parsed config without agent settings; 208 unsupported format; 81 data files not analyzed; 6 parse errors.

## 7. Caveats

- **No accuracy claims.** These numbers are alert prevalence and overlap. Measuring precision needs manual review against a labeling protocol, ideally on the lockbox after the freeze.
- **The lockbox is untouched at item level.** All 250 lockbox skills were scanned by every tool. Their item-level outputs are only in `sealed/` folders with `SHA256SUMS`, and nobody opened them. Notebook 01's per-skill Cisco reports for all 1,000 skills stay in local, untracked run folders. This report uses only aggregates over all 1,000 and item-level details for open skills.
- **Tool configuration limits.**
  - MalSkills ran without its LLM stage and without YASA, the same as Rio's earlier run. Its verdicts may differ under the full profile.
  - Cisco ran without LLM, OSV or meta analyzers, as in main1000.
- **The frame is the GitSkills sample DB** after excluding previously used skills. It is not every skill on GitHub.

## 8. Reproducing

```bash
MALSKILLS_BIN=~/MalSkills/.venv/bin/malskills caffeinate -i .venv/bin/python -I results/skillguard_runs/next1000/run_next1000.py batch1   # ... batch4
PYTHONPATH=src .venv/bin/python -I results/skillguard_runs/next1000/analyze_next1000.py <the 4 batch run dirs>
```

Run folders: `2026-11-22_223501_…batch1`, `2026-11-23_000733_…batch2`, `2026-11-23_013501_…batch3`, `2026-11-23_024754_…batch4`.
