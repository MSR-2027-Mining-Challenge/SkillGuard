# Skill `scientific-reactome-pathways-b24c9a2b5a6b`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | nahisaho/satori |
| SKILL.md path | src/.github/skills/scientific-reactome-pathways/SKILL.md |
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
| SKILL.md only \| behavioral+llm | COMPLETE | 2 | LOW | exit code 0 |
| SKILL.md only \| behavioral+meta | COMPLETE | 1 | INFO | exit code 0 |
| SKILL.md only \| behavioral+llm+meta | PARTIAL | 2 | HIGH | Meta-Analyzer degraded: \[{'code': 'META_BATCH_PARSE_FAILED', 'message': 'Meta-analysis response was malformed (Ollama Meta did not classify every expected index exactly once); this batch was retained unchanged.', 'first_index': 0, 'last_index': 1, 'finding_count': 2, 'failure_diagnostic': {'outer_error_code': 'META_BATCH_PARSE_FAILED', 'inner_error_code': 'META_CONTRACT_RESPONSE', 'request_sha256': '73629c47e13fe5c755d2185cf07b541d8e9baff661e4d1a4a4be187c306b2cb6', 'response_sha256': '6b78426e84bfe8cc3ca7348331bed5c3001da36570f8ddcfd35196265b4fbfe8', 'repair_attempted': 1, 'repair_succeeded': 0, 'repair_request_sha256': '2268bbb860e1d19266f2c00726ddb6a353608dc28a7bb78614c6ce2f19161d9b', 'repair_response_sha256': '7f91636c7b7f3d286c607a73922fd5f3db5c27974aa5848c9012e5ee0634a7ba', 'repair_error_code': 'META_CONTRACT_RESPONSE'}}\] |
| Full folder \| behavioral+llm | COMPLETE | 2 | HIGH | exit code 0 |
| Full folder \| behavioral+meta | COMPLETE | 1 | INFO | exit code 0 |
| Full folder \| behavioral+llm+meta | PARTIAL | 2 | HIGH | Meta-Analyzer degraded: \[{'code': 'META_BATCH_PARSE_FAILED', 'message': 'Meta-analysis response was malformed (Ollama Meta did not classify every expected index exactly once); this batch was retained unchanged.', 'first_index': 0, 'last_index': 1, 'finding_count': 2, 'failure_diagnostic': {'outer_error_code': 'META_BATCH_PARSE_FAILED', 'inner_error_code': 'META_CONTRACT_RESPONSE', 'request_sha256': 'c09d806b20515de7db65f599a3d4ab9f35bb45743511116f2ab238bcffe370fd', 'response_sha256': '12d34dcb0a76f3181a6f1146173f838b6d09b36173d2b35622bc6b86ba4b639b', 'repair_attempted': 1, 'repair_succeeded': 0, 'repair_request_sha256': '1b1a171ec3319af8b69399b41950af31eb8a2499589f0933e700c993cff5066f', 'repair_response_sha256': '3712a2dce4ec0c33055d3704ac75274c67ea7cc4489ee08f752ccdabb669ab68', 'repair_error_code': 'META_CONTRACT_RESPONSE'}}\] |
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
| Title | Potential prompt injection in SKILL.md |
Evidence snippet:

```text
The SKILL.md file describes a skill that uses the Reactome API to search for pathways, map UniProt IDs to pathways, and retrieve pathway participants. The skill's instructions include code examples that accept user input (query_or_uniprot) without validation, which could allow for prompt injection if the input is not properly sanitized.
```
## Other notes

10 metadata-quality / scan-coverage rows: MANIFEST_MISSING_LICENSE (10).
