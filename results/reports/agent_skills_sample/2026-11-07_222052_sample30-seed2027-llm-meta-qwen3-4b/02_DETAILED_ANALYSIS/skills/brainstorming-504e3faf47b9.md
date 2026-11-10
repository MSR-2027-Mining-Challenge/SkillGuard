# Skill `brainstorming-504e3faf47b9`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | jbro/pi-agent |
| SKILL.md path | skills/superpowers/brainstorming/SKILL.md |
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
| SKILL.md only \| behavioral+llm+meta | PARTIAL | 2 | LOW | Meta-Analyzer degraded: \[{'code': 'META_BATCH_PARSE_FAILED', 'message': 'Meta-analysis response was malformed (NONE_SUPPORTED conflicts with a substantive Meta delta); this batch was retained unchanged.', 'first_index': 0, 'last_index': 1, 'finding_count': 2, 'failure_diagnostic': {'outer_error_code': 'META_BATCH_PARSE_FAILED', 'inner_error_code': 'META_CONTRACT_DELTA_CONSISTENCY', 'request_sha256': '4818dedb38a8645e7f8be5c03b5d85b333ecdab8bc461f821fb74d9764d394d1', 'response_sha256': '37e27dc74431e01b49596da873b90894f872ef5d9c1db827b0f9eea7b3a1ce99', 'repair_attempted': 1, 'repair_succeeded': 0, 'repair_request_sha256': '82c5daaebfc626c67ff1bb37ff1eb68e1f5de3081003cf6e7bbdd21e57e39ed3', 'repair_response_sha256': '471f4bfd40fcc0ebea7c61c5cbec431cbf63938e781f53e50942ba8b10140451', 'repair_error_code': 'META_CONTRACT_RESPONSE'}}\] |
| Full folder \| behavioral+llm | COMPLETE | 2 | LOW | exit code 0 |
| Full folder \| behavioral+meta | COMPLETE | 1 | INFO | exit code 0 |
| Full folder \| behavioral+llm+meta | COMPLETE | 2 | LOW | exit code 0 |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### LOW · LLM_POLICY_VIOLATION · SKILL.md:
|  | value |
|---|---|
| Validation | Scanner alert, not in the review queue |
| Review ID |  |
| Provisional label |  |
| Final (human) label |  |
| Configurations | SKILL.md only \| behavioral+llm; SKILL.md only \| behavioral+llm+meta |
| Scan outcomes | complete; partial |
| Cisco category | policy_violation |
| Analyzer | llm |
| Evidence check | unavailable |
| Title | Policy violation: Hard-coded instruction override |
Evidence snippet:

```text
The skill's HARD-GATE states: Do NOT invoke any implementation skill... until you have presented a design and the user has approved it. However, the process flow diagram shows a direct transition to 'Invoke writing-plans skill' after design doc writing without explicit user approval check
```
### LOW · LLM_POLICY_VIOLATION · :
|  | value |
|---|---|
| Validation | Scanner alert, not in the review queue |
| Review ID |  |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| behavioral+llm; Full folder \| behavioral+llm+meta |
| Scan outcomes | complete |
| Cisco category | policy_violation |
| Analyzer | llm |
| Evidence check | unavailable |
| Title | Policy violation: Missing license declaration |
Evidence snippet:

```text
YAML Manifest Details [evidence_id=SRC:bd43a7da36c1cfe1]: - name: brainstorming - description: Use before any creative work — creating features, building components, adding functionality, or modifying behavior — to explore intent, requirements, and design before implementation begins. - license: Not specified - compatibility: Not specified - allowed-tools: Not specified
```
## Other notes

10 metadata-quality / scan-coverage rows: MANIFEST_MISSING_LICENSE (10).
