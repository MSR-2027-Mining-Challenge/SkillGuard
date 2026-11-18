# SkillGuard V1 on the Nov-3 Cisco 30-skill baseline

Run `2026-11-13_221401_skillguard-v1`. Input: `results/cisco_dataset_runs/agent_skills_sample/runs/2026-11-03_173516_sample30-seed2027/<skill>/full` (30 skills).
This is not the 13k-skill `skill_security_study/` analysis.

A capability finding is an inventory item, not a vulnerability. Every finding below is `assessment: needs_context`.

## Reproducibility

| Item | Value |
|---|---|
| Command | `.venv/bin/python -I results/skillguard_runs/sample30-seed2027/run_skillguard_sample30.py` |
| SkillGuard source sha256 | `a9e04f89…3203` (uncommitted working tree on top of `383590f`) |
| Tests sha256 | `9ffa4d53…0f76` (21/21 passing) |
| Python | 3.14.10. System Python 3.9 adds 1 parse error in skill-creator `scripts/models.py`, which uses `match`. |
| Input hashes | `input_file_hashes.csv` (102 files) |
| Determinism | A second run produced byte-identical CSVs and raw JSON. That duplicate run was deleted. |
| Skill code executed | No. Content is read and parsed with `ast`/`shlex` only. |

Files: `findings.csv` (automatic), `manual_review.csv` (reviewer verdicts), `missed_behaviors.csv`, `coverage.csv`, `per_skill_summary.csv`, `gap_candidate_recall.csv`, `parse_error_dedent_sensitivity.csv`, `raw/<skill>.json`, `run_metadata.json`.

## Headline numbers

| | Count |
|---|---|
| Skills scanned | 30 |
| Skills with ≥1 finding | 2 (set-reminder, skill-creator) |
| Findings (rows) | 21 |
| Distinct behaviors after manual grouping | 4 (B1–B4 below) |
| Findings judged false positive (capability absent) | 0 |
| Findings that duplicate another finding's behavior | 6 doc examples + 3 cleanup rows + 4 extra CLI rows at shared sinks |
| Files present in snapshot | 102 |
| ... fully analyzed | 35 |
| ... analyzed, some non-code fences skipped | 17 |
| ... partially analyzed (some Python blocks failed to parse) | 3 |
| ... Markdown with no supported code (prose / JSON fences only) | 36 |
| ... data files (JSON/YAML) | 7 |
| ... unsupported code format (HTML ×3, JS ×1) | 4 |
| Python blocks that failed to parse | 8 (in 3 files) |
| Files missing from the GitSkills snapshot | 179 across 3 skills (176 in skill-24eda454b855) |

The run reports 234 coverage-limitation rows. 179 of them are snapshot-missing files, so treat the number as a scope warning, not as a SkillGuard failure count.

## Findings by capability

| Capability | Rows | Skill | File:line |
|---|---|---|---|
| scheduler_invocation | 2 | set-reminder | `scripts/set_reminder.py:130` (`crontab -l`), `:133` (`crontab -`) |
| agent_config_modification | 5 | skill-creator | `scripts/run_eval.py:144` mkdir, `:157` write SKILL.md, `:209`/`:212`/`:218` delete (cleanup) |
| agent_env_marker_removal | 2 | skill-creator | `scripts/run_eval.py:182`, `scripts/run_loop.py:186` (drop CLAUDECODE, OPENCODE, OPENCODE_PID, CURSOR_API_KEY) |
| nested_agent_invocation | 12 | skill-creator | `scripts/run_eval.py:188` ×3 (claude, **agent `--trust`**, opencode), `scripts/run_loop.py:192` ×3 (agent, claude, opencode), `SKILL.md:403,406,413,416,423,426` (bash-fence examples) |

By carrier: 15 in executable scripts, 6 in Markdown shell examples, 0 in Markdown Python examples.

### Distinct behaviors (manual grouping)

| ID | Behavior | Rows | Gap ID |
|---|---|---|---|
| B1 | Bundled script rewrites the user's crontab to schedule a generated reminder script | 2 | G01 |
| B2 | Temporary SKILL.md written into `~/.cursor/skills`, `~/.claude/skills` or `<project>/.claude/commands`, then removed | 5 | G05 |
| B3 | Nested non-interactive agent CLI launch (`agent -p … --trust`, `claude -p`, `opencode run`) | 12 | G06 |
| B4 | Agent nesting markers removed from the environment; the rest of the environment (including other API keys) passed to the child | 2 | G07 |

## Comparison with Cisco Static/Behavioral (same Nov-3 run)

Only Cisco findings with `finding_kind = security` count. MANIFEST_* metadata notes are excluded.

| Relation | Rows | Meaning |
|---|---|---|
| Cisco flagged the same location (±3 lines, any of 4 configs) | **0** | No duplicates of a Cisco detection |
| Cisco flagged other lines in the same file | 2 | set_reminder.py: Cisco has DATA_EXFIL_NETWORK_REQUESTS at 38/41 (the Telegram POST inside the template), unrelated to crontab |
| Cisco scanned the file and reported no security finding | 19 | skill-creator run_eval.py, run_loop.py, SKILL.md |
| Cisco did not scan the file | 0 | |

