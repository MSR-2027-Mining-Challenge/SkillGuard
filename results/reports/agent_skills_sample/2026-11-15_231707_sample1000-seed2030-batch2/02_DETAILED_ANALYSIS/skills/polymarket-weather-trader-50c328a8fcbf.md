# Skill `polymarket-weather-trader-50c328a8fcbf`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | LJT-520/openClaw-backup |
| SKILL.md path | skills/adlai88/polymarket-weather-trader/SKILL.md |
| Sample stratum | scripts |
| Folder complete in GitSkills | False |
| Coverage | complete: every planned configuration produced a COMPLETE scan |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 1 | INFO | exit code 0 |
| SKILL.md only \| behavioral | COMPLETE | 1 | INFO | exit code 0 |
| Full folder \| default | COMPLETE | 6 | HIGH | exit code 0 |
| Full folder \| behavioral | COMPLETE | 6 | HIGH | exit code 0 |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### MEDIUM · SOCIAL_ENG_MISLEADING_DESC · SKILL.md:
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | bffff90e41 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | social_engineering |
| Analyzer | static |
| Evidence check | unavailable |
| Title | Potential description-behavior mismatch |
Evidence snippet:

```text

```
### MEDIUM · TOOL_ABUSE_UNDECLARED_NETWORK · SKILL.md:
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 2ea3dd9e76 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | unauthorized_tool_use |
| Analyzer | static |
| Evidence check | unavailable |
| Title | Undeclared network usage |
Evidence snippet:

```text

```
### HIGH · CORRELATED_SENSITIVE_NETWORK_FLOW · scripts/status.py:32
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | d9ea1c6964 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | data_exfiltration |
| Analyzer | correlation |
| Evidence check | unavailable |
| Title | Sensitive source reaches a network sink |
Evidence snippet:

```text

```
### LOW · UNDECLARED_NETWORK_DESTINATION · weather_trader.py:65
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 3e2c262be3 |
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
### LOW · UNDECLARED_NETWORK_DESTINATION · weather_trader.py:514
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 74557b32c9 |
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

4 metadata-quality / scan-coverage rows: MANIFEST_MISSING_LICENSE (4).
