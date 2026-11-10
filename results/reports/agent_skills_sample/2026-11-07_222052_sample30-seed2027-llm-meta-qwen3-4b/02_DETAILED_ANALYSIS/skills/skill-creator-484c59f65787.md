# Skill `skill-creator-484c59f65787`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | niekbeckers/skills |
| SKILL.md path | skills/skill-creator/SKILL.md |
| Sample stratum | scripts |
| Folder complete in GitSkills | True |
| Coverage | partially_complete: some configurations are COMPLETE, others are partial, contract-only or failed |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 1 | INFO | exit code 0 |
| SKILL.md only \| behavioral | COMPLETE | 1 | INFO | exit code 0 |
| Full folder \| default | COMPLETE | 3 | CRITICAL | exit code 0 |
| Full folder \| behavioral | COMPLETE | 3 | CRITICAL | exit code 0 |
| SKILL.md only \| behavioral+llm | COMPLETE | 2 | HIGH | exit code 0 |
| SKILL.md only \| behavioral+meta | COMPLETE | 1 | INFO | exit code 0 |
| SKILL.md only \| behavioral+llm+meta | PARTIAL | 2 | LOW | Meta-Analyzer degraded: \[{'code': 'META_BATCH_PARSE_FAILED', 'message': 'Meta-analysis response was malformed (NONE_SUPPORTED conflicts with a substantive Meta delta); this batch was retained unchanged.', 'first_index': 0, 'last_index': 1, 'finding_count': 2, 'failure_diagnostic': {'outer_error_code': 'META_BATCH_PARSE_FAILED', 'inner_error_code': 'META_CONTRACT_DELTA_CONSISTENCY', 'request_sha256': '00b63c6c01d4b28fa7e44f202390fa613d16849aa147e5c8d24510b205db4fa3', 'response_sha256': '094dd0c80269082c954095630761d928e81ec1b4b9a338da5fcf58efcc9f53ba', 'repair_attempted': 1, 'repair_succeeded': 0, 'repair_request_sha256': 'e4388ea50638bf6198a30cf34c87b9fa5ea6c013cc2b6909f42a50c9c7079812', 'repair_response_sha256': 'f0faa965728f8d95d71738e5722a318f34c5c44ae4c9078e7b88df33d34ca29e', 'repair_error_code': 'META_CONTRACT_DELTA_CONSISTENCY'}}\] |
| Full folder \| behavioral+llm | PARTIAL | 10 | CRITICAL | Cisco reported an analyzer failure (llm_analyzer: litellm.Timeout: OllamaException - litellm.Timeout: Connection timed out. Timeout passed=120.0, time taken=120.018 seconds); the LLM analyzer could not review the skill (LLM_ANALYSIS_FAILED) |
| Full folder \| behavioral+meta | PARTIAL | 3 | CRITICAL | Meta-Analyzer degraded: \[{'code': 'META_BATCH_PARSE_FAILED', 'message': 'Meta-analysis response was malformed (Ollama Meta did not classify every expected index exactly once); this batch was retained unchanged.', 'first_index': 0, 'last_index': 2, 'finding_count': 3, 'failure_diagnostic': {'outer_error_code': 'META_BATCH_PARSE_FAILED', 'inner_error_code': 'META_CONTRACT_RESPONSE', 'request_sha256': '659e985715f577839776659fa61d1df1310304cf15cc8bc0a6dd670ab4d038bd', 'response_sha256': 'c8e437053b9d612d1846856f46930955dcc68d6301316fd6b00a213653f7b53c', 'repair_attempted': 1, 'repair_succeeded': 0, 'repair_request_sha256': 'e652e3ea1ab5607d3fb378fc1315aa56c2c85fa1f700440841a5778ce82d47e2', 'repair_response_sha256': 'ad172d1025c12c81a44199515da8218dd42a9294716fb45c36448ee50854d16c', 'repair_error_code': 'META_CONTRACT_RESPONSE'}}\] |
| Full folder \| behavioral+llm+meta | PARTIAL | 10 | CRITICAL | Cisco reported an analyzer failure (llm_analyzer: litellm.Timeout: OllamaException - litellm.Timeout: Connection timed out. Timeout passed=120.0, time taken=120.014 seconds); the LLM analyzer could not review the skill (LLM_ANALYSIS_FAILED); Meta-Analyzer degraded: \[{'code': 'META_BATCH_PARSE_FAILED', 'message': 'Meta-analysis response was malformed (Ollama Meta did not classify every expected index exactly once); this batch was retained unchanged.', 'first_index': 0, 'last_index': 9, 'finding_count': 10, 'failure_diagnostic': {'outer_error_code': 'META_BATCH_PARSE_FAILED', 'inner_error_code': 'META_CONTRACT_RESPONSE', 'request_sha256': 'e07d68c8c9eeeeaf6711b6a577a16271d374e752df92e61bf9ee2588296f8565', 'response_sha256': '74bfea1933d13966a832451ab1862d03c18497a44e306374ca75210f73c45e1f', 'repair_attempted': 1, 'repair_succeeded': 0, 'repair_request_sha256': 'e8d788aafd881adcbc62bcfcce279ef2470c0c45ee4eb54527aad4edbe01f308', 'repair_response_sha256': '18d8a504394712f839ff68de9166ad84abac029dbe2b71348c9c0269281626e3', 'repair_error_code': 'META_CONTRACT_RESPONSE'}}\] |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### CRITICAL · COMMAND_INJECTION_OS_SYSTEM · eval-viewer/generate_review.py:390
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
| Title | Shell command execution with string formatting (potential injection) |
Evidence snippet:

```text
result = subprocess.run(
```
### MEDIUM · FILE_MAGIC_MISMATCH · scripts/__init__.py:
|  | value |
|---|---|
| Validation | Scanner alert, not in the review queue |
| Review ID |  |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral; Full folder \| behavioral+llm; Full folder \| behavioral+meta; Full folder \| behavioral+llm+meta |
| Scan outcomes | complete; partial |
| Cisco category | obfuscation |
| Analyzer | static |
| Evidence check | unavailable |
| Title | File extension does not match actual content type |
Evidence snippet:

```text

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
| Title | Skill Creator enables prompt injection via instruction override |
Evidence snippet:

```text
The skill creator skill explicitly instructs the agent to skip formal evaluation when user says 'just vibe with me' (SKILL.md: 'Be flexible — if the user says "just vibe with me", skip the formal evaluation.')
```
## Other notes

24 metadata-quality / scan-coverage rows: LLM_CONTEXT_BUDGET_EXCEEDED (12), MANIFEST_MISSING_LICENSE (10), LLM_ANALYSIS_FAILED (2).
