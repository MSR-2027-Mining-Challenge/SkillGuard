# SkillGuard V3.2: development evaluation and comparison with frozen V3.1

**Date:** 2026-11-22. **Branch:** `skillguard-v3.2`.

- **V3.2 source sha256** (combined package hash; the `tool.sha256` field of every result): `c15e43c3…` (full hash at the end of this report).
- **V3.1:** `eebc59e7`, unchanged and hash-checked by the tests.

> **What this report is not.** No number here is a precision or recall on real skills. The benchmark is a hand-written specification that V3.2 was developed against. The real-skill regression compares two versions of our own tool. Scanner overlap is agreement, not accuracy. Labels in this report are not human-validated.

## 1. Tests

| Suite | Result |
|---|---|
| `PYTHONPATH=src .venv/bin/python -m unittest discover -s tests` | **101 tests, all pass**: V3.1 suite 55 (unchanged), V3.2 suite 22, existing reporting / LLM-pipeline tests 24 |
| Controlled benchmark ([report](../../../benchmarks/skillguard_v32/results/BENCHMARK_REPORT.md)) | **V3.2: 65/65 cases, 141/141 checks.** Frozen V3.1, credited when a finding of the same capability is at the expected file/line: **34/47** checks it can express, **15/65** cases fully. The other 94 checks need output V3.1 does not produce: config/JS formats, chains, links, coverage statuses, severity/priority |

The V3.2 suite (`tests/test_skillguard_v32.py`) covers:

- every benchmark case;
- schema fields and independent scales;
- secret redaction;
- validation records (a confirmed issue requires a reviewer);
- the `allowed-tools` grammar and Bash scope matching;
- agent-specific and value-dependent bypass flags;
- endpoint classification, config target kinds, fetch-execute positives and negatives, persistence and developer-credential paths;
- odd config shapes, oversized, binary and unparsable files, symlinks not followed;
- determinism;
- no subprocess or `os.system` call during scanning;
- the frozen V3.1 hash;
- the JSON CLI.

Benchmark groups:

| Group | Cases | V3.2 | V3.1 (relaxed) |
|---|---|---|---|
| classification (delegation vs external agents, flags, approval phrasing, install docs, schedulers) | 13 | 13 | 9 |
| config (settings, hooks, MCP, Codex, VS Code, package.json, registries, snippets, malformed, benign) | 13 | 13 | 0 |
| cross_file (links, credential + send, bundled hooks installed by code, fetch-exec + cron, allowed-tools) | 11 | 11 | 0 |
| js_ts | 9 | 9 | 0 |
| execution, instruction, credentials, coverage | 14 | 14 | 6 |
| regression_fp (look-alikes found on real skills during this work) | 5 | 5 | 0 |

## 2. V3.1 vs V3.2 on previously used real skills

**Script:** `run_regression.py`. **Outputs:** `2026-11-22_212921/` (`per_skill.csv`, `v32_behaviors.csv`, `v31_vs_v32_locations.csv`, `summary.json`).

**Input:** 1,220 exported folders (1,216 unique skills): the seed-2030 main1000 sample (1,000), seed-2027 (30), held-out seed 2028 (90) and seed 2029 (100). All of these were already used for V1–V3.1 development or evaluation. They are regression data, not held-out data.

### Coverage

Files analyzed rose from 5,260 to 6,098; files not analyzed fell from 1,235 to 397.

| Files | V3.1 analyzed / not | V3.2 analyzed / not |
|---|---|---|
| `.js .mjs .cjs .jsx .ts .tsx` | 0 / 344 | 344 / 0 |
| `.json` | 0 / 324 | 324 / 0 (parsed; agent config recognized where present) |
| `.yaml .yml .toml` | 0 / 172 | 170 / 2 (2 parse errors) |
| `.md .py .sh .ps1` | unchanged | unchanged |
| Still not analyzed | | `.txt` 104, `.html` 68, files without suffix 80, `.csv` 71, `.go` 26, `.css` 22, … |

### Location parity

For every location V3.1 reported in its 7 families (mapped to V3.2 names), V3.2 reports the same capability at the same file and line, with 3 deliberate exceptions:

| Capability | Both | Only V3.1 | Only V3.2 |
|---|---|---|---|
| in-host delegation (V3.1 `nested_agent_invocation`, spawn prose / Task) | 247 | 0 | 0 |
| external agent launch (V3.1 `nested_agent_invocation`, CLI) | 81 | 0 | 2 (a `spawnSync('claude')` in `.mjs`; `copilot agent` in `.ps1`) |
| agent config modification | 231 | 0 | 7 (JS/TS writes, a shell redirect into `.mcp.json`, `~/.config/opencode/skills`) |
| scheduler | 63 | 0 | 10 (`systemctl enable`, `launchctl`) |
| approval bypass | 72 | 2 (negated: "Do not write production code until the user approves…", "Don't pad a clear brief…") | 0 |
| agent credential access | 11 | 1 (`[ -f "$HOME/.claude.json" ]`, an existence test) | 0 |
| env marker removal / suspicious instruction | 9 / 5 | 0 | 0 |

