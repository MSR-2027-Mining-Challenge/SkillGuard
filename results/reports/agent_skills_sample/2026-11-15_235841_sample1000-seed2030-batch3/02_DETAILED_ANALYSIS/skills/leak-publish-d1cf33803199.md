# Skill `leak-publish-d1cf33803199`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | modbender/skill-library-mcp |
| SKILL.md path | data/leak-publish/SKILL.md |
| Sample stratum | scripts |
| Folder complete in GitSkills | False |
| Coverage | complete: every planned configuration produced a COMPLETE scan |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 1 | INFO | exit code 0 |
| SKILL.md only \| behavioral | COMPLETE | 1 | INFO | exit code 0 |
| Full folder \| default | COMPLETE | 1 | INFO | exit code 0 |
| Full folder \| behavioral | COMPLETE | 3 | MEDIUM | exit code 0 |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### MEDIUM · BEHAVIOR_BASH_TAINT_FLOW · scripts/publish.sh:328
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 31007244e1 |
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
echo "[leak-publish] PROMO LINK: ${URL}/"
```
### MEDIUM · BEHAVIOR_BASH_TAINT_FLOW · scripts/publish.sh:329
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 196245d8cb |
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
echo "[leak-publish] BUY LINK:   ${URL}/download"
```
## Other notes

4 metadata-quality / scan-coverage rows: MANIFEST_MISSING_LICENSE (4).
