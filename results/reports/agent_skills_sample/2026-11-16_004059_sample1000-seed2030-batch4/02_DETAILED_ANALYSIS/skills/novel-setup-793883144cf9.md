# Skill `novel-setup-793883144cf9`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | 1608kiy/oh-novel-claudecode |
| SKILL.md path | skills/novel-setup/SKILL.md |
| Sample stratum | scripts |
| Folder complete in GitSkills | False |
| Coverage | complete: every planned configuration produced a COMPLETE scan |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 1 | INFO | exit code 0 |
| SKILL.md only \| behavioral | COMPLETE | 1 | INFO | exit code 0 |
| Full folder \| default | COMPLETE | 1 | INFO | exit code 0 |
| Full folder \| behavioral | COMPLETE | 2 | MEDIUM | exit code 0 |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### MEDIUM · BEHAVIOR_BASH_TAINT_FLOW · references/templates/hooks/session-start.sh:44
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 15adab71cf |
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
OUTPUT+="[WARN] novel-setup agents_version=$AGENTS_VERSION is older than v1. Re-run /novel-setup to refresh hooks, agents, and references.\n\n"
```
## Other notes

4 metadata-quality / scan-coverage rows: MANIFEST_MISSING_LICENSE (4).
