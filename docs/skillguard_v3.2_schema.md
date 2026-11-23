# SkillGuard V3.2 output schema (`schema_version` "5.0")

`python -m skillguard <folder> --json` prints one JSON object. Fields marked *list* are always present, possibly empty. All paths are relative to the skill folder, and line numbers are 1-based.

## Top level

| Field | Type | Meaning |
|---|---|---|
| `schema` | string | Always `"skillguard/result"` |
| `schema_version` | string | `"5.0"` |
| `tool` | object | `name`, `version` (`3.2.0`), `sha256` (combined source hash of the package), `python_parser`, `js_parser` |
| `root` | string | Scanned folder as given on the command line |
| `findings` | list | One entry per detected capability or risk indicator (below) |
| `chains` | list | Combinations of findings (below) |
| `behaviors` | list | Findings grouped for counting: capability + key + code/text class. Text-only documentation attaches to a matching code behavior |
| `links` | list | Instruction → file links (below) |
| `declared_tools` | object | Frontmatter `allowed-tools` analysis (below) |
| `coverage` | object | `files` (one entry per file) and `summary` |
| `summary` | object | Counts by layer, category, capability and review priority; `highest_priority` includes chains. Supporting findings are counted separately |

## Finding

| Field | Values | Meaning |
|---|---|---|
| `id` | `F1`… | Stable within one result |
| `fingerprint` | 16 hex | sha256 of capability, file, line, evidence excerpt and key details. Use it to attach validations across runs |
| `capability` | see docs/skillguard_v3.2.md | What was observed |
| `layer` | `capability`, `risk_indicator`, `confirmed_issue` | `confirmed_issue` only after a validation record with `status: confirmed` and a `reviewer` |
| `category`, `category_name` | `T1`…`T9` | Taxonomy category |
| `subcategory`, `subcategory_name` | e.g. `T3.1` | Taxonomy subcategory |
| `severity` | `info` `low` `medium` `high` `critical` | Impact if abused (independent of confidence) |
| `confidence` | `low` `medium` `high` | Certainty of the detection itself |
| `review_priority` | `none` `low` `medium` `high` | Triage order derived from the fields above, not a verdict |
| `detection_method` | `python_ast`, `shell_tokens`, `powershell_lines`, `js_tree_sitter`, `config_structure`, `markdown_heuristic` | How it was found |
| `execution_context` | `direct`, `generated`, `bundled_config`, `skill_metadata`, `documented_example`, `instruction` | Whether and how the evidence runs: code that runs, code written out by code, a config file in the skill, frontmatter, a fenced example, prose |
| `context_tags` | list | e.g. `installation_doc` |
| `supporting` | bool | `true` for plain network use: inventoried for combinations only |
| `risk_indicators` | list | e.g. `bypass_flags`, `env_marker_removal`, `persistent_target`, `credential_target`, `fetch_execute_in_command`, `network_in_command`, `non_official_endpoint`, `insecure_transport`, `outward_action`, `unscoped_shell`, `auto_enable`, `unpinned`, `generated_code`, `concealment`, `invoked_by_instruction` |
| `file`, `line`, `carrier` | | Location and carrier (`executable_script`, `markdown_shell_example`, `markdown_js_example`, `markdown_config_example`, `markdown_instruction`, `config_file`, `frontmatter`, …) |
| `evidence` | object | `excerpt`: the source line with secrets redacted, ≤200 characters. `excerpt_sha256`: 16 hex |
| `explanation` | string | Why the behavior matters, plus the specifics |
| `remediation` | string | Suggested fix (empty for supporting findings) |
| `details` | object | Capability-specific fields, e.g. `commands`, `trust_flags`, `targets`, `target_kind`, `sources`, `operation`, `setting`, `value`, `server`, `hook_event`, `variable`, `endpoint_class`, `config_path`, `matched`. `{name}` marks an unresolved value |
| `invoked_by` | list | Optional. Instruction locations that execute this file |
| `in_chains` | list | Chain IDs that include this finding |
| `validation` | object | `status`: `unvalidated` (default), `confirmed` or `rejected`. Plus `reviewer`, `note`, `date` when given |

## Chain

`chain_id`, `rule`, `category`, `subcategory`, `subcategory_name`, `severity`, `confidence`, `scope` (`same_file`, `linked_files`, `same_skill`), `members` (finding IDs), `evidence` (finding, file, line, capability), `explanation`, `remediation`, `layer` (`risk_indicator`) and `review_priority`. Rule-specific extras: `link` (for `instruction_runs_sensitive_script`) and `installed_file` (for `script_installs_agent_config`).

## Link

`from_file`, `from_line`, `target`, `relation` (`executes` or `references`), `via` (`code_fence`, `inline_code`, `markdown_link`, `prose`), `resolved_by` (`relative`, `root`, `suffix`, `basename`) and `evidence`.

## Declared tools

| Field | Meaning |
|---|---|
| `frontmatter_status` | `parsed`, `absent` or `invalid` |
| `frontmatter_error` | Parser error, if any |
| `declared` | One entry per `allowed-tools` item: `tool`, `pattern`, `raw` |
| `declared_present` | Whether `allowed-tools` exists |
| `broad_shell` | Unscoped `Bash` / `Bash(*)` |
| `observed_needs` | e.g. `Bash`, `Task/Agent`, network |
| `uncovered_commands` | Instructed commands outside the declared Bash scopes |
| `notes` | |

## Coverage

`coverage.files[]` has `file`, `status`, `analyzers` (list) and, when relevant, `skipped_fences`, `config_types`, `line` or `reason`.

| Status | Counts as analyzed? | Meaning |
|---|---|---|
| `analyzed` | yes | |
| `analyzed_with_parse_errors` | yes | JS/TS with tree-sitter error recovery |
| `markdown_instructions_only` | yes | Markdown with no code fences; prose heuristics only |
| `disguised_text_scanned` | yes | |
| `parsed_no_agent_config` | yes | A config file that parsed but holds no agent configuration |
| `parse_error` | no | |
| `data_file_not_analyzed` | no | `.txt`, `.csv`, … |
| `unsupported_format` | no | |
| `unreadable` | no | Binary or undecodable |
| `too_large` | no | Over 2 MB |
| `analyzer_unavailable` | no | |

`coverage.summary` has `files`, `analyzed`, `not_analyzed`, `by_status` and `not_analyzed_by_suffix`.

## Validation records (`--validations FILE`)

A JSON list of `{"fingerprint", "status": "confirmed"|"rejected", "reviewer", "note", "date"}`.

- `confirmed` with a reviewer sets `layer` to `confirmed_issue`.
- `rejected` sets `review_priority` to `none`.

SkillGuard never sets these on its own.
