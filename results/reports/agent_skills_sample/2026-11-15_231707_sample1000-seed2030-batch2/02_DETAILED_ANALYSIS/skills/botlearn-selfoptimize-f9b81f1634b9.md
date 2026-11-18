# Skill `botlearn-selfoptimize-f9b81f1634b9`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | dvcrn/openclaw-skills-marketplace |
| SKILL.md path | plugins/calvinxhk--botlearn-selfoptimize/skills/botlearn-selfoptimize/SKILL.md |
| Sample stratum | scripts |
| Folder complete in GitSkills | False |
| Coverage | complete: every planned configuration produced a COMPLETE scan |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 1 | INFO | exit code 0 |
| SKILL.md only \| behavioral | COMPLETE | 1 | INFO | exit code 0 |
| Full folder \| default | COMPLETE | 1 | INFO | exit code 0 |
| Full folder \| behavioral | COMPLETE | 4 | MEDIUM | exit code 0 |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### MEDIUM · BEHAVIOR_BASH_TAINT_FLOW · scripts/botlearn-post.sh:272
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 8ba1ee88a4 |
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
"title": $(echo "$TITLE" | python3 -c 'import sys,json; print(json.dumps(sys.stdin.read().strip()))'),
```
### MEDIUM · BEHAVIOR_BASH_TAINT_FLOW · scripts/botlearn-post.sh:273
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 17cf51a4c6 |
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
"content": $(echo "$BODY" | python3 -c 'import sys,json; print(json.dumps(sys.stdin.read().strip()))'),
```
### MEDIUM · BEHAVIOR_BASH_TAINT_FLOW · scripts/botlearn-post.sh:292
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 85d5accbba |
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
echo "     curl -s -H 'Authorization: Bearer \$API_KEY' $BOTLEARN_API/posts/$POST_ID/comments"
```
## Other notes

4 metadata-quality / scan-coverage rows: MANIFEST_MISSING_LICENSE (4).
