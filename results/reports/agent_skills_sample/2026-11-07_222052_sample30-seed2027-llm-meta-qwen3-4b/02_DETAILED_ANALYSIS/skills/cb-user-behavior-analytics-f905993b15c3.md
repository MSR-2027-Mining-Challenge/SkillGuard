# Skill `cb-user-behavior-analytics-f905993b15c3`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | at-src/cold-box |
| SKILL.md path | cold-box-room/skills/library/cb-user-behavior-analytics/SKILL.md |
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
| SKILL.md only \| behavioral+llm+meta | PARTIAL | 2 | HIGH | Meta-Analyzer degraded: \[{'code': 'META_BATCH_PARSE_FAILED', 'message': 'Meta-analysis response was malformed (Ollama Meta did not classify every expected index exactly once); this batch was retained unchanged.', 'first_index': 0, 'last_index': 1, 'finding_count': 2, 'failure_diagnostic': {'outer_error_code': 'META_BATCH_PARSE_FAILED', 'inner_error_code': 'META_CONTRACT_RESPONSE', 'request_sha256': 'ed9222851088ec67f13f6929c5fb73051f6df3d74b85909b5671908b15cfad38', 'response_sha256': '5c7d41c55f0a07b233d38f93c51b313e9580bad2c205193add93caca31144356', 'repair_attempted': 1, 'repair_succeeded': 0, 'repair_request_sha256': 'a8344cd230739d288082acfc5a8aa23cd716e5b500bcca7811a09a487ad7e52e', 'repair_response_sha256': 'f2e1838cd5a643d3f0a9d47bae3804a8a6291d8dae39eb89acf9c6e1d4a9b300', 'repair_error_code': 'META_CONTRACT_RESPONSE'}}\] |
| Full folder \| behavioral+llm | COMPLETE | 2 | HIGH | exit code 0 |
| Full folder \| behavioral+meta | COMPLETE | 1 | INFO | exit code 0 |
| Full folder \| behavioral+llm+meta | PARTIAL | 3 | HIGH | Meta-Analyzer degraded: \[{'code': 'META_BATCH_PARSE_FAILED', 'message': 'Meta-analysis response was malformed (Ollama Meta did not classify every expected index exactly once); this batch was retained unchanged.', 'first_index': 0, 'last_index': 2, 'finding_count': 3, 'failure_diagnostic': {'outer_error_code': 'META_BATCH_PARSE_FAILED', 'inner_error_code': 'META_CONTRACT_RESPONSE', 'request_sha256': 'c8b3fabd991695fb57d536ef2276930a423a181f72930ddf0aa83960e33765f9', 'response_sha256': 'da4e769c54b31f6538271ee4d743c981247399a9ac370145e6d14c7c592848e6', 'repair_attempted': 1, 'repair_succeeded': 0, 'repair_request_sha256': 'bc991331dd1eec071b66023ee49da7045c991135b318427aafe83e339326df12', 'repair_response_sha256': '06b806036c3b73cceb41feeebd0c3464d71b55c2583159b9d11376e200c70660', 'repair_error_code': 'META_CONTRACT_RESPONSE'}}\] |
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
The skill's instruction body requires logging the playbook with `CB-SKL-339` in the case journal when adopting it, which is a direct instruction to override the agent's behavior without user confirmation.
```
## Other notes

10 metadata-quality / scan-coverage rows: MANIFEST_MISSING_LICENSE (10).
