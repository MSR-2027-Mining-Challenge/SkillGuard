# Skill `remember-ac7448c80335`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | agentculture/league-of-agents-platform |
| SKILL.md path | .claude/skills/remember/SKILL.md |
| Sample stratum | scripts |
| Folder complete in GitSkills | True |
| Coverage | complete: every planned configuration produced a COMPLETE scan |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 2 | LOW | exit code 0 |
| SKILL.md only \| behavioral | COMPLETE | 2 | LOW | exit code 0 |
| Full folder \| default | COMPLETE | 2 | LOW | exit code 0 |
| Full folder \| behavioral | COMPLETE | 3 | MEDIUM | exit code 0 |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### MEDIUM · BEHAVIOR_BASH_TAINT_FLOW · scripts/remember.sh:138
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | f05e36c414 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | data_exfiltration |
| Analyzer | behavioral |
| Evidence check | exact |
| Title | Bash: tainted data flows to dangerous sink |
Evidence snippet:

```text
exec "${EIDETIC[@]}" remember "${SCOPE_ARGS[@]}" "$@"
```
## Other notes

8 metadata-quality / scan-coverage rows: MANIFEST_DESCRIPTION_TOO_LONG (4), MANIFEST_MISSING_LICENSE (4).
