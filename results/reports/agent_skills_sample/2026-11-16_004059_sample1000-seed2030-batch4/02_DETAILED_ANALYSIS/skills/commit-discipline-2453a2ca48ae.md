# Skill `commit-discipline-2453a2ca48ae`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | epologee/laicluse-agent-fieldkit |
| SKILL.md path | .agents/plugins/generated/git-discipline/skills/commit-discipline/SKILL.md |
| Sample stratum | scripts |
| Folder complete in GitSkills | True |
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
### MEDIUM · BEHAVIOR_BASH_TAINT_FLOW · git-hooks/pre-push:47
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 2ffdf3a96e |
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
if ! printf '%s\n' "$push_updates" | "$NODE_EXECUTABLE" "$GIT_DISCIPLINE" guard-push; then
```
## Other notes

4 metadata-quality / scan-coverage rows: MANIFEST_MISSING_LICENSE (4).
