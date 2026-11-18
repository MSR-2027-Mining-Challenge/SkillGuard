# Skill `ios-release-pipeline-48b2472211a7`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | viktart/claude-skills |
| SKILL.md path | ios-release-pipeline/skill.md |
| Sample stratum | scripts |
| Folder complete in GitSkills | False |
| Coverage | complete: every planned configuration produced a COMPLETE scan |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 1 | INFO | exit code 0 |
| SKILL.md only \| behavioral | COMPLETE | 1 | INFO | exit code 0 |
| Full folder \| default | COMPLETE | 3 | MEDIUM | exit code 0 |
| Full folder \| behavioral | COMPLETE | 3 | MEDIUM | exit code 0 |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### MEDIUM · SECRET_PASSWORD_VAR · scripts/collect-secrets.sh:38
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 0e96a4bdfd |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | hardcoded_secrets |
| Analyzer | static |
| Evidence check | exact |
| Title | Hardcoded password or secret in variable |
Evidence snippet:

```text
match_pass****
```
### LOW · UNDECLARED_NETWORK_DESTINATION · scripts/collect-secrets.sh:46
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 60c99ff1b0 |
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
