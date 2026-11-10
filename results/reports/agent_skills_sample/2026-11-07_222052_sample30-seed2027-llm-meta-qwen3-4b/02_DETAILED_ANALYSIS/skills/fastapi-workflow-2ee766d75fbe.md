# Skill `fastapi-workflow-2ee766d75fbe`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | MikeCheng1208/BattleTree |
| SKILL.md path | .agents/skills/fastapi-workflow/SKILL.md |
| Sample stratum | skill_md_only |
| Folder complete in GitSkills | True |
| Coverage | partially_complete: some configurations are COMPLETE, others are partial, contract-only or failed |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 1 | INFO | exit code 0 |
| SKILL.md only \| behavioral | COMPLETE | 1 | INFO | exit code 0 |
| Full folder \| default | COMPLETE | 1 | INFO | exit code 0 |
| Full folder \| behavioral | COMPLETE | 1 | INFO | exit code 0 |
| SKILL.md only \| behavioral+llm | COMPLETE | 3 | LOW | exit code 0 |
| SKILL.md only \| behavioral+meta | COMPLETE | 1 | INFO | exit code 0 |
| SKILL.md only \| behavioral+llm+meta | PARTIAL | 3 | LOW | Meta-Analyzer degraded: \[{'code': 'META_BATCH_PARSE_FAILED', 'message': 'Meta-analysis response was malformed (Ollama Meta did not classify every expected index exactly once); this batch was retained unchanged.', 'first_index': 0, 'last_index': 2, 'finding_count': 3, 'failure_diagnostic': {'outer_error_code': 'META_BATCH_PARSE_FAILED', 'inner_error_code': 'META_CONTRACT_RESPONSE', 'request_sha256': 'd266e60abf6e7716f0013b238ec606da6c0bf86effad8fdb33969d11ac25377b', 'response_sha256': '2e03ac9a2928b4628663709976241c8bcf6b60ef61739e8adcaaf344f3491818', 'repair_attempted': 1, 'repair_succeeded': 0, 'repair_request_sha256': '6d8d0e7c65b7c63979e73b2da4c52d9d1ca26bdb9b8c2916cbc16033bf62085c', 'repair_response_sha256': '70f123edbd12eface30651bfd36b58487a46f2f90edd55435f28e41ba486b721', 'repair_error_code': 'META_CONTRACT_RESPONSE'}}\] |
| Full folder \| behavioral+llm | COMPLETE | 3 | LOW | exit code 0 |
| Full folder \| behavioral+meta | COMPLETE | 1 | INFO | exit code 0 |
| Full folder \| behavioral+llm+meta | PARTIAL | 3 | LOW | Meta-Analyzer degraded: \[{'code': 'META_BATCH_PARSE_FAILED', 'message': 'Meta-analysis response was malformed (Ollama Meta did not classify every expected index exactly once); this batch was retained unchanged.', 'first_index': 0, 'last_index': 2, 'finding_count': 3, 'failure_diagnostic': {'outer_error_code': 'META_BATCH_PARSE_FAILED', 'inner_error_code': 'META_CONTRACT_RESPONSE', 'request_sha256': '69d70d6022521cd95757ee1da379dca8372d22e622d9b8320a14f419d3c53ac6', 'response_sha256': '903be512158d4f923bb65c783f7c8dc0425cc1b7a612f93b7f0c20ce3b404cb1', 'repair_attempted': 1, 'repair_succeeded': 0, 'repair_request_sha256': '03dba873c4fa131edc2658ec3031e1d281da3cfcfed80b27aa35a81351a8a11c', 'repair_response_sha256': '2f73902874da72ddcdda74a2494e02af8026fa38543f33ef19a6f84a0579d5f1', 'repair_error_code': 'META_CONTRACT_RESPONSE'}}\] |
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
| Title | Mandatory MCP tool calls before implementation |
Evidence snippet:

```text
DOCS FIRST, CODE SECOND
You MUST NEVER generate FastAPI code without first fetching relevant documentation via MCP tools.
This is NON-NEGOTIABLE. Every workflow below has MANDATORY MCP fetch steps that MUST be completed before implementation.
```
## Other notes

14 metadata-quality / scan-coverage rows: MANIFEST_MISSING_LICENSE (10), LLM_CONTEXT_BUDGET_EXCEEDED (4).
