# Skill `csdn-upload-b2c7d2a24d09`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | ricky-theseus/DaisyWriter |
| SKILL.md path | skills/tech/csdn-upload/SKILL.md |
| Sample stratum | scripts |
| Folder complete in GitSkills | True |
| Coverage | complete: every planned configuration produced a COMPLETE scan |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 1 | INFO | exit code 0 |
| SKILL.md only \| behavioral | COMPLETE | 1 | INFO | exit code 0 |
| Full folder \| default | COMPLETE | 4 | LOW | exit code 0 |
| Full folder \| behavioral | COMPLETE | 4 | LOW | exit code 0 |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### LOW · ALLOWED_TOOLS_GLOB_VIOLATION · SKILL.md:
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 6becf0083a |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | unauthorized_tool_use |
| Analyzer | static |
| Evidence check | unavailable |
| Title | Code uses glob/file patterns but Glob tool not in allowed-tools |
Evidence snippet:

```text

```
### LOW · UNDECLARED_NETWORK_DESTINATION · scripts/playwright_uploader.py:187
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | cb0270f5d1 |
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
### LOW · UNDECLARED_NETWORK_DESTINATION · scripts/playwright_uploader.py:205
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 1c7f5294f3 |
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
