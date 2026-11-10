# Skill `product-interviewer-888617f63ea3`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | joleques/northstar-ai |
| SKILL.md path | .codex/skills/product-interviewer/SKILL.md |
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
| SKILL.md only \| behavioral+llm | COMPLETE | 2 | HIGH | exit code 0 |
| SKILL.md only \| behavioral+meta | COMPLETE | 1 | INFO | exit code 0 |
| SKILL.md only \| behavioral+llm+meta | PARTIAL | 2 | HIGH | Meta-Analyzer degraded: \[{'code': 'META_BATCH_PARSE_FAILED', 'message': 'Meta-analysis response was malformed (Ollama Meta did not classify every expected index exactly once); this batch was retained unchanged.', 'first_index': 0, 'last_index': 1, 'finding_count': 2, 'failure_diagnostic': {'outer_error_code': 'META_BATCH_PARSE_FAILED', 'inner_error_code': 'META_CONTRACT_RESPONSE', 'request_sha256': '964a6c7671872aba177856b1fec1622c8d9e6d452b96336d68195e1e8897888a', 'response_sha256': 'b4c0c4fee8b733dd96d84061e85230efed73dfcea655defd0596b1f58aaa20ba', 'repair_attempted': 1, 'repair_succeeded': 0, 'repair_request_sha256': '3e658df53fcf65f594829a866fff9a5daa4796e4ca77742eb42b7e1a6643500c', 'repair_response_sha256': '293e04c4949887ee54577d487345cb4965ace8ce9555e8da2c8650644a1e43a5', 'repair_error_code': 'META_CONTRACT_DELTA_CONSISTENCY'}}\] |
| Full folder \| behavioral+llm | COMPLETE | 2 | HIGH | exit code 0 |
| Full folder \| behavioral+meta | COMPLETE | 1 | INFO | exit code 0 |
| Full folder \| behavioral+llm+meta | PARTIAL | 2 | LOW | Meta-Analyzer degraded: \[{'code': 'META_BATCH_PARSE_FAILED', 'message': 'Meta-analysis response was malformed (NONE_SUPPORTED conflicts with a substantive Meta delta); this batch was retained unchanged.', 'first_index': 0, 'last_index': 1, 'finding_count': 2, 'failure_diagnostic': {'outer_error_code': 'META_BATCH_PARSE_FAILED', 'inner_error_code': 'META_CONTRACT_DELTA_CONSISTENCY', 'request_sha256': 'c38c1ff66e231c2bb3a56f9863f5424e2574206d06a49790d45b0e041dd1f95d', 'response_sha256': 'c7ce8ac02f0f11673ea5caf638feaa158732323c78f3a1a7272e858363a3ae45', 'repair_attempted': 1, 'repair_succeeded': 0, 'repair_request_sha256': 'c2bad3a42a04f19d721a37e0b770d3e8771e30652b04ad4468f02fdabffb1670', 'repair_response_sha256': '0ffbb03fea5fbe617966035d34425478b56df7c5b067b5e0396e4cdbf698863e', 'repair_error_code': 'META_CONTRACT_RESPONSE'}}\] |
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
| Title | Regra Inviolável: NUNCA supõe, NUNCA acha, NUNCA inventa |
Evidence snippet:

```text
Regra Inviolável: Esta skill **NUNCA supõe, NUNCA acha, NUNCA inventa informações.** Absolutamente TUDO deve ter sido dito explicitamente pelo usuário. Se falta informação, **PERGUNTE** — jamais preencha lacunas por conta própria. Qualquer inferência ou "achismo" invalida o artefato produzido.
```
## Other notes

10 metadata-quality / scan-coverage rows: MANIFEST_MISSING_LICENSE (10).
