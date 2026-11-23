# SkillGuard V3.2

SkillGuard is a static, read-only security analyzer for AI agent skill folders (`SKILL.md` plus bundled scripts, references and configuration). V3.2 is the first version organized around a security taxonomy. It separates what a skill **can do** (capabilities) from what **deserves review** (risk indicators). A **confirmed issue** can only come from an independent human validation record.

- **Code:** `src/skillguard/` (package). Frozen V3.1 stays unchanged in `src/skillguard_capabilities.py` and `results/skillguard_runs/versions/`.
- **Output schema:** [skillguard_v3.2_schema.md](skillguard_v3.2_schema.md).
- **Evaluation:**
  - [benchmark report](../benchmarks/skillguard_v32/results/BENCHMARK_REPORT.md)
  - [V3.1 vs V3.2 report](../results/skillguard_runs/v32_regression/REPORT_v32.md)

```bash
PYTHONPATH=src .venv/bin/python -m skillguard path/to/skill            # text report, grouped by review priority
PYTHONPATH=src .venv/bin/python -m skillguard path/to/skill --json     # machine-readable (schema 5.0)
PYTHONPATH=src .venv/bin/python -m skillguard path/to/skill --validations reviews.json
```

Nothing from a skill is imported or executed. Symlinks are not followed. Files over 2 MB, binary files and malformed input are reported in the coverage section instead of being silently skipped.

## What changed from V3.1

| Area | V3.1 | V3.2 |
|---|---|---|
| Classification | 7 capability families, a single review priority | T1–T9 taxonomy with subcategories; separate `severity` (impact), `confidence` (detection certainty), `review_priority` (triage) and `layer` (capability / risk indicator / confirmed issue) |
| Sub-agents | Prose "spawn sub-agents" and agent CLI launches were both `nested_agent_invocation` | `in_host_delegation` (host feature, info) vs `external_agent_launch` |
| Permission flags | One flag list for every agent; `--force` counted everywhere | Per-agent flags (`--force` only for cursor-agent); value flags (`--permission-mode bypassPermissions`, `--sandbox danger-full-access`, `-a never`, `--approval-mode yolo`) |
| Approval bypass | Phrase regex | Adds negation of the phrase itself ("never skip the confirmation") and outward actions ("do not ask …; push the branch") as T2.3 |
| Configuration | `.json/.yaml/.toml` not analyzed | Structural analysis of agent settings, hooks, MCP servers, Codex/VS Code/Aider configs, `package.json` install hooks, registries, embedded secrets; JSON/YAML/TOML snippets in Markdown |
| JavaScript/TypeScript | Not analyzed | tree-sitter analysis of `.js .mjs .cjs .jsx .ts .mts .cts .tsx` and JS fences |
| Cross-file | None | Instruction→file links, `allowed-tools` grammar and scope check, 8 combination rules (chains) |
| Persistence / execution | crontab, schtasks, launchctl | Adds `systemctl enable/link`, `at`, shell rc files, LaunchAgents, systemd units, Startup folder, fetch-and-execute |
| Credentials / egress | Agent credential files | Adds developer credentials (code-level reads only), environment harvesting, network send/fetch (supporting), endpoint overrides |
| Output | Findings + behaviors | Evidence excerpt (secrets redacted) with hash, explanation, remediation, fingerprints, chains, links, declared tools, per-file coverage with analyzers |

## Taxonomy and detections

