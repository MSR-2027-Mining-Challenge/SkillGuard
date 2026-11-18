# Skill `detecting-golden-ticket-forgery-0b384ff76feb`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | Molly-agi/Molly-Core |
| SKILL.md path | src/skills/registry/skills/cybersecurity/skills/detecting-golden-ticket-forgery/SKILL.md |
| Sample stratum | scripts |
| Folder complete in GitSkills | True |
| Coverage | complete: every planned configuration produced a COMPLETE scan |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 0 | SAFE | exit code 0 |
| SKILL.md only \| behavioral | COMPLETE | 0 | SAFE | exit code 0 |
| Full folder \| default | COMPLETE | 1 | LOW | exit code 0 |
| Full folder \| behavioral | COMPLETE | 1 | LOW | exit code 0 |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### LOW · UNDECLARED_NETWORK_DESTINATION · scripts/agent.py:15
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | e4e2d7eb2b |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | unauthorized_tool_use |
| Analyzer | static |
| Evidence check | unavailable |
| Title | Script contacts a destination the documentation never mentions |
Evidence snippet:

```text

```
## Other notes

0 metadata-quality / scan-coverage rows: .
