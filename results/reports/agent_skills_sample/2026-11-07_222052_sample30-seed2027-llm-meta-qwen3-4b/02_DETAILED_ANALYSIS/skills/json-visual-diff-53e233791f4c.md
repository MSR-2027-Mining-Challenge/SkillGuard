# Skill `json-visual-diff-53e233791f4c`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | doghelWang/amr_studio_v4 |
| SKILL.md path | skills/json-visual-diff/json-visual-diff/SKILL.md |
| Sample stratum | scripts |
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
| Full folder \| behavioral+llm | COMPLETE | 2 | LOW | exit code 0 |
| Full folder \| behavioral+meta | COMPLETE | 1 | INFO | exit code 0 |
| Full folder \| behavioral+llm+meta | PARTIAL | 2 | LOW | Meta-Analyzer degraded: \[{'code': 'META_BATCH_PARSE_FAILED', 'message': 'Meta-analysis response was malformed (Ollama Meta did not classify every expected index exactly once); this batch was retained unchanged.', 'first_index': 0, 'last_index': 1, 'finding_count': 2, 'failure_diagnostic': {'outer_error_code': 'META_BATCH_PARSE_FAILED', 'inner_error_code': 'META_CONTRACT_RESPONSE', 'request_sha256': '96b067dc958c05c1df8ba99ef827b0d78829f78ddb67591dbd7c018510da6049', 'response_sha256': '62296dd57331912dd619da99298be3b47351ec3d8ece453fc72e5f338fc6d4fd', 'repair_attempted': 1, 'repair_succeeded': 0, 'repair_request_sha256': '244d484c672b2e60eadd6eda72df46cea2598b7317f7a24b68b31ba3dd020ebd', 'repair_response_sha256': '686f94a8a0bef9dce65e24703a8949f1ec03535197c0143db240b7beba960f90', 'repair_error_code': 'META_CONTRACT_DELTA_CONSISTENCY'}}\] |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### LOW · LLM_POLICY_VIOLATION · :
|  | value |
|---|---|
| Validation | Scanner alert, not in the review queue |
| Review ID |  |
| Provisional label |  |
| Final (human) label |  |
| Configurations | SKILL.md only \| behavioral+llm; SKILL.md only \| behavioral+llm+meta; Full folder \| behavioral+llm |
| Scan outcomes | complete |
| Cisco category | policy_violation |
| Analyzer | llm |
| Evidence check | unavailable |
| Title | Policy violation: Missing license specification |
Evidence snippet:

```text
YAML Manifest Details [evidence_id=SRC:bd43a7da36c1cfe1]: - name: json-visual-diff - description: Visually compares two JSON files (e.g. compdesc.json) and requires manual confirmation from the user. Use when the user wants to see a visual diff of two JSON files and explicitly confirm the changes. - license: Not specified - compatibility: Not specified - allowed-tools: Not specified
```
### LOW · LLM_PROMPT_INJECTION · SKILL.md:
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
| Title | Potential prompt injection via manual confirmation step |
Evidence snippet:

```text
The skill requires manual confirmation using `ask_user` tool before proceeding with actions. This creates a potential prompt injection vector if the user is tricked into confirming malicious changes.
```
## Other notes

10 metadata-quality / scan-coverage rows: MANIFEST_MISSING_LICENSE (10).
