# Skill `mobile-platform-guardian-3e3ce17e3392`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | traorecheikh/mobile-platform-guardian |
| SKILL.md path | skills/mobile-platform-guardian/SKILL.md |
| Sample stratum | scripts |
| Folder complete in GitSkills | True |
| Coverage | complete: every planned configuration produced a COMPLETE scan |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 0 | SAFE | exit code 0 |
| SKILL.md only \| behavioral | COMPLETE | 0 | SAFE | exit code 0 |
| Full folder \| default | COMPLETE | 2 | CRITICAL | exit code 0 |
| Full folder \| behavioral | COMPLETE | 2 | CRITICAL | exit code 0 |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### CRITICAL · COMMAND_INJECTION_OS_SYSTEM · scripts/guardian.py:384
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | ef8dafbba1 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | command_injection |
| Analyzer | static |
| Evidence check | exact |
| Title | Shell command execution with string formatting (potential injection) |
Evidence snippet:

```text
proc = subprocess.run(
```
### LOW · UNDECLARED_NETWORK_DESTINATION · scripts/guardian.py:1054
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 6501c8bc15 |
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
