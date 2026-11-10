# Skill `python-f1868b2af2ee`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | alec-c4/agent_dev_kit |
| SKILL.md path | skills/stacks/python/SKILL.md |
| Sample stratum | supporting_no_scripts |
| Folder complete in GitSkills | True |
| Coverage | partially_complete: some configurations are COMPLETE, others are partial, contract-only or failed |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 2 | INFO | exit code 0 |
| SKILL.md only \| behavioral | COMPLETE | 2 | INFO | exit code 0 |
| Full folder \| default | COMPLETE | 2 | INFO | exit code 0 |
| Full folder \| behavioral | COMPLETE | 2 | INFO | exit code 0 |
| SKILL.md only \| behavioral+llm | COMPLETE | 3 | LOW | exit code 0 |
| SKILL.md only \| behavioral+meta | COMPLETE | 2 | INFO | exit code 0 |
| SKILL.md only \| behavioral+llm+meta | PARTIAL | 3 | LOW | Meta-Analyzer degraded: \[{'code': 'META_BATCH_PARSE_FAILED', 'message': 'Meta-analysis response was malformed (Ollama Meta did not classify every expected index exactly once); this batch was retained unchanged.', 'first_index': 0, 'last_index': 2, 'finding_count': 3, 'failure_diagnostic': {'outer_error_code': 'META_BATCH_PARSE_FAILED', 'inner_error_code': 'META_CONTRACT_RESPONSE', 'request_sha256': '33b34f286f8118757a57fadde7eebb00e57bdde567da7530f6d83fba2b0fc625', 'response_sha256': '267e3642f4fae0673089ede6809e468c02b662599f742ac689b8f5a23fa2091e', 'repair_attempted': 1, 'repair_succeeded': 0, 'repair_request_sha256': 'dce2ad10aec4725587d7e6881169faeb7784b2c929f2e9dade20bf294c416960', 'repair_response_sha256': 'b71cf8ba2d9954e99256b0ff16590d4a81214d95438f18b8f7c2d736e3f753c0', 'repair_error_code': 'META_CONTRACT_RESPONSE'}}\] |
| Full folder \| behavioral+llm | COMPLETE | 3 | LOW | exit code 0 |
| Full folder \| behavioral+meta | COMPLETE | 2 | INFO | exit code 0 |
| Full folder \| behavioral+llm+meta | PARTIAL | 3 | LOW | Meta-Analyzer degraded: \[{'code': 'META_BATCH_PARSE_FAILED', 'message': 'Meta-analysis response was malformed (Ollama Meta did not classify every expected index exactly once); this batch was retained unchanged.', 'first_index': 0, 'last_index': 2, 'finding_count': 3, 'failure_diagnostic': {'outer_error_code': 'META_BATCH_PARSE_FAILED', 'inner_error_code': 'META_CONTRACT_RESPONSE', 'request_sha256': '07db0c7ce98e4c606be5409622f1c2c588cc8fce846a4857d8e56cbb370375d6', 'response_sha256': '0c80aa952a10cfe57d30bc8a3dcb6ea095015ce266b70a464defced2399127aa', 'repair_attempted': 1, 'repair_succeeded': 0, 'repair_request_sha256': 'b9991a849ef07b2772c4190dc5bb34f7ca64996524e0642ce51df07c4f74c49f', 'repair_response_sha256': 'e3ff28da9ee0ea4e23100f3e048c8fe40f73605bdfc3a07c86093ab55730edc5', 'repair_error_code': 'META_CONTRACT_RESPONSE'}}\] |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### LOW · LLM_POLICY_VIOLATION · SKILL.md:
|  | value |
|---|---|
| Validation | Scanner alert, not in the review queue |
| Review ID |  |
| Provisional label |  |
| Final (human) label |  |
| Configurations | SKILL.md only \| behavioral+llm; SKILL.md only \| behavioral+llm+meta; Full folder \| behavioral+llm; Full folder \| behavioral+llm+meta |
| Scan outcomes | complete; partial |
| Cisco category | policy_violation |
| Analyzer | llm |
| Evidence check | unavailable |
| Title | Policy violation in manifest |
Evidence snippet:

```text
Manifest has missing license and invalid name (rule: MANIFEST_MISSING_LICENSE, MANIFEST_INVALID_NAME)
```
## Other notes

20 metadata-quality / scan-coverage rows: MANIFEST_INVALID_NAME (10), MANIFEST_MISSING_LICENSE (10).
