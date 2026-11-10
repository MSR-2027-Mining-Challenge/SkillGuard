# Skill `summarize_text_with_key_details-06e4bdda53f8`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | MikeCheng1208/BattleTree |
| SKILL.md path | .agents/skills/summarize_text_with_key_details/SKILL.md |
| Sample stratum | skill_md_only |
| Folder complete in GitSkills | True |
| Coverage | partially_complete: some configurations are COMPLETE, others are partial, contract-only or failed |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 2 | INFO | exit code 0 |
| SKILL.md only \| behavioral | COMPLETE | 2 | INFO | exit code 0 |
| Full folder \| default | COMPLETE | 2 | INFO | exit code 0 |
| Full folder \| behavioral | COMPLETE | 2 | INFO | exit code 0 |
| SKILL.md only \| behavioral+llm | COMPLETE | 3 | HIGH | exit code 0 |
| SKILL.md only \| behavioral+meta | COMPLETE | 2 | INFO | exit code 0 |
| SKILL.md only \| behavioral+llm+meta | PARTIAL | 3 | HIGH | Meta-Analyzer degraded: \[{'code': 'META_BATCH_PARSE_FAILED', 'message': 'Meta-analysis response was malformed (Ollama Meta did not classify every expected index exactly once); this batch was retained unchanged.', 'first_index': 0, 'last_index': 2, 'finding_count': 3, 'failure_diagnostic': {'outer_error_code': 'META_BATCH_PARSE_FAILED', 'inner_error_code': 'META_CONTRACT_RESPONSE', 'request_sha256': '16849047475c220c0c745b94bd65fe72c9dff77aed3c7c61765fbb4a28b56881', 'response_sha256': 'f0ec0d2da09b29ae37bae758721129ed5a619a0d2f8cd83bf0c64402943b0eea', 'repair_attempted': 1, 'repair_succeeded': 0, 'repair_request_sha256': '7aa0d588d5e6ce56a8d68c2ef109ba20f1e401379c8bcb7b245c64de397d0da1', 'repair_response_sha256': '2ef3af8f4d153bd43165ed52a26e3b344cc6c72b44263a50bc15723dc0c3e11d', 'repair_error_code': 'META_CONTRACT_RESPONSE'}}\] |
| Full folder \| behavioral+llm | COMPLETE | 3 | HIGH | exit code 0 |
| Full folder \| behavioral+meta | COMPLETE | 2 | INFO | exit code 0 |
| Full folder \| behavioral+llm+meta | PARTIAL | 3 | HIGH | Meta-Analyzer degraded: \[{'code': 'META_BATCH_PARSE_FAILED', 'message': 'Meta-analysis response was malformed (Ollama Meta did not classify every expected index exactly once); this batch was retained unchanged.', 'first_index': 0, 'last_index': 2, 'finding_count': 3, 'failure_diagnostic': {'outer_error_code': 'META_BATCH_PARSE_FAILED', 'inner_error_code': 'META_CONTRACT_RESPONSE', 'request_sha256': 'c62e120250939c132cdea6faba940e919ac62564731a4cf4308f736858ea7f86', 'response_sha256': 'cf76112045942f3af1ba871e0276af51b4c01708fff75cca8a91514d06c20def', 'repair_attempted': 1, 'repair_succeeded': 0, 'repair_request_sha256': '753a468646921b2b07304307d8a563f343a66f485d314e823ea09a253e907183', 'repair_response_sha256': '72b1b5506d74890ad524479561644989f6bba7a655dd5f8334d181cfd3869a10', 'repair_error_code': 'META_CONTRACT_RESPONSE'}}\] |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### HIGH · LLM_PROMPT_INJECTION · SKILL.md:
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
| Title | Conditional Adaptation Rule Overriding User Intent |
Evidence snippet:

```text
Conditional Adaptation: If completeness is requested: Prioritize retaining all critical facts, key processes, and important details. The output can be a concise paragraph or a more detailed set of bullet points, ensuring no essential information is omitted.
```
## Other notes

20 metadata-quality / scan-coverage rows: MANIFEST_INVALID_NAME (10), MANIFEST_MISSING_LICENSE (10).
