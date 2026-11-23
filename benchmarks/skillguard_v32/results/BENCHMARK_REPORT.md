# SkillGuard controlled benchmark

Synthetic cases with hand-written expectations. This is a specification/regression test, not an accuracy estimate on real skills.

- Cases: 65; checks: 141
- V3.2: 141/141 checks, 65/65 cases fully passed
- V3.1 (frozen, generous name mapping): 34/47 expressible checks passed; 94 checks need V3.2-only output (severity, priority, confidence, chains, links, new formats); 15/65 cases fully passed

| Group | Cases | V3.2 cases passed | V3.1 cases passed | V3.1 expressible checks passed |
|---|---|---|---|---|
| classification | 13 | 13 | 9 | 23/25 |
| config | 13 | 13 | 0 | 0/0 |
| coverage | 5 | 5 | 3 | 4/5 |
| credentials | 3 | 3 | 1 | 1/1 |
| cross_file | 11 | 11 | 0 | 2/2 |
| execution | 3 | 3 | 0 | 0/0 |
| instruction | 3 | 3 | 2 | 2/3 |
| js_ts | 9 | 9 | 0 | 2/10 |
| regression_fp | 5 | 5 | 0 | 0/1 |

| Case | Kind | V3.2 | V3.1 | Description |
|---|---|---|---|---|
| a01_subagent_delegation | negative | pass | pass | Prose asking the agent to use host sub-agents is a host feature, not an external agent launch. |
| a02_task_tool_call | negative | pass | pass | A Task(subagent_type=...) call in code is in-host delegation. |
| a03_external_cli_from_script | positive | pass | fail | A script launches the claude CLI; SKILL.md runs that script. |
| a04_cli_with_bypass_flag | positive | pass | pass | Shell script runs claude with --dangerously-skip-permissions. |
| a05_agent_specific_force_flag | edge | pass | pass | --force is a bypass for cursor-agent but not for other agent programs. |
| a06_value_dependent_flags | edge | pass | pass | --permission-mode only bypasses with bypassPermissions; --sandbox danger-full-access bypasses. |
| a07_existence_check_only | negative | pass | pass | `command -v claude` only checks that the CLI exists. |
| a08_env_marker_python | positive | pass | fail | Filtered os.environ copy drops CLAUDECODE and the child claude runs with it. |
| a09_no_confirmation_outward_action | positive | pass | fail | A no-confirmation instruction about pushing is an outward action; negated and conditional phrasings are not. |
| a10_bypass_flag_mention_vs_use | edge | pass | pass | Documenting an opt-out of a bypass flag is not an instruction to use it. |
| a11_installation_doc_is_low_priority | negative | pass | pass | README installation steps that copy the skill into ~/.claude/skills are user-run setup. |
| a12_scheduler_list_vs_modify | edge | pass | pass | Listing cron jobs is low severity; rewriting the crontab is a modification. |
| b01_settings_bypass_hook_endpoint | positive | pass | n/a | Bundled Claude settings with bypass mode, a fetch-and-execute SessionStart hook and a raw-IP endpoint. |
| b02_benign_settings | negative | pass | n/a | Scoped permissions and a local formatter hook: no bypass, no endpoint, low priority. |
| b03_mcp_pinned_vs_unpinned | edge | pass | n/a | MCP servers: a pinned package is fine, an unpinned npx package is flagged as supply-chain. |
| b04_mcp_remote_http | positive | pass | n/a | Remote MCP server over plain HTTP to a raw IP. |
| b05_codex_config | positive | pass | n/a | Codex config.toml with approval_policy=never, full-access sandbox and an unpinned uvx MCP server. |
| b06_vscode_autoapprove_task | positive | pass | n/a | VS Code chat auto-approval and a task that runs on folder open. |
| b07_package_json_hooks | edge | pass | n/a | postinstall that downloads and runs code vs a benign prepare hook. |
| b08_registry_redirect_and_token | positive | pass | n/a | .npmrc pointing to a non-default registry with a literal token (redacted in output). |
| b09_markdown_settings_snippet | positive | pass | n/a | SKILL.md shows a settings.json snippet with bypass mode: a documented example, lower priority than active config. |
| b10_malformed_configs | edge | pass | n/a | Malformed JSON/YAML/TOML and a YAML alias bomb are reported as parse errors without crashing. |
| b11_benign_data_files | negative | pass | n/a | Ordinary JSON/YAML data and tool configs produce no findings. |
| b12_endpoint_local_placeholder_official | negative | pass | n/a | Local proxies are low severity; placeholders and official hosts are not reported. |
| b13_frontmatter_preapproval | positive | pass | n/a | Frontmatter pre-approves unscoped Bash and sets permissionMode bypassPermissions. |
| c01_instruction_runs_config_writer | positive | pass | fail | SKILL.md runs setup.py, which writes ~/.claude/settings.json. |
| c02_placeholder_paths_resolve | edge | pass | n/a | Paths written with ${CLAUDE_SKILL_DIR} or ~/.claude/skills/<name>/ resolve to bundled files. |
| c03_reference_only | negative | pass | n/a | A Markdown link to a helper is a reference, not an execution; no chain. |
| c04_credential_and_send_same_file | positive | pass | n/a | One script reads AWS credentials and posts data. |
| c05_credential_and_send_unrelated | edge | pass | n/a | Credential read and network send in unrelated files: chain only at skill scope with low confidence. |
| c06_script_installs_bundled_hooks | positive | pass | fail | install.py copies a bundled settings file containing a hook into ~/.claude/settings.json. |
| c07_fetch_exec_with_cron | positive | pass | n/a | Script downloads and runs a payload and installs a cron job. |
| c08_bypass_instruction_with_launch | positive | pass | n/a | SKILL.md says to use bypass mode and runs a script that launches claude without flags. |
| c09_allowed_tools_scope | edge | pass | n/a | allowed-tools with scoped Bash entries (commas inside parentheses) vs an instructed command outside the scope. |
| c10_preapproved_shell_runs_sensitive_script | positive | pass | n/a | Unscoped Bash pre-approval plus an instruction that runs a script launching an agent with bypass flags. |
| c11_scheduled_agent | positive | pass | n/a | A script installs a crontab and launches an agent program. |
| d01_js_spawn_agent_bypass | positive | pass | fail | ESM spawn of claude with a bypass flag held in a const array. |
| d02_ts_config_write | positive | pass | fail | TypeScript writes ~/.claude/settings.json via path.join(os.homedir(), ...). |
| d03_js_exec_shell_strings | positive | pass | fail | CommonJS execSync of a crontab listing and exec of codex with --full-auto in a template literal. |
| d04_js_env_manipulation | positive | pass | fail | Deleting CLAUDECODE and redirecting OPENAI_BASE_URL to a raw IP. |
| d05_js_credential_exfil | positive | pass | n/a | Reads an SSH private key and POSTs it. |
| d06_js_benign_lookalikes | negative | pass | fail | Strings mentioning claude, a local function named spawn, project-local writes and a GET request. |
| d07_js_syntax_error_recovery | edge | pass | fail | A JS file with a syntax error is still parsed with error recovery and marked in coverage. |
| d08_markdown_js_fence | positive | pass | fail | A JavaScript fence in SKILL.md that runs an agent with --yolo is a documented example. |
| d09_zx_tagged_template | positive | pass | fail | zx $`...` template runs an agent with a bypass flag. |
| e01_fetch_exec_script_vs_readme | edge | pass | n/a | curl|bash in a script is high priority; the same line in README installation steps is low. |
| e02_os_persistence | positive | pass | n/a | Appending to ~/.bashrc and writing a LaunchAgent plist. |
| e03_python_exec_of_download | positive | pass | n/a | exec() of text downloaded with requests. |
| f01_hidden_comment_future_session | positive | pass | pass | An HTML comment with a deferred, concealed instruction. |
| f02_unicode_tag_characters | positive | pass | fail | Invisible Unicode tag characters next to a concealment instruction. |
| f03_benign_silently | negative | pass | pass | Descriptive 'may silently fail' is not concealment. |
| g01_agent_credentials | positive | pass | pass | Reading the Claude credential file. |
| g02_environment_harvest | positive | pass | n/a | Serializing os.environ and posting it. |
| g03_ssh_benign_operations | negative | pass | n/a | Generating a key or printing a public key is not credential access. |
| h01_unsupported_and_data | edge | pass | n/a | Binary-looking and plain data files are reported, not silently skipped. |
| h02_plain_skill | negative | pass | pass | A SKILL.md with ordinary instructions produces no primary findings. |
| h03_crlf_and_bom | edge | pass | fail | CRLF line endings and a UTF-8 BOM do not break parsing or line numbers. |
| h04_generated_script | positive | pass | pass | A Python string template that writes a shell script launching an agent with --yolo. |
| h05_powershell | positive | pass | pass | PowerShell clears CLAUDECODE and launches claude with a bypass flag. |
| a13_systemctl_service_vs_persistence | negative | pass | fail | systemctl start/restart/status manage services; only enable/link installs persistence. |
| i01_printed_install_hint | negative | pass | n/a | An echo that prints an installation hint does not execute it; a pipe into `python3 -c` parses data. |
| i02_fetch_exec_mentioned_without_url | negative | pass | n/a | A table cell saying the skill contains no curl|bash is not an instruction. |
| i03_credential_lookalikes | negative | pass | fail | Writing .npmrc, testing that ~/.claude.json exists, ssh-copy-id, a default-path prompt and a regex are not credential reads. |
| i04_rc_env_export_is_low | edge | pass | n/a | Appending an `export KEY=` line to ~/.bashrc is persistence of configuration (low), not of code. |
| i05_proxy_and_truncated_tokens | negative | pass | n/a | HTTP proxies are low/info, and truncated or sample tokens in docs are not secrets. |
