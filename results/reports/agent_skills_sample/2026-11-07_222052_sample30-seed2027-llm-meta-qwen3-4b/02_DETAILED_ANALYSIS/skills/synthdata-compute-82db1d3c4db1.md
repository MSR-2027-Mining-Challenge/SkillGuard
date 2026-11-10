# Skill `synthdata-compute-82db1d3c4db1`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | rappdw/synthdata |
| SKILL.md path | skills/synthdata-compute/SKILL.md |
| Sample stratum | scripts |
| Folder complete in GitSkills | True |
| Coverage | partially_complete: some configurations are COMPLETE, others are partial, contract-only or failed |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 1 | INFO | exit code 0 |
| SKILL.md only \| behavioral | COMPLETE | 1 | INFO | exit code 0 |
| Full folder \| default | COMPLETE | 2 | CRITICAL | exit code 0 |
| Full folder \| behavioral | COMPLETE | 2 | CRITICAL | exit code 0 |
| SKILL.md only \| behavioral+llm | COMPLETE | 2 | HIGH | exit code 0 |
| SKILL.md only \| behavioral+meta | COMPLETE | 1 | INFO | exit code 0 |
| SKILL.md only \| behavioral+llm+meta | PARTIAL | 2 | HIGH | Meta-Analyzer degraded: \[{'code': 'META_BATCH_PARSE_FAILED', 'message': 'Meta-analysis response was malformed (Ollama Meta did not classify every expected index exactly once); this batch was retained unchanged.', 'first_index': 0, 'last_index': 1, 'finding_count': 2, 'failure_diagnostic': {'outer_error_code': 'META_BATCH_PARSE_FAILED', 'inner_error_code': 'META_CONTRACT_RESPONSE', 'request_sha256': 'f11c93219760131295ed6c9f7b58a0ff1046f2105550c2ad9fa6f2966d90f865', 'response_sha256': '40f6b28cc0cbd9bbe93cf2c057c84a2082a5315f1824368f11443d57bbb1fa74', 'repair_attempted': 1, 'repair_succeeded': 0, 'repair_request_sha256': 'c1242992652b83b7452f3e27c7a63ed5797bb5c3da12ff793f7e97fd2ca3710c', 'repair_response_sha256': 'e6acadc0da5bbf622bf5a0e0882263a8c0faef80c39b312c5c4a65cdabca3066', 'repair_error_code': 'META_CONTRACT_RESPONSE'}}\] |
| Full folder \| behavioral+llm | COMPLETE | 3 | CRITICAL | exit code 0 |
| Full folder \| behavioral+meta | COMPLETE | 3 | CRITICAL | exit code 0 |
| Full folder \| behavioral+llm+meta | PARTIAL | 3 | CRITICAL | Meta-Analyzer degraded: \[{'code': 'META_BATCH_PARSE_FAILED', 'message': 'Meta-analysis response was malformed (Ollama Meta did not classify every expected index exactly once); this batch was retained unchanged.', 'first_index': 0, 'last_index': 2, 'finding_count': 3, 'failure_diagnostic': {'outer_error_code': 'META_BATCH_PARSE_FAILED', 'inner_error_code': 'META_CONTRACT_RESPONSE', 'request_sha256': 'd57eee9014e2498eec271191ad47d6ca86663caba0d43658fe5364d8b54bea76', 'response_sha256': 'fb75e8a779122248e7557b1f71c3b6c27e6957224c2843a87738cdc242b2f7cf', 'repair_attempted': 1, 'repair_succeeded': 0, 'repair_request_sha256': '87e584f832b54b5e151370f1555cb423c11f8ea7b92fcaf8b02465c6155fbae7', 'repair_response_sha256': 'e3c61d5350c6527792717615348f6eeb14b73f56c3bb6eb6d5744d062d24abc4', 'repair_error_code': 'META_CONTRACT_RESPONSE'}}\] |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### CRITICAL · COMMAND_INJECTION_EVAL · scripts/compute.py:174
|  | value |
|---|---|
| Validation | Scanner alert, not in the review queue |
| Review ID |  |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral; Full folder \| behavioral+llm; Full folder \| behavioral+meta; Full folder \| behavioral+llm+meta |
| Scan outcomes | complete; partial |
| Cisco category | command_injection |
| Analyzer | static |
| Evidence check | exact |
| Title | Dangerous code execution functions that can execute arbitrary code |
Evidence snippet:

```text
exec(code, namespace)
```
### HIGH · LLM_PROMPT_INJECTION · SKILL.md:
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
| Title | Direct prompt injection in skill instructions |
Evidence snippet:

```text
The skill's instructions require the user to provide natural language descriptions of computations, which are then used to generate Python code that is executed by the agent. This allows for direct prompt injection where the user's input can be used to create malicious computation logic that is executed without proper validation.
```
### CRITICAL · LLM_COMMAND_INJECTION · :
|  | value |
|---|---|
| Validation | Scanner alert, not in the review queue |
| Review ID |  |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| behavioral+llm; Full folder \| behavioral+llm+meta |
| Scan outcomes | complete; partial |
| Cisco category | command_injection |
| Analyzer | llm |
| Evidence check | unavailable |
| Title | Command injection via inline Python expressions |
Evidence snippet:

```text
The `--expr` flag accepts inline Python expressions that are executed without validation or sanitization, enabling arbitrary code execution if the user supplies malicious expressions.
```
### CRITICAL · META_DETECTED_UNAUTHORIZED_TOOL_USE · :
|  | value |
|---|---|
| Validation | Scanner alert, not in the review queue |
| Review ID |  |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| behavioral+meta |
| Scan outcomes | complete |
| Cisco category | unauthorized_tool_use |
| Analyzer | meta |
| Evidence check | unavailable |
| Title | Insecure code execution in compute.py |
Evidence snippet:

```text

```
## Other notes

10 metadata-quality / scan-coverage rows: MANIFEST_MISSING_LICENSE (10).
