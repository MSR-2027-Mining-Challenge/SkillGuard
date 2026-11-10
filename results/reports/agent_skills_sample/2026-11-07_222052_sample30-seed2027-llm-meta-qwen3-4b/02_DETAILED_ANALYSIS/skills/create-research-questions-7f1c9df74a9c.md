# Skill `create-research-questions-7f1c9df74a9c`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | harivansh-afk/rpi |
| SKILL.md path | .claude/skills/create-research-questions/SKILL.md |
| Sample stratum | supporting_no_scripts |
| Folder complete in GitSkills | True |
| Coverage | partially_complete: some configurations are COMPLETE, others are partial, contract-only or failed |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 1 | INFO | exit code 0 |
| SKILL.md only \| behavioral | COMPLETE | 1 | INFO | exit code 0 |
| Full folder \| default | COMPLETE | 1 | INFO | exit code 0 |
| Full folder \| behavioral | COMPLETE | 1 | INFO | exit code 0 |
| SKILL.md only \| behavioral+llm | COMPLETE | 2 | LOW | exit code 0 |
| SKILL.md only \| behavioral+meta | COMPLETE | 1 | INFO | exit code 0 |
| SKILL.md only \| behavioral+llm+meta | COMPLETE | 2 | LOW | exit code 0 |
| Full folder \| behavioral+llm | COMPLETE | 2 | HIGH | exit code 0 |
| Full folder \| behavioral+meta | COMPLETE | 1 | INFO | exit code 0 |
| Full folder \| behavioral+llm+meta | PARTIAL | 3 | HIGH | Meta-Analyzer degraded: \[{'code': 'META_BATCH_PARSE_FAILED', 'message': 'Meta-analysis response was malformed (Ollama Meta did not classify every expected index exactly once); this batch was retained unchanged.', 'first_index': 0, 'last_index': 2, 'finding_count': 3, 'failure_diagnostic': {'outer_error_code': 'META_BATCH_PARSE_FAILED', 'inner_error_code': 'META_CONTRACT_RESPONSE', 'request_sha256': '99279d0a4d8a61ae1f6fbf79b7c28149f736d0c0a9c971f98f7b0f929bc4e251', 'response_sha256': '03eaa77c18c6e6392459fcc08423710611bcce15954ff633ce692e25fefce7a1', 'repair_attempted': 1, 'repair_succeeded': 0, 'repair_request_sha256': '004ebc787b45b2cee2ac739d3ef0b23690d781a64586385fb2e928a20452492e', 'repair_response_sha256': 'a1f193c840422c2e94690468126e965f28d94a6a86240aeecb3c2a91d6f49450', 'repair_error_code': 'META_CONTRACT_RESPONSE'}}\] |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### LOW · LLM_PROMPT_INJECTION · SKILL.md:
|  | value |
|---|---|
| Validation | Scanner alert, not in the review queue |
| Review ID |  |
| Provisional label |  |
| Final (human) label |  |
| Configurations | SKILL.md only \| behavioral+llm; SKILL.md only \| behavioral+llm+meta; Full folder \| behavioral+llm; Full folder \| behavioral+llm+meta |
| Scan outcomes | complete; partial |
| Cisco category | prompt_injection |
| Analyzer | llm |
| Evidence check | unavailable |
| Title | Potential prompt injection via instruction override |
Evidence snippet:

```text
You have access to specialized agents to help research the codebase: ... Read all @-mentioned files immediately and FULLY ... Review them carefully before creating questions
```
### MEDIUM · LLM_PROMPT_INJECTION · references/research_questions_template.md:
|  | value |
|---|---|
| Validation | Scanner alert, not in the review queue |
| Review ID |  |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| behavioral+llm+meta |
| Scan outcomes | partial |
| Cisco category | prompt_injection |
| Analyzer | llm |
| Evidence check | unavailable |
| Title | Indirect prompt injection via template files |
Evidence snippet:

```text
The template file contains a list of research questions that could be used to prompt the agent to execute unintended actions if the template is modified
```
## Other notes

10 metadata-quality / scan-coverage rows: MANIFEST_MISSING_LICENSE (10).
