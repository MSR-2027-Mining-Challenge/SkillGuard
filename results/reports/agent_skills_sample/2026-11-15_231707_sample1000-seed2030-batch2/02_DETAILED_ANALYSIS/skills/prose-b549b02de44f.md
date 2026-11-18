# Skill `prose-b549b02de44f`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | Flexasaurusrex/OpenPaw |
| SKILL.md path | extensions/open-prose/skills/prose/SKILL.md |
| Sample stratum | supporting_no_scripts |
| Folder complete in GitSkills | False |
| Coverage | complete: every planned configuration produced a COMPLETE scan |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 1 | INFO | exit code 0 |
| SKILL.md only \| behavioral | COMPLETE | 1 | INFO | exit code 0 |
| Full folder \| default | COMPLETE | 3 | HIGH | exit code 0 |
| Full folder \| behavioral | COMPLETE | 3 | HIGH | exit code 0 |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### HIGH · SECRET_CONNECTION_STRING · state/postgres.md:508
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 046c16e4d1 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | hardcoded_secrets |
| Analyzer | static |
| Evidence check | exact |
| Title | Database connection string with embedded credentials |
Evidence snippet:

```text
| Connection | `post****host:5432/db` |
```
### HIGH · SECRET_CONNECTION_STRING · state/postgres.md:538
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | abcb29e1c6 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | hardcoded_secrets |
| Analyzer | static |
| Evidence check | exact |
| Title | Database connection string with embedded credentials |
Evidence snippet:

```text
| Connection | `post****host:5432/db` |
```
## Other notes

4 metadata-quality / scan-coverage rows: MANIFEST_MISSING_LICENSE (4).