- **Relative to Cisco Static/Behavioral, all 4 behaviors are new.** Neither the default nor the behavioral configuration produced any security finding at these locations.
- **Relative to our own manual gap analysis, nothing is new.** B1–B4 are G01, G05, G06 and G07, and the SKILL.md examples were already pattern hits.
- **This is not an independent test.** The V1 detectors for B2–B4 were built and tuned on skill-creator, so their recall here is closer to training-set accuracy than to generalization. Only the crontab detection (B1) predates that tuning.
- **Cisco detections SkillGuard does not reproduce** in these 2 skills: COMMAND_INJECTION_OS_SYSTEM at `generate_review.py:390` (G08; the gap analysis judged the mechanism wrong), FILE_MAGIC_MISMATCH on `scripts/__init__.py`, ALLOWED_TOOLS_* on SKILL.md, and DATA_EXFIL at 38/41. These fall outside V1's families. The two tools are complementary; V1 does not replace Cisco.
- **Misleading-finding check.** The 6 SKILL.md rows are true but non-executable documentation of B3. Counting them as separate detections would inflate B3 from 2 code locations to 8 rows.

## Recall against gap-analysis candidates in V1's families

| Candidate | Location | Detected |
|---|---|---|
| G01 | set_reminder.py 128–133 | yes (130, 133) |
| G01 | set_reminder.py 47–51 (inside the generated-script template string) | **no** |
| G05 | run_eval.py 126–158 / 205–218 | yes / yes |
| G06 | run_eval.py 170–191 / run_loop.py 175–198 | yes / yes |
| G07 | run_eval.py 182–186 / run_loop.py 186–190 | yes / yes |
| G11 | youtube-content SKILL.md 128, 357, 395 (agent `cronjob(...)` tool) | **no** (all 3) |

7 of 11 expected locations were detected, covering 4 of 5 candidates at least partly. G02–G04, G08–G10 and G12–G20 are outside V1's four families: TLS, exec(), network exposure, destructive kill/rm, package install and instruction-level approval bypass.

## False positives and imprecision

- No row reports a capability that isn't in the code.
- **Target over-approximation.** Rows `run_eval.py:157`, `:209` and `:218` each list 6 target paths. 3 of them combine branches that cannot co-occur (for example `{project_root}/.claude/commands/SKILL.md`), because path folding ignores which branch a value came from.
- **Shared-sink rows.** One `Popen`/`run` call becomes 3 rows, one per runtime-selected CLI. All three are possible at runtime, but at most one runs per invocation.
- **Binary-name assumption.** `agent` is generic. It is correct here (the Cursor CLI), but it is a known false-positive risk on larger samples.

## Important misses (see `missed_behaviors.csv`)

1. **M1: code inside string templates.** set-reminder's generated script removes its own crontab entry (G01 lines 47/51). V1 skips string contents by design.
2. **M2: agent tool calls and prose.** youtube-content instructs recurring `cronjob(...)` agent jobs and placing scripts in `~/.hermes/scripts/` (G11). `~/.hermes` is also absent from the agent-config path list.
3. **M3: new candidate, not in the gap list.** spdd `CODEX.md:7-25` instructs adding a persistent rule block to `AGENTS.md` / `~/.codex/AGENTS.md` and a prompt to `~/.codex/prompts/`.
4. **M4: new candidate, not in the gap list.** moonshot-teams-runner `SKILL.md:20-30, 397` runs forked Claude Code Agent Teams (with `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`). The nesting goes through the host's agent tool, not a CLI. It does include an explicit fanout safety contract.
5. **M5/M6: coverage, not detection.** skill-24eda454b855 is missing 176 files, including `claude_researcher.py`, `orchestrator.py` and `instagram_agent.py`. oat-brainstorm `helper.js` is unsupported, and `server.cjs` is missing.

M3 and M4 come from a keyword sweep of all 30 skills (see `missed_behaviors.csv`). They need human review before entering the candidate list.

## Parse errors

8 Markdown Python blocks failed to parse (`parse_error_dedent_sensitivity.csv`):
- **5 in youtube-content** are indented under list items. They parse after `textwrap.dedent`, which is a SkillGuard bug, but they yield **0 additional findings**, so the bug did not hide any V1 behavior in this sample.
- **3 still fail** (fastapi-workflow ×2, youtube-content ×1). They are not Python: `requirements.txt` lines, `async def f(...)` placeholders, and rename tables.

## What this tells us

1. **V1 is precise where it applies, but the evidence is thin.** All 21 rows are real capabilities, but they come from 2 skills, and 3 of the 4 behaviors were the tuning target. We have no evidence yet about precision or recall on unseen skills.
2. **V1 adds signal Cisco lacks.** Cisco Static/Behavioral reported nothing at any of the 4 behaviors, including in configurations that fully scanned these files.
3. **Row counts overstate.** 21 rows are 4 behaviors in 7 code locations plus 6 documentation examples. Report behaviors, not rows.
4. **The agent-specific risk in this sample lives mostly outside code.** 3 of the 5 in-scope misses are instructions or agent-tool calls in Markdown (M2–M4), and 36 of 102 present files are Markdown with no code at all.

## Next improvements (in priority order)

1. **Group findings into behaviors.** Merge rows that share a sink and report doc-example rows as `documentation_of` the code finding, so counts can't inflate.
2. **Make the analysis branch-aware** for paths and argv, so infeasible targets disappear.
3. **Analyze code embedded in strings** that is written to a file or passed to `bash -c`/`exec` (M1).
4. **Add agent tool-call sinks and an instruction-level layer** for `cronjob(...)`, `terminal(...)`, `Task`/subagent/Agent Teams, and "add this to AGENTS.md" instructions (M2–M4), labeled with a separate carrier so they aren't mixed with code findings. Add `~/.hermes`, `~/.codex/prompts` and similar paths to the config path list.
5. **Dedent indented Markdown fences** (parse bug, no impact here).
6. **Before the 1,000-skill run, evaluate on held-out skills:** a fresh sample not used for tuning, with a human-labeled subset to estimate precision and recall honestly.