### Inventory and triage

Skill counts below are unique skills (n = 1,216).

| Measure | V3.1 | V3.2 |
|---|---|---|
| Skills with any behavior | 179 | 300 (incl. 128 `tool_preapproval` from frontmatter `allowed-tools`, mostly info) |
| Skills with any behavior, excluding in-host delegation | 137 | 262 |
| Skills with a behavior at review priority ≥ low | n/a | 209 |
| Skills with a high-priority behavior | 23 | 19 (22 including chains) |
| Skills with at least one chain | n/a | 28 |

**High-priority sets** (11 skills in both):

- **Only V3.2 (code-level evidence V3.1 could not see):**
  - `curl … | sh` and `iex (iwr …)` in install scripts (4 skills);
  - a LaunchAgent plist and a `/etc/profile.d` snippet written by scripts (2);
  - a `.mcp.json` generated by `sed` redirect, and a hooks directory created by an installer (2).
- **Only V3.1 (V3.2 rates them medium):**
  - prose approval-bypass phrases and prose mentions of credential files (low-confidence evidence is capped at medium);
  - documented examples.

  This is the intended down-weighting of text-only evidence. The two hidden deferred `curl … | bash` payloads (`ecommerce-email-quote`, `case_00858`) briefly dropped to medium during development; they are high again after the suspicious-instruction confidence fix described in §4.

**V3.2 behaviors by capability** (unique skills):

| Group | Behaviors |
|---|---|
| tool pre-approval | 128 |
| agent config modification | 104 |
| in-host delegation | 71 |
| approval bypass | 41 |
| external agent launch | 35 |
| MCP server definition | 25 |
| scheduler | 21 |
| fetch-and-execute | 12 |
| OS persistence | 8 |
| agent credentials | 7 |
| unpinned package | 7 |
| agent hook command | 7 |
| env marker removal | 5 |
| suspicious instruction | 3 |
| developer credentials | 2 |
| install hook | 2 |
| endpoint override | 2 |
| embedded secret | 1 |

- **By evidence level:** instruction-only 197, skill metadata 125, documented example 86, code 53, config 19, generated code 1.
- **By priority:** high 19, medium 206, low 123, none 133.
- **Chains (skills):**

| Chain rule | Skills |
|---|---|
| instruction runs sensitive script | 25 |
| nesting guard removed for agent launch | 5 |
| bypass with external agent | 4 |
| scheduled agent run | 1 |
| pre-approved shell runs sensitive script | 1 |
| credential access with network send | 1 |

- **Cisco (seed-2030 sample):** 11 of 396 V3.2 behaviors have a Cisco core security finding within ±3 lines (V3.1: 4 of 244). The tools still mostly look at different things.
- **Runtime:** V3.1 25 s, V3.2 36 s for 1,220 folders.

## 3. False-positive patterns found on real skills and fixed

The real-skill output was inspected item by item for every new capability and every high-priority behavior. These patterns were fixed and added to the benchmark (`regression_fp`, `a13`):

- `systemctl start/stop/restart/status` was treated as scheduling. Now only `enable`, `link` and `reenable` count.
- `echo "curl … | sh"` (a printed hint), `curl … | python3 -c '…'` (JSON parsing) and "no curl|bash" in a table were treated as fetch-and-execute.
- Writing `.npmrc`, `[ -f ~/.claude.json ]`, `ssh-copy-id`, a prompt's default path, and a regex containing `\.azure\.` were treated as credential access.
- `echo 'export KEY=…' >> ~/.bashrc` is now low severity; appending a `source`/command line stays high.
- HTTP(S) proxies are low or info rather than endpoint hijacks. Truncated or sample tokens (`eyJ…`, `abc123`, `…`) are not secrets.
- `mkdir` of a hooks directory is medium; writes to settings/hooks stay high.

## 4. Known remaining weaknesses

- **Prose detections** (approval bypass, config instructions, delegation) remain regex heuristics. They are low confidence and capped at medium priority.
- **The suspicious-instruction detector** found 3 behaviors in 1,216 skills. Its recall on new positives is untested beyond the synthetic cases and the known adversarial samples.
- **`tool_preapproval` from `allowed-tools`** appears in 128 skills; most are scoped and info. It is reported for transparency and excluded from priority.
- **Not analyzed:** HTML, `.txt`, compiled languages.
- **No interprocedural or cross-language dataflow.** Chains connect findings by file and instruction links, not by value flow.
- **Incomplete-folder anomaly:** the main1000 observation that incomplete script folders carry more SkillGuard behaviors was not investigated further here.

## 5. Scanner comparison

### Cisco core vs core + ATR on the controlled benchmark

**Script:** `../v32_scanner_comparison/run_benchmark_scanners.py`. **Outputs:** `../v32_scanner_comparison/2026-11-22_211928/`.

