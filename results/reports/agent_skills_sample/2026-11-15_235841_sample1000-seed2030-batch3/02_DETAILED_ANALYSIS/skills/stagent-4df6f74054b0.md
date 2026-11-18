# Skill `stagent-4df6f74054b0`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | jie-worldstatelabs/stagent |
| SKILL.md path | skills/stagent/SKILL.md |
| Sample stratum | supporting_no_scripts |
| Folder complete in GitSkills | True |
| Coverage | complete: every planned configuration produced a COMPLETE scan |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 1 | INFO | exit code 0 |
| SKILL.md only \| behavioral | COMPLETE | 6 | MEDIUM | exit code 0 |
| Full folder \| default | COMPLETE | 1 | INFO | exit code 0 |
| Full folder \| behavioral | COMPLETE | 6 | MEDIUM | exit code 0 |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### MEDIUM · BEHAVIOR_BASH_TAINT_FLOW · SKILL.md:122
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 9923a04216 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | SKILL.md only \| behavioral; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | data_exfiltration |
| Analyzer | behavioral |
| Evidence check | mismatch |
| Title | Bash: sensitive data flows to execution sink |
Evidence snippet:

```text
if ! "$P/scripts/loop-tick.sh" >/dev/null 2>&1; then
```
### MEDIUM · BEHAVIOR_BASH_TAINT_FLOW · SKILL.md:155
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 05068368a1 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | SKILL.md only \| behavioral; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | data_exfiltration |
| Analyzer | behavioral |
| Evidence check | mismatch |
| Title | Bash: sensitive data flows to execution sink |
Evidence snippet:

```text
TICK="$("$P/scripts/loop-tick.sh")"
```
### MEDIUM · BEHAVIOR_BASH_TAINT_FLOW · SKILL.md:200
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | d9e696baa1 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | SKILL.md only \| behavioral; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | data_exfiltration |
| Analyzer | behavioral |
| Evidence check | mismatch |
| Title | Bash: sensitive data flows to execution sink |
Evidence snippet:

```text
NEXT="$("$P/scripts/next-status.sh" --result "$RESULT")"
```
### MEDIUM · BEHAVIOR_BASH_TAINT_FLOW · SKILL.md:221
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | b5328c53d2 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | SKILL.md only \| behavioral; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | data_exfiltration |
| Analyzer | behavioral |
| Evidence check | mismatch |
| Title | Bash: sensitive data flows to execution sink |
Evidence snippet:

```text
"$P/scripts/update-status.sh" --status "$(echo "$NEXT" | jq -r .next_status)"
```
### MEDIUM · BEHAVIOR_BASH_TAINT_FLOW · SKILL.md:257
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 9923a04216 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | SKILL.md only \| behavioral; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | data_exfiltration |
| Analyzer | behavioral |
| Evidence check | mismatch |
| Title | Bash: sensitive data flows to execution sink |
Evidence snippet:

```text
"$P/scripts/update-status.sh" --status escalated
```
## Other notes

4 metadata-quality / scan-coverage rows: MANIFEST_MISSING_LICENSE (4).
