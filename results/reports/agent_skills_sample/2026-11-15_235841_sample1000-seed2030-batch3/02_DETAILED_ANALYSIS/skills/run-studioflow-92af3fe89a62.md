# Skill `run-studioflow-92af3fe89a62`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | EPW80/studioFlow |
| SKILL.md path | .claude/skills/run-studioflow/SKILL.md |
| Sample stratum | scripts |
| Folder complete in GitSkills | True |
| Coverage | complete: every planned configuration produced a COMPLETE scan |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 1 | INFO | exit code 0 |
| SKILL.md only \| behavioral | COMPLETE | 1 | INFO | exit code 0 |
| Full folder \| default | COMPLETE | 3 | HIGH | exit code 0 |
| Full folder \| behavioral | COMPLETE | 9 | CRITICAL | exit code 0 |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### HIGH · CORRELATED_SENSITIVE_NETWORK_FLOW · smoke.sh:35
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 226b63c08f |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | data_exfiltration |
| Analyzer | correlation |
| Evidence check | unavailable |
| Title | Sensitive source reaches a network sink |
Evidence snippet:

```text

```
### HIGH · SECRET_CONNECTION_STRING · start.sh:24
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 4436988c24 |
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
-e DATABASE_URL=post****db/studioflow_development \
```
### MEDIUM · BEHAVIOR_BASH_TAINT_FLOW · smoke.sh:22
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 9b1efc039c |
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
code=$(curl -sS -D "$H" -o /tmp/r.json -w '%{http_code}' -X POST "$BASE/api/v1/signup" \
```
### MEDIUM · BEHAVIOR_BASH_TAINT_FLOW · smoke.sh:35
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 344ecc3dac |
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
code=$(curl -sS -o /tmp/r.json -w '%{http_code}' "$BASE/api/v1/projects" -H "Authorization: $TOKEN")
```
### CRITICAL · BEHAVIOR_BASH_TAINT_FLOW · smoke.sh:50
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | c05a786042 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | data_exfiltration |
| Analyzer | behavioral |
| Evidence check | exact |
| Title | Bash: sensitive data exfiltration via network |
Evidence snippet:

```text
code=$(curl -sS -o /tmp/r.json -w '%{http_code}' -X PATCH "$BASE/api/v1/projects/$PID/update_status" \
```
### CRITICAL · BEHAVIOR_BASH_TAINT_FLOW · smoke.sh:57
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | b2593be9c3 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | data_exfiltration |
| Analyzer | behavioral |
| Evidence check | exact |
| Title | Bash: sensitive data exfiltration via network |
Evidence snippet:

```text
code=$(curl -sS -o /tmp/r.json -w '%{http_code}' "$BASE/api/v1/projects/$PID/activity" -H "Authorization: $TOKEN")
```
### MEDIUM · BEHAVIOR_BASH_TAINT_FLOW · smoke.sh:64
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 78aed406ae |
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
code=$(curl -sS -o /dev/null -w '%{http_code}' -X DELETE "$BASE/api/v1/logout" -H "Authorization: $TOKEN")
```
### MEDIUM · BEHAVIOR_BASH_TAINT_FLOW · smoke.sh:68
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | f10ae53de6 |
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
code=$(curl -sS -o /dev/null -w '%{http_code}' "$BASE/api/v1/projects" -H "Authorization: $TOKEN")
```
## Other notes

4 metadata-quality / scan-coverage rows: MANIFEST_MISSING_LICENSE (4).
