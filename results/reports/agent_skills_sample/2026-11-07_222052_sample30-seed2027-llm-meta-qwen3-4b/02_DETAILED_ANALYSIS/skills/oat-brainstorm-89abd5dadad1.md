# Skill `oat-brainstorm-89abd5dadad1`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | tkstang/open-agent-toolkit |
| SKILL.md path | .agents/skills/oat-brainstorm/SKILL.md |
| Sample stratum | scripts |
| Folder complete in GitSkills | False |
| Coverage | partially_complete: some configurations are COMPLETE, others are partial, contract-only or failed |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 1 | INFO | exit code 0 |
| SKILL.md only \| behavioral | COMPLETE | 1 | INFO | exit code 0 |
| Full folder \| default | SKIPPED_INCOMPLETE_FOLDER |  |  | SKIPPED_INCOMPLETE_FOLDER: GitSkills did not store every file of this folder (missing: 1) |
| Full folder \| behavioral | SKIPPED_INCOMPLETE_FOLDER |  |  | SKIPPED_INCOMPLETE_FOLDER: GitSkills did not store every file of this folder (missing: 1) |
| SKILL.md only \| behavioral+llm | COMPLETE | 4 | LOW | exit code 0 |
| SKILL.md only \| behavioral+meta | COMPLETE | 1 | INFO | exit code 0 |
| SKILL.md only \| behavioral+llm+meta | PARTIAL | 3 | LOW | Meta-Analyzer degraded: \[{'code': 'META_BATCH_PARSE_FAILED', 'message': 'Meta-analysis response was malformed (Ollama Meta did not classify every expected index exactly once); this batch was retained unchanged.', 'first_index': 0, 'last_index': 2, 'finding_count': 3, 'failure_diagnostic': {'outer_error_code': 'META_BATCH_PARSE_FAILED', 'inner_error_code': 'META_CONTRACT_RESPONSE', 'request_sha256': '5139fbd50d1ad0b364ffd687ba7b56920636de5ea6d009d2e00685886c52c807', 'response_sha256': 'a48bae916366fda286387c442c0520945c14cd02f8c4b54bcde307d0cee9c432', 'repair_attempted': 1, 'repair_succeeded': 0, 'repair_request_sha256': 'dab775ff7c146294739e13ffe53b511c6ad139a72542831d18cb0e59fa1af002', 'repair_response_sha256': 'af6824a9b729f1953ed392719aa2e23caffe8c7f44c7da4188b4ea453c9632d2', 'repair_error_code': 'META_CONTRACT_RESPONSE'}}\] |
| Full folder \| behavioral+llm | SKIPPED_INCOMPLETE_FOLDER |  |  | SKIPPED_INCOMPLETE_FOLDER: GitSkills did not store every file of this folder (missing: 1) |
| Full folder \| behavioral+meta | SKIPPED_INCOMPLETE_FOLDER |  |  | SKIPPED_INCOMPLETE_FOLDER: GitSkills did not store every file of this folder (missing: 1) |
| Full folder \| behavioral+llm+meta | SKIPPED_INCOMPLETE_FOLDER |  |  | SKIPPED_INCOMPLETE_FOLDER: GitSkills did not store every file of this folder (missing: 1) |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### LOW · LLM_PROMPT_INJECTION · SKILL.md:
|  | value |
|---|---|
| Validation | Scanner alert, not in the review queue |
| Review ID |  |
| Provisional label |  |
| Final (human) label |  |
| Configurations | SKILL.md only \| behavioral+llm; SKILL.md only \| behavioral+llm+meta |
| Scan outcomes | complete; partial |
| Cisco category | prompt_injection |
| Analyzer | llm |
| Evidence check | unavailable |
| Title | Hard Activation triggers without user confirmation |
Evidence snippet:

```text
The skill's Activation Contract states: 'Do NOT auto-enter; respond conversationally and offer mode only after ≥2 sustained exploratory turns.' However, the skill also states that Hard Activation runs the full Process flow for explicit hard-activation triggers like '/oat-brainstorm' or 'let's brainstorm X', which can be triggered without user confirmation for ambiguous exploratory phrasing.
```
## Other notes

7 metadata-quality / scan-coverage rows: MANIFEST_MISSING_LICENSE (5), LLM_CONTEXT_BUDGET_EXCEEDED (2).
