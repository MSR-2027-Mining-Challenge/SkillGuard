# Skill `skill-24eda454b855`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | LauchnerMedia/nexus-bdr |
| SKILL.md path | SKILL.md |
| Sample stratum | scripts |
| Folder complete in GitSkills | False |
| Coverage | partially_complete: some configurations are COMPLETE, others are partial, contract-only or failed |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 1 | INFO | exit code 0 |
| SKILL.md only \| behavioral | COMPLETE | 1 | INFO | exit code 0 |
| Full folder \| default | SKIPPED_INCOMPLETE_FOLDER |  |  | SKIPPED_INCOMPLETE_FOLDER: GitSkills did not store every file of this folder (missing: 176) |
| Full folder \| behavioral | SKIPPED_INCOMPLETE_FOLDER |  |  | SKIPPED_INCOMPLETE_FOLDER: GitSkills did not store every file of this folder (missing: 176) |
| SKILL.md only \| behavioral+llm | COMPLETE | 2 | HIGH | exit code 0 |
| SKILL.md only \| behavioral+meta | COMPLETE | 1 | INFO | exit code 0 |
| SKILL.md only \| behavioral+llm+meta | PARTIAL | 2 | HIGH | Meta-Analyzer degraded: \[{'code': 'META_BATCH_PARSE_FAILED', 'message': 'Meta-analysis response was malformed (Ollama Meta did not classify every expected index exactly once); this batch was retained unchanged.', 'first_index': 0, 'last_index': 1, 'finding_count': 2, 'failure_diagnostic': {'outer_error_code': 'META_BATCH_PARSE_FAILED', 'inner_error_code': 'META_CONTRACT_RESPONSE', 'request_sha256': 'd259372aa3c2981fea68d60aed4188623e8882347cb34e4c3c8c05c69bcf8ab2', 'response_sha256': 'f9eef845567a7de3eecfe2306073735eaf97274fcd51ef8f50777df69eb814b6', 'repair_attempted': 1, 'repair_succeeded': 0, 'repair_request_sha256': 'c06ade1b8ad591e6d4eda751b0ffed2878de9c7869ee72f20b04f61655562afc', 'repair_response_sha256': 'd1c0a704fbd2061952df43f1f5c322fc8c76fa3fb1cabcf2155ac5e4c5d280af', 'repair_error_code': 'META_CONTRACT_RESPONSE'}}\] |
| Full folder \| behavioral+llm | SKIPPED_INCOMPLETE_FOLDER |  |  | SKIPPED_INCOMPLETE_FOLDER: GitSkills did not store every file of this folder (missing: 176) |
| Full folder \| behavioral+meta | SKIPPED_INCOMPLETE_FOLDER |  |  | SKIPPED_INCOMPLETE_FOLDER: GitSkills did not store every file of this folder (missing: 176) |
| Full folder \| behavioral+llm+meta | SKIPPED_INCOMPLETE_FOLDER |  |  | SKIPPED_INCOMPLETE_FOLDER: GitSkills did not store every file of this folder (missing: 176) |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### HIGH · LLM_PROMPT_INJECTION · SKILL.md:
|  | value |
|---|---|
| Validation | Scanner alert, not in the review queue |
| Review ID |  |
| Provisional label |  |
| Final (human) label |  |
| Configurations | SKILL.md only \| behavioral+llm; SKILL.md only \| behavioral+llm+meta |
| Scan outcomes | complete; partial |
| Cisco category | prompt_injection |
| Analyzer | llm |
| Evidence check | unavailable |
| Title | Direct prompt injection in SKILL.md |
Evidence snippet:

```text
The skill's core workflows (Prospect Discovery, Lead Enrichment, Lead Qualification) require the agent to execute Apollo searches and Hunter enrichment without user approval, directly overriding the 'Never send outreach without user approval' rule.
```
## Other notes

5 metadata-quality / scan-coverage rows: MANIFEST_MISSING_LICENSE (5).
