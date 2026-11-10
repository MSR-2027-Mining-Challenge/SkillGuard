# Skill `moonshot-teams-runner-b816482cad2c`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | munlucky/moonshot-relay |
| SKILL.md path | skills/moonshot-teams-runner/SKILL.md |
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
| SKILL.md only \| behavioral+llm+meta | PARTIAL | 2 | LOW | Meta-Analyzer degraded: \[{'code': 'META_BATCH_PARSE_FAILED', 'message': 'Meta-analysis response was malformed (Ollama Meta did not classify every expected index exactly once); this batch was retained unchanged.', 'first_index': 0, 'last_index': 1, 'finding_count': 2, 'failure_diagnostic': {'outer_error_code': 'META_BATCH_PARSE_FAILED', 'inner_error_code': 'META_CONTRACT_RESPONSE', 'request_sha256': '413566b0120f933e492b5277d31be4e456b39ac24b10ea5b9e6fcb2f9569146d', 'response_sha256': 'bfa8ca5879eab783471e8c9cb18e579f5d4a81574adc58b2ddd50a5617a04532', 'repair_attempted': 1, 'repair_succeeded': 0, 'repair_request_sha256': '55ba0df31a92a360ba68ffe2d9507a6670181fca248918826de461ea660c352f', 'repair_response_sha256': '377ab47606b6d8777d878411a2f3bf1102ace82d16965038b3c851a4e61cebd2', 'repair_error_code': 'META_CONTRACT_RESPONSE'}}\] |
| Full folder \| behavioral+llm | COMPLETE | 2 | LOW | exit code 0 |
| Full folder \| behavioral+meta | COMPLETE | 1 | INFO | exit code 0 |
| Full folder \| behavioral+llm+meta | PARTIAL | 2 | LOW | Meta-Analyzer degraded: \[{'code': 'META_BATCH_PARSE_FAILED', 'message': 'Meta-analysis response was malformed (Ollama Meta did not classify every expected index exactly once); this batch was retained unchanged.', 'first_index': 0, 'last_index': 1, 'finding_count': 2, 'failure_diagnostic': {'outer_error_code': 'META_BATCH_PARSE_FAILED', 'inner_error_code': 'META_CONTRACT_RESPONSE', 'request_sha256': '07ab5922d52b85f37a5235391a8e52e7d08b3ec6ee31294e39f740693cf856aa', 'response_sha256': '626495ca1b7252e50a2e9bda5255e95c1c87495c92fbfce26ed4a2cd6d739e80', 'repair_attempted': 1, 'repair_succeeded': 0, 'repair_request_sha256': '6b7185216af4e8fc76dff5f117e9edc44033f88c2edac455aaf91778d97492ba', 'repair_response_sha256': '778974b4f36c2279f0b5e3163480bd10ecd38e6a92ebc841fdd283f54f801d25', 'repair_error_code': 'META_CONTRACT_RESPONSE'}}\] |
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
| Title | Potential prompt injection in team configuration |
Evidence snippet:

```text
The skill's team configuration instructions include a pattern for `impl-team` that requires `requirePlanApproval: true` and `fileOwnership: exclusive`.
```
## Other notes

10 metadata-quality / scan-coverage rows: MANIFEST_MISSING_LICENSE (10).
