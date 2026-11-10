# Skill `notion-content-91d9024c9adf`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | MikeCheng1208/BattleTree |
| SKILL.md path | .agents/skills/notion-content/SKILL.md |
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
| SKILL.md only \| behavioral+llm | COMPLETE | 2 | HIGH | exit code 0 |
| SKILL.md only \| behavioral+meta | COMPLETE | 1 | INFO | exit code 0 |
| SKILL.md only \| behavioral+llm+meta | PARTIAL | 2 | HIGH | Meta-Analyzer degraded: \[{'code': 'META_BATCH_PARSE_FAILED', 'message': 'Meta-analysis response was malformed (Ollama Meta did not classify every expected index exactly once); this batch was retained unchanged.', 'first_index': 0, 'last_index': 1, 'finding_count': 2, 'failure_diagnostic': {'outer_error_code': 'META_BATCH_PARSE_FAILED', 'inner_error_code': 'META_CONTRACT_RESPONSE', 'request_sha256': 'af778ebb072395abc95e7d90eeffe71b45dd40cb0eeb7a3f7f3100fd64e66772', 'response_sha256': 'c4a4ecb56d6dab3d1e0e760c456f2192fe269d86f83c8c65b0ee869432c1b1d6', 'repair_attempted': 1, 'repair_succeeded': 0, 'repair_request_sha256': '1f6f4fadbdba3696663c5c8a0f308b675108bfdc308e6611fd503a3be4faee97', 'repair_response_sha256': 'ddc816ef066ef2b3fcce36603e008d6365eb7894376c3356b33fb8f09b2c8ea0', 'repair_error_code': 'META_CONTRACT_RESPONSE'}}\] |
| Full folder \| behavioral+llm | COMPLETE | 2 | HIGH | exit code 0 |
| Full folder \| behavioral+meta | COMPLETE | 1 | INFO | exit code 0 |
| Full folder \| behavioral+llm+meta | PARTIAL | 2 | HIGH | Meta-Analyzer degraded: \[{'code': 'META_BATCH_PARSE_FAILED', 'message': 'Meta-analysis response was malformed (Ollama Meta did not classify every expected index exactly once); this batch was retained unchanged.', 'first_index': 0, 'last_index': 1, 'finding_count': 2, 'failure_diagnostic': {'outer_error_code': 'META_BATCH_PARSE_FAILED', 'inner_error_code': 'META_CONTRACT_RESPONSE', 'request_sha256': '0a9205ee6f37ae89a8118515c5994a051c3389611f2f02e97d14a2be49bee571', 'response_sha256': '4a88e06acbaf63e0a86292288bb05ed322304ecd1595abd09cceaabd90a6fdde', 'repair_attempted': 1, 'repair_succeeded': 0, 'repair_request_sha256': '0f4f991328bf95c5d821e30e4826cc83ef48ce872d7a52a2d5cac7f7f2572c48', 'repair_response_sha256': '5ff052375a359f0e66bd2e929f9b6e88b42b8b9dd18bae060b1fbc7489e50152', 'repair_error_code': 'META_CONTRACT_RESPONSE'}}\] |
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
Skill Name: notion-content
Description: Create content records in Notion database after publishing articles. Use when user provides article title and publishing links (zhihu, weixin, baidu, sohu, toutiao, x.com). Auto-detects platform from URL, fills publish date. Trigger on "/notion-content", "notion记录", "内容入库", or when user says they published an article with links.
```
## Other notes

10 metadata-quality / scan-coverage rows: MANIFEST_MISSING_LICENSE (10).
