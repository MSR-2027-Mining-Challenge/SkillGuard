# Skill `slide-style-65f218b6102e`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | HaykTarkhanyan/python_math_ml_course |
| SKILL.md path | .claude/skills/slide-style/SKILL.md |
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
| SKILL.md only \| behavioral+llm+meta | COMPLETE | 2 | LOW | exit code 0 |
| Full folder \| behavioral+llm | COMPLETE | 2 | LOW | exit code 0 |
| Full folder \| behavioral+meta | COMPLETE | 1 | INFO | exit code 0 |
| Full folder \| behavioral+llm+meta | PARTIAL | 2 | LOW | Meta-Analyzer degraded: \[{'code': 'META_BATCH_PARSE_FAILED', 'message': 'Meta-analysis response was malformed (Ollama Meta did not classify every expected index exactly once); this batch was retained unchanged.', 'first_index': 0, 'last_index': 1, 'finding_count': 2, 'failure_diagnostic': {'outer_error_code': 'META_BATCH_PARSE_FAILED', 'inner_error_code': 'META_CONTRACT_RESPONSE', 'request_sha256': 'add07aae825a829997c9379bb1a69d63b0784a206dd1453d09e439808376cfb7', 'response_sha256': '7e379127cc2d857bf54d297d195d7052d7ea7337e2d12baf052c9ac79784fd7e', 'repair_attempted': 1, 'repair_succeeded': 0, 'repair_request_sha256': '83fac522b97371188b1e034fac65a08ce32ddee849f0760a02952d78387cf701', 'repair_response_sha256': '9389cce57bb7301b3e64082b588393edb22787139905974d3ed171eb7ea2b3d5', 'repair_error_code': 'META_CONTRACT_RESPONSE'}}\] |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### LOW · LLM_POLICY_VIOLATION · :
|  | value |
|---|---|
| Validation | Scanner alert, not in the review queue |
| Review ID |  |
| Provisional label |  |
| Final (human) label |  |
| Configurations | SKILL.md only \| behavioral+llm; Full folder \| behavioral+llm; Full folder \| behavioral+llm+meta |
| Scan outcomes | complete; partial |
| Cisco category | policy_violation |
| Analyzer | llm |
| Evidence check | unavailable |
| Title | Policy violation: Missing license declaration |
Evidence snippet:

```text
YAML Manifest Details [evidence_id=SRC:bd43a7da36c1cfe1]: - name: slide-style ... - license: Not specified ...
```
### LOW · LLM_POLICY_VIOLATION · SKILL.md:
|  | value |
|---|---|
| Validation | Scanner alert, not in the review queue |
| Review ID |  |
| Provisional label |  |
| Final (human) label |  |
| Configurations | SKILL.md only \| behavioral+llm+meta |
| Scan outcomes | complete |
| Cisco category | policy_violation |
| Analyzer | llm |
| Evidence check | unavailable |
| Title | Potential prompt injection in skill instructions |
Evidence snippet:

```text
First action: read `ml/SLIDE_STYLE.md` and follow it. That file is the single source of truth; this skill is just the trigger.
```
## Other notes

10 metadata-quality / scan-coverage rows: MANIFEST_MISSING_LICENSE (10).
