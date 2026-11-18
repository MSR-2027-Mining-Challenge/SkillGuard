# Skill `lerneinheit-9754e2e2f353`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | TimRudorf/dotfiles |
| SKILL.md path | claude/skills/lerneinheit/SKILL.md |
| Sample stratum | scripts |
| Folder complete in GitSkills | True |
| Coverage | complete: every planned configuration produced a COMPLETE scan |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 1 | INFO | exit code 0 |
| SKILL.md only \| behavioral | COMPLETE | 2 | MEDIUM | exit code 0 |
| Full folder \| default | COMPLETE | 2 | LOW | exit code 0 |
| Full folder \| behavioral | COMPLETE | 4 | MEDIUM | exit code 0 |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### MEDIUM · BEHAVIOR_BASH_TAINT_FLOW · SKILL.md:57
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 9f6bed89a7 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | SKILL.md only \| behavioral; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | data_exfiltration |
| Analyzer | behavioral |
| Evidence check | mismatch |
| Title | Bash: tainted data flows to dangerous sink |
Evidence snippet:

```text
bash ~/.claude/skills/remarkable-upload/scripts/rm.sh put <local-pfad> "$FOLDER/"
```
### LOW · UNDECLARED_NETWORK_DESTINATION · scripts/patch_todoist_task.sh:59
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 6922e41aa8 |
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
### MEDIUM · BEHAVIOR_BASH_TAINT_FLOW · scripts/patch_todoist_task.sh:115
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 1f245a2e8b |
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
PAYLOAD=$(python3 -c "import json,sys; print(json.dumps({'description': sys.argv[1]}))" "$NEW_DESC")
```
## Other notes

4 metadata-quality / scan-coverage rows: MANIFEST_MISSING_LICENSE (4).
