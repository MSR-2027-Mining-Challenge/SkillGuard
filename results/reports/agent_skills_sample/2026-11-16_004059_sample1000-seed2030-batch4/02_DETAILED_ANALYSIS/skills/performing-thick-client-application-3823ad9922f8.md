# Skill `performing-thick-client-application-3823ad9922f8`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | b3belov/security-superpowers |
| SKILL.md path | plugins/security-superpowers/skills/performing-thick-client-application-penetration-test/SKILL.md |
| Sample stratum | scripts |
| Folder complete in GitSkills | True |
| Coverage | complete: every planned configuration produced a COMPLETE scan |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 1 | CRITICAL | exit code 0 |
| SKILL.md only \| behavioral | COMPLETE | 1 | CRITICAL | exit code 0 |
| Full folder \| default | COMPLETE | 1 | CRITICAL | exit code 0 |
| Full folder \| behavioral | COMPLETE | 1 | CRITICAL | exit code 0 |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### CRITICAL · YARA_sql_injection_generic · SKILL.md:178
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 1bb52301d1 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | SKILL.md only \| default; SKILL.md only \| behavioral; Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | command_injection |
| Analyzer | static |
| Evidence check | mismatch |
| Title | INJECTION ATTACK detected by YARA |
Evidence snippet:

```text
# Test input fields with: ' OR 1=1--
```
## Other notes

0 metadata-quality / scan-coverage rows: .
