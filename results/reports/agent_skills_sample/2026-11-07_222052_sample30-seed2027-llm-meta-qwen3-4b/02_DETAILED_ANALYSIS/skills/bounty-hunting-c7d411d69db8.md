# Skill `bounty-hunting-c7d411d69db8`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | richard-devbot/SDLC-rstack |
| SKILL.md path | skills/bounty-hunting/SKILL.md |
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
| SKILL.md only \| behavioral+llm+meta | PARTIAL | 2 | LOW | Meta-Analyzer degraded: \[{'code': 'META_BATCH_PARSE_FAILED', 'message': 'Meta-analysis response was malformed (NONE_SUPPORTED conflicts with a substantive Meta delta); this batch was retained unchanged.', 'first_index': 0, 'last_index': 1, 'finding_count': 2, 'failure_diagnostic': {'outer_error_code': 'META_BATCH_PARSE_FAILED', 'inner_error_code': 'META_CONTRACT_DELTA_CONSISTENCY', 'request_sha256': 'f3a2289f9b31d398444f5f7c9ce9485f5c38c2eade7f0e78af03ccdaaf40fb31', 'response_sha256': '6b38639b2530f6f75f493d7150d1164d4022a635477ed8833337a32d4c36c66f', 'repair_attempted': 1, 'repair_succeeded': 0, 'repair_request_sha256': '9f2203de54106ab5e94cb665d3baa6fdbd4bb887f81445ffa149f4d0a1a1ada7', 'repair_response_sha256': '5a9472ab47dcd4589f606ee932d59f87ab335fa2b384165bd606e09339052113', 'repair_error_code': 'META_CONTRACT_RESPONSE'}}\] |
| Full folder \| behavioral+llm | COMPLETE | 2 | HIGH | exit code 0 |
| Full folder \| behavioral+meta | COMPLETE | 1 | INFO | exit code 0 |
| Full folder \| behavioral+llm+meta | PARTIAL | 2 | HIGH | Meta-Analyzer degraded: \[{'code': 'META_BATCH_PARSE_FAILED', 'message': 'Meta-analysis response was malformed (Ollama Meta did not classify every expected index exactly once); this batch was retained unchanged.', 'first_index': 0, 'last_index': 1, 'finding_count': 2, 'failure_diagnostic': {'outer_error_code': 'META_BATCH_PARSE_FAILED', 'inner_error_code': 'META_CONTRACT_RESPONSE', 'request_sha256': '491f098551b5cf8b39d31fcd241cd6de0a79a6ec226aa000b2b4fc429bf46212', 'response_sha256': '6e50075e35bedd3d0f5568a054e57ece929979dd07a7d3b764f2aa87b93ddef4', 'repair_attempted': 1, 'repair_succeeded': 0, 'repair_request_sha256': 'e5774f05af6747d3f325815d51f91bf810c7c24b8cc1ba84127b061058d71946', 'repair_response_sha256': '0328586afe7f4b657d801df8c972365d25243e8b549aed6a53037c70caa0d4a4', 'repair_error_code': 'META_CONTRACT_RESPONSE'}}\] |
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
| Title | Potential prompt injection via REPO_MODE override |
Evidence snippet:

```text
If `REPO_MODE` is `solo`: you own everything. Fix issues proactively without asking. If `REPO_MODE` is `collaborative`: flag via AskUserQuestion before fixing anything owned by others. If `REPO_MODE` is `unknown`: treat as collaborative.
```
## Other notes

10 metadata-quality / scan-coverage rows: MANIFEST_MISSING_LICENSE (10).
