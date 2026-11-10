# Skill `f-hypothesis-ledger-0b6cb775953e`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | FurtherBank/cpu-ai |
| SKILL.md path | skills/f-hypothesis-ledger/SKILL.md |
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
| SKILL.md only \| behavioral+llm+meta | PARTIAL | 2 | LOW | Meta-Analyzer degraded: \[{'code': 'META_BATCH_PARSE_FAILED', 'message': 'Meta-analysis response was malformed (Ollama Meta did not classify every expected index exactly once); this batch was retained unchanged.', 'first_index': 0, 'last_index': 1, 'finding_count': 2, 'failure_diagnostic': {'outer_error_code': 'META_BATCH_PARSE_FAILED', 'inner_error_code': 'META_CONTRACT_RESPONSE', 'request_sha256': 'b4f2f316c897d45a5b964cbf64f5f5b9ae67f1911f21657f92b1a0344ca2d7c7', 'response_sha256': 'a805a18652463c5bedd8f1675de87a029dc91bf241024aa176b92b125057fdbe', 'repair_attempted': 1, 'repair_succeeded': 0, 'repair_request_sha256': '51e9ec014028e6c9caf6f78cc7ff5f3395aa6918d05068647b60590e12d72e13', 'repair_response_sha256': '0a20094282628b1fb195b4cabf0c405f213ee56e83451c024bb6a58840ba9bac', 'repair_error_code': 'META_CONTRACT_RESPONSE'}}\] |
| Full folder \| behavioral+llm | COMPLETE | 2 | HIGH | exit code 0 |
| Full folder \| behavioral+meta | COMPLETE | 1 | INFO | exit code 0 |
| Full folder \| behavioral+llm+meta | PARTIAL | 2 | LOW | Meta-Analyzer degraded: \[{'code': 'META_BATCH_PARSE_FAILED', 'message': 'Meta-analysis response was malformed (Ollama Meta did not classify every expected index exactly once); this batch was retained unchanged.', 'first_index': 0, 'last_index': 1, 'finding_count': 2, 'failure_diagnostic': {'outer_error_code': 'META_BATCH_PARSE_FAILED', 'inner_error_code': 'META_CONTRACT_RESPONSE', 'request_sha256': '0b57b7d7ef7fa7013e922fccf0f1048e48015699f41c247d5a63168f00c8ab32', 'response_sha256': '4eb932036b970cdf50c19d71b6b9f655769de9d7c5963d968cecc010ee5b723c', 'repair_attempted': 1, 'repair_succeeded': 0, 'repair_request_sha256': '0b7edcd549702899d5885ca165c8a3476ebabeea3aea9510c65593867e7a0595', 'repair_response_sha256': '7532e17ef509d8bdbd372dbd585e41512434a34febe0e10b8128082b36fe1fb4', 'repair_error_code': 'META_CONTRACT_RESPONSE'}}\] |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### LOW · LLM_POLICY_VIOLATION · SKILL.md:
|  | value |
|---|---|
| Validation | Scanner alert, not in the review queue |
| Review ID |  |
| Provisional label |  |
| Final (human) label |  |
| Configurations | SKILL.md only \| behavioral+llm |
| Scan outcomes | complete |
| Cisco category | policy_violation |
| Analyzer | llm |
| Evidence check | unavailable |
| Title | Potential prompt injection in hypothesis ledger protocol |
Evidence snippet:

```text
The skill's instructions define a complex state machine with conditional triggers that could be exploited to bypass security checks or override the agent's behavior.
```
### LOW · LLM_PROMPT_INJECTION · SKILL.md:
|  | value |
|---|---|
| Validation | Scanner alert, not in the review queue |
| Review ID |  |
| Provisional label |  |
| Final (human) label |  |
| Configurations | SKILL.md only \| behavioral+llm+meta; Full folder \| behavioral+llm; Full folder \| behavioral+llm+meta |
| Scan outcomes | partial; complete |
| Cisco category | prompt_injection |
| Analyzer | llm |
| Evidence check | unavailable |
| Title | Potential prompt injection via self-referential instructions |
Evidence snippet:

```text
The skill's instructions describe a mechanism for self-referential behavior that could be used to inject prompts if the agent's security boundaries are bypassed.
```
## Other notes

10 metadata-quality / scan-coverage rows: MANIFEST_MISSING_LICENSE (10).
