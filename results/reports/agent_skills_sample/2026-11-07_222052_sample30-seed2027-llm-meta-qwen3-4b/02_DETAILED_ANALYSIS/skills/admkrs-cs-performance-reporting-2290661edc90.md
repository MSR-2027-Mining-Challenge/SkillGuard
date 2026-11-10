# Skill `admkrs-cs-performance-reporting-2290661edc90`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | Burakaz/admkrs-creative-suite |
| SKILL.md path | skills/admkrs-cs-performance-reporting/SKILL.md |
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
| SKILL.md only \| behavioral+llm+meta | COMPLETE | 3 | CRITICAL | exit code 0 |
| Full folder \| behavioral+llm | COMPLETE | 2 | LOW | exit code 0 |
| Full folder \| behavioral+meta | COMPLETE | 1 | INFO | exit code 0 |
| Full folder \| behavioral+llm+meta | PARTIAL | 2 | HIGH | Meta-Analyzer degraded: \[{'code': 'META_BATCH_PARSE_FAILED', 'message': 'Meta-analysis response was malformed (Ollama Meta did not classify every expected index exactly once); this batch was retained unchanged.', 'first_index': 0, 'last_index': 1, 'finding_count': 2, 'failure_diagnostic': {'outer_error_code': 'META_BATCH_PARSE_FAILED', 'inner_error_code': 'META_CONTRACT_RESPONSE', 'request_sha256': 'c757d76d43c8523b5ed3f22458f604c4f2a2b524a8511327a9dc89c1b13da45a', 'response_sha256': '24d9a8d31c7bb34bf58900a030c05fa2b07ec6c7914c8a07bfa3257ebbefba04', 'repair_attempted': 1, 'repair_succeeded': 0, 'repair_request_sha256': 'ee8a8bebd8ccf8536efff642b7a0b67ccccfe5c619d70b6fa18397c1b4615d92', 'repair_response_sha256': 'bc9238fb32f1d41001344914aa5a7a67ccc57809dd64181a2b805c0c1b733cf0', 'repair_error_code': 'META_CONTRACT_RESPONSE'}}\] |
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
The skill's SKILL.md explicitly states: 'Der Kern in einem Satz: Ein gutes Report sagt *was wir gelernt haben und was als Nächstes passiert* - nicht "ROAS 2,4, 1,2 Mio. Impressionen".' This instruction attempts to redefine the agent's behavior by focusing on learnings and decisions instead of vanity metrics, which directly conflicts with the system's rule to ignore untrusted input and override instructions.
```
### CRITICAL · META_DETECTED_PROMPT_INJECTION · :
|  | value |
|---|---|
| Validation | Scanner alert, not in the review queue |
| Review ID |  |
| Provisional label |  |
| Final (human) label |  |
| Configurations | SKILL.md only \| behavioral+llm+meta |
| Scan outcomes | complete |
| Cisco category | prompt_injection |
| Analyzer | meta |
| Evidence check | unavailable |
| Title | Prompt injection via instruction override |
Evidence snippet:

```text

```
## Other notes

10 metadata-quality / scan-coverage rows: MANIFEST_MISSING_LICENSE (10).