**Setup:** skill-scanner 2.3.1, policy balanced, behavioral on, run on the 65 synthetic folders. An expected V3.2 finding counts as *located* if the configuration reports a non-INFO finding in the same file within ±3 lines (or anywhere in the file when the expectation has no line).

| | Cisco core | Cisco core + ATR |
|---|---|---|
| Cases with any security finding | 20 / 65 | 32 / 65 |
| Security findings | 39 | 72 |
| Expected V3.2 findings located (of 54 with a file) | 19 | 21 |

By capability:

| Capability | Expected | Located by core | Located by core + ATR |
|---|---|---|---|
| external agent launch | 13 | 4 | 5 |
| fetch-and-execute | 6 | 4 | 4 |
| auto-approval settings | 4 | 0 | 0 |
| OS persistence writes | 4 | 0 | 0 |
| agent config writes | 4 | 1 | 1 |
| hooks, MCP | 1, 0 | 0 | 0 |
| install hooks, registry redirect, embedded secret | 1, 1, 1 | 0 | 0 |
| suspicious instructions | 2 | 2 | 2 |
| credentials, environment harvesting, network | | mostly located | mostly located |

- **ATR adds mostly prose-level matches.** Its agent-configuration regexes look for verbs such as "write to .claude/settings" or "inject into CLAUDE.md". They did not fire on parsed configuration structure (a `defaultMode: bypassPermissions`, a `SessionStart` hook, `approval_policy = "never"`) or on code that writes to agent paths.
- **This is a synthetic, small-n comparison against our own definitions.** Cisco was not built around them, and the result is not an accuracy estimate for either tool. Whether ATR matters on real skills is measured by the 5th configuration in the next experiment.

### V3.2 vs existing MalSkills results

**Script:** `compare_malskills_overlap.py`. **Outputs:** `../v32_scanner_comparison/malskills_overlap_2026-11-22_212601/`.

**Setup:** 74 skills appear both in Rio's MalSkills 1,000 (branch `rio`, static profile, CRLF-translated export) and in the seed-2030 sample. Their identities were mapped by content hash.

| Measure | Result |
|---|---|
| MalSkills: skills with ≥1 SSO | 30 |
| MalSkills: malicious verdicts | 0 |
| V3.2: skills with a reviewable finding | 6 |
| Both | 4 |
| V3.2 reviewable findings with a MalSkills SSO within ±3 lines | 0 of 10 |

- V3.2 finds agent config writes, MCP servers, tool pre-approval and unpinned MCP packages.
- MalSkills SSOs are generic operation evidence (file, network, installation).
- The overlap is too small for more than a qualitative statement.

### Summary: what each tool covers (from the research plan, checked against these runs)

| Area | Cisco core | Cisco ATR (optional) | MalSkills (static) | SkillGuard V3.2 |
|---|---|---|---|---|
| Generic code security, secrets, prompt injection | yes | yes (prose regex) | operation evidence plus malicious-chain patterns | out of scope (deliberately) |
| Agent configuration content (hooks, MCP, permission modes, auto-approve, endpoints) | no | regex on paths/prose only | generic file/config operations | **parsed structure** |
| External agent launches with bypass flags; nesting-guard removal | generic command execution | partial | generic exec | **resolved argv, agent-specific flags** |
| In-host delegation vs external agents | no | no | no | **yes** |
| Cross-file evidence | behavioral cross-file taxonomy | no | dependency graph (strong) | instruction→script links, `allowed-tools`, 8 chain rules |
| JS/TS | yes | regex | yes | yes (tree-sitter) |
| Per-file coverage report | no | no | caps only | **yes** |
| Severity vs confidence vs priority | severity only | severity only | verdict | **separate fields** |

## 6. Next 1,000-skill experiment

Prepared, not launched; see [../next1000/README.md](../next1000/README.md).

- **Sample:** seed 2031, 400/300/300, with 2,174 previously used identities excluded.
- **Lockbox:** 250 skills, untouched.
- **Pilot:** 12 skills through notebook 01 (48 Cisco scans), export verification, Cisco + ATR, SkillGuard V3.1 and V3.2. Byte-identical exports, deterministic outputs.
- **MalSkills:** the corpus is prepared, but MalSkills is not installed in this environment.

## Reproduce

```bash
PYTHONPATH=src .venv/bin/python -m unittest discover -s tests
PYTHONPATH=src .venv/bin/python -I benchmarks/skillguard_v32/run_benchmark.py --out benchmarks/skillguard_v32/results
PYTHONPATH=src .venv/bin/python -I results/skillguard_runs/v32_regression/run_regression.py
.venv/bin/python -I results/skillguard_runs/v32_scanner_comparison/run_benchmark_scanners.py
PYTHONPATH=src .venv/bin/python -I results/skillguard_runs/v32_scanner_comparison/compare_malskills_overlap.py
```

The V3.2 package sha256 for all results in this report is `c15e43c3d796dd5fc00aff62671fa2977adb7a76a18b7f888e39785e9f9aa82b`.
