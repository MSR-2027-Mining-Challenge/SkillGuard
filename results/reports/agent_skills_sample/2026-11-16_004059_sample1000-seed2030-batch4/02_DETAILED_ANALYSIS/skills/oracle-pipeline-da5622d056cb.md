# Skill `oracle-pipeline-da5622d056cb`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | carespace-ai/maestro-skills |
| SKILL.md path | skills/oracle-pipeline/SKILL.md |
| Sample stratum | scripts |
| Folder complete in GitSkills | False |
| Coverage | complete: every planned configuration produced a COMPLETE scan |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 1 | INFO | exit code 0 |
| SKILL.md only \| behavioral | COMPLETE | 1 | INFO | exit code 0 |
| Full folder \| default | COMPLETE | 1 | INFO | exit code 0 |
| Full folder \| behavioral | COMPLETE | 5 | MEDIUM | exit code 0 |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### MEDIUM · BEHAVIOR_BASH_TAINT_FLOW · scripts/03-run-story.sh:128
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 01b35a3bff |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | data_exfiltration |
| Analyzer | behavioral |
| Evidence check | exact |
| Title | Bash: sensitive data flows to execution sink |
Evidence snippet:

```text
if ! "$SCRIPT_DIR/lint-check.sh" "$REPO_ROOT"; then
```
### MEDIUM · BEHAVIOR_BASH_TAINT_FLOW · scripts/03-run-story.sh:131
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 5495a6f5f5 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | data_exfiltration |
| Analyzer | behavioral |
| Evidence check | exact |
| Title | Bash: sensitive data flows to execution sink |
Evidence snippet:

```text
if ! "$SCRIPT_DIR/check-coverage.sh" "$REPO_ROOT"; then
```
### MEDIUM · BEHAVIOR_BASH_TAINT_FLOW · scripts/03-run-story.sh:141
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 3bf44b77ee |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | data_exfiltration |
| Analyzer | behavioral |
| Evidence check | exact |
| Title | Bash: sensitive data flows to execution sink |
Evidence snippet:

```text
"$SCRIPT_DIR/lint-check.sh"     "$REPO_ROOT" || GATE_FAILS="${GATE_FAILS}lint "
```
### MEDIUM · BEHAVIOR_BASH_TAINT_FLOW · scripts/03-run-story.sh:142
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | d37c4f1eda |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | data_exfiltration |
| Analyzer | behavioral |
| Evidence check | exact |
| Title | Bash: sensitive data flows to execution sink |
Evidence snippet:

```text
"$SCRIPT_DIR/check-coverage.sh" "$REPO_ROOT" || GATE_FAILS="${GATE_FAILS}tests/coverage "
```
## Other notes

4 metadata-quality / scan-coverage rows: MANIFEST_MISSING_LICENSE (4).
