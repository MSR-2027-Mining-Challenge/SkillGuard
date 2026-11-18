# Skill `github-copilot-pr-comments-d9446ad758d3`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | AdaskoTheBeAsT/AdaskoTheBeAsT.Interop |
| SKILL.md path | .factory/skills/github-copilot-pr-comments/SKILL.md |
| Sample stratum | skill_md_only |
| Folder complete in GitSkills | True |
| Coverage | complete: every planned configuration produced a COMPLETE scan |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 3 | HIGH | exit code 0 |
| SKILL.md only \| behavioral | COMPLETE | 3 | HIGH | exit code 0 |
| Full folder \| default | COMPLETE | 3 | HIGH | exit code 0 |
| Full folder \| behavioral | COMPLETE | 3 | HIGH | exit code 0 |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### HIGH · CORRELATED_SENSITIVE_NETWORK_FLOW · SKILL.md:125
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 190afee1ea |
| Provisional label |  |
| Final (human) label |  |
| Configurations | SKILL.md only \| default; SKILL.md only \| behavioral; Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | data_exfiltration |
| Analyzer | correlation |
| Evidence check | unavailable |
| Title | Sensitive source reaches a network sink |
Evidence snippet:

```text

```
### HIGH · CORRELATED_SENSITIVE_NETWORK_FLOW · SKILL.md:173
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 11a1d9c136 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | SKILL.md only \| default; SKILL.md only \| behavioral; Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | data_exfiltration |
| Analyzer | correlation |
| Evidence check | unavailable |
| Title | Sensitive source reaches a network sink |
Evidence snippet:

```text

```
## Other notes

4 metadata-quality / scan-coverage rows: MANIFEST_MISSING_LICENSE (4).