| Category | Subcategory | Capability (`capability`) | Default severity | Detected in |
|---|---|---|---|---|
| T1 Instruction manipulation | T1.2 hidden / T1.3 deferred / T1.4 pre-approval | `suspicious_agent_instruction` (layer: risk indicator) | high | Markdown blocks with ≥2 signals incl. a core signal (future-session trigger, concealment, pre-approval claim, HTML-comment imperative, invisible Unicode incl. Tag characters, disguised file) |
| T2 Autonomy and oversight | T2.1 approval bypass | `approval_bypass_instruction` | low (phrase), high (permission flag) | Markdown prose |
| | T2.2 permission flags / auto-approval | `auto_approval_setting`, `tool_preapproval` | high / low–medium | configs, frontmatter (`allowed-tools`, `permissionMode`) |
| | T2.3 outward action without confirmation | `approval_bypass_instruction` + `outward_action` | medium | Markdown prose |
| | T2.4 external agent program | `external_agent_launch` | medium (high with bypass flags or removed markers) | py, sh, ps1, js/ts, fences, inline code |
| | T2.5 nesting guard removal | `agent_env_marker_removal` | medium | py, sh, ps1, js/ts |
| | T2.7 in-host delegation | `in_host_delegation` | info (priority none) | prose, Task/Agent tool calls |
| T3 Agent environment and persistence | T3.1 settings / hooks / startup commands | `agent_config_modification` (target kind), `agent_hook_command` | high (settings, hooks, MCP), medium (instructions, skills dirs) | code writes/copies; configs (hooks, statusLine, apiKeyHelper, Codex `notify`, VS Code folder-open tasks) |
| | T3.2 MCP servers | `mcp_server_definition` | low (medium for plain HTTP or auto-enabled; high with fetch-execute) | `mcpServers`, VS Code `servers`, Codex `[mcp_servers]` |
| | T3.3 / T3.4 instruction, memory and skill files | `agent_config_modification` | medium | code and prose |
| | T3.5 OS persistence | `scheduler_invocation`, `os_persistence_write` | medium / high (low for `export VAR=` rc lines) | commands, file writes, redirects |
| | T3.6 endpoint override | `agent_endpoint_override` | high (non-official host), low (localhost or proxies) | code env assignments, configs |
| T4 Credentials | T4.1 agent / T4.2 developer | `agent_credential_access`, `developer_credential_access` | high | code reads (prose mentions excluded for developer credentials) |
| | T4.3 environment harvesting | `environment_harvesting` | medium | serializing / sending the whole environment |
| | T4.4 embedded secret | `embedded_secret` | medium | configs (value redacted) |
| T5 Egress (supporting) | T5.1 send / T5.2 fetch | `network_send`, `network_fetch` | info, never prioritized | py, sh, js/ts; used only in combinations |
| T6 Execution | T6.1 fetch-and-execute | `remote_fetch_execute` | high | pipes to shells/interpreters, process substitution, `iex(iwr)`, `exec(requests.get().text)`, eval of downloads, hooks/MCP/install-hook commands |
| T7 Supply chain | T7.1 / T7.3 / T7.4 | `unpinned_package_execution`, `registry_redirect`, `install_time_hook` | low / medium / medium | MCP server commands, `.npmrc`/`pip.conf`/uv index, `package.json` scripts |
| T8 Consistency and composition | T8.1 / T8.3 / T8.4 | chains (below), `declared_tools` section | per chain | cross-file |

### Combinations (chains, layer `risk_indicator`)

| Rule | Members | Severity |
|---|---|---|
| `credential_access_with_network_send` | credential read or environment harvest + network send (code) | high (one step lower and low confidence when only in the same skill) |
| `bypass_with_external_agent` | external agent launch + bypass instruction, setting or unscoped shell pre-approval (same or linked files) | high |
| `nesting_guard_removed_for_agent_launch` | marker removal + external agent launch | high |
| `fetch_execute_with_persistence` | fetch-and-execute + scheduler / rc write / hook / settings write | critical |
| `scheduled_agent_run` | scheduler modification + external agent launch | high |
| `script_installs_agent_config` | code copies a bundled config file that has findings into an agent config path | high |
| `instruction_runs_sensitive_script` | an instruction executes a bundled file with medium+ capabilities | medium |
| `preapproved_shell_runs_sensitive_script` | the above + unscoped `allowed-tools: Bash` | high |

Scopes: `same_file`, `linked_files` (connected by an executes-link from an instruction), `same_skill`. Documented examples and installation docs never form chains.

## Severity, confidence and review priority

- **Severity:** the impact if the capability were abused. It comes from the capability and its specifics, e.g. a settings or hooks target vs a skills directory, or bypass flags present. It does not depend on how sure the detection is.
- **Confidence:** how certain the detection is.
  - `high`: parsed configuration, or code whose security-relevant token (agent binary, config/credential path) is a single resolved literal.
  - `medium`: several runtime alternatives, generated code, documented examples, network heuristics, or inline-code instructions.
  - `low`: prose heuristics.
- **Review priority:** a triage order derived from severity, execution context and risk indicators. It is not a verdict.
  - Documented examples and bundled (inactive) configs drop one level.
  - Installation docs are capped at low.
  - Bypass flags, fetch-execute in auto-run commands, marker removal, concealment and credential targets raise it one level.
  - Low-confidence evidence is capped at medium.
  - Supporting and info findings have priority `none`.

## Known limitations

- **Static analysis only:** file-local constant folding, no interprocedural or cross-language dataflow. Values built at runtime become `{placeholders}`.
- **Prose rules are heuristic** and mostly English (plus some Russian verb stems). Paraphrased or obfuscated instructions are missed.
- **Some config key names are heuristics.** The generic auto-approval keys (`autoApprove`, `alwaysAllow`, `yolo`, `approval_mode`, …) are matched by name across agent configs. The Claude Code, Codex, VS Code and Aider keys used are those documented by the respective tools and cited in the research plan; other tools' formats may differ.
- **JSON/TOML line numbers are located textually** after parsing (first occurrence after the parent key). YAML uses parser marks.
- **Bundled configs are treated as inactive** (one priority level lower), because a skill's own `.claude/settings.json` is only loaded if it is installed somewhere active. The `script_installs_agent_config` chain covers the case where code installs it.
- **Not analyzed:** HTML, `.txt`, compiled languages (Go, Java, …), notebooks, binaries and archives. These are listed in coverage.
- **No accuracy claim.** The benchmark is a hand-written specification and V3.2 was developed against it. Real-skill regressions only compare tools. No precision or recall on real skills has been measured, and none should be inferred.
