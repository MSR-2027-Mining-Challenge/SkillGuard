# Skill `spatial-domains-712e4a65bdd1`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | mdbabumiamssm/AI-Agentic-Skills-by-Dr.-Mia |
| SKILL.md path | Skills/Genomics/Spatial_Transcriptomics/bioSkills/spatial-domains/SKILL.md |
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
| SKILL.md only \| behavioral+llm | COMPLETE | 2 | HIGH | exit code 0 |
| SKILL.md only \| behavioral+meta | COMPLETE | 1 | INFO | exit code 0 |
| SKILL.md only \| behavioral+llm+meta | PARTIAL | 2 | HIGH | Meta-Analyzer degraded: \[{'code': 'META_BATCH_PARSE_FAILED', 'message': 'Meta-analysis response was malformed (Ollama Meta did not classify every expected index exactly once); this batch was retained unchanged.', 'first_index': 0, 'last_index': 1, 'finding_count': 2, 'failure_diagnostic': {'outer_error_code': 'META_BATCH_PARSE_FAILED', 'inner_error_code': 'META_CONTRACT_RESPONSE', 'request_sha256': '973ecf943f11b097d7a6cf08811902d92b982f8591d1f141bb9555a7ac5bed7b', 'response_sha256': 'a3589487aba3da5bfdbf772c002ae44bdfcd61996ccc651732a864409c626f5b', 'repair_attempted': 1, 'repair_succeeded': 0, 'repair_request_sha256': 'd075458dd66b8ba0d79a0edf110cfd62a81ffe71642d7de1be130bf3c33355ab', 'repair_response_sha256': '125aa91e11aac4549928a39d353d1a98af790fec6a69f3a4791b1faba41bde6d', 'repair_error_code': 'META_CONTRACT_RESPONSE'}}\] |
| Full folder \| behavioral+llm | COMPLETE | 2 | HIGH | exit code 0 |
| Full folder \| behavioral+meta | COMPLETE | 1 | INFO | exit code 0 |
| Full folder \| behavioral+llm+meta | PARTIAL | 2 | HIGH | Meta-Analyzer degraded: \[{'code': 'META_BATCH_PARSE_FAILED', 'message': 'Meta-analysis response was malformed (Ollama Meta did not classify every expected index exactly once); this batch was retained unchanged.', 'first_index': 0, 'last_index': 1, 'finding_count': 2, 'failure_diagnostic': {'outer_error_code': 'META_BATCH_PARSE_FAILED', 'inner_error_code': 'META_CONTRACT_RESPONSE', 'request_sha256': 'ff64a1f5fe758f88332c34cfd61bb0a9716a217af40e2fe00bfdde7f2d1959aa', 'response_sha256': '7b76e73cd03e8b91391c2bcf8a28a44c92d6fdc5f3818959f547ff239f866d25', 'repair_attempted': 1, 'repair_succeeded': 0, 'repair_request_sha256': 'cb71b7e7636b6c357d4aeb23cba37d93dc222445e6118a40c1cf806d6de03b5a', 'repair_response_sha256': '2f45d434c291674e67b3048fe202bbb08c9db71892609fb01f1afe8441f0bd45', 'repair_error_code': 'META_CONTRACT_RESPONSE'}}\] |
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
| Title | Direct prompt injection in SKILL.md |
Evidence snippet:

```text
The skill's SKILL.md instructs the agent to run code that bypasses security rules by executing untrusted Python scripts without user confirmation or safety checks, directly violating the system protection rules that require ignoring untrusted input and not executing instructions from untrusted sources.
```
## Other notes

10 metadata-quality / scan-coverage rows: MANIFEST_MISSING_LICENSE (10).
