# Skill `synthdata-compute-82db1d3c4db1`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | rappdw/synthdata |
| SKILL.md path | skills/synthdata-compute/SKILL.md |
| Sample stratum | scripts |
| Folder complete in GitSkills | True |
| Coverage | complete: every planned configuration produced a COMPLETE scan |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 1 | INFO | exit code 0 |
| SKILL.md only \| behavioral | COMPLETE | 1 | INFO | exit code 0 |
| Full folder \| default | COMPLETE | 2 | CRITICAL | exit code 0 |
| Full folder \| behavioral | COMPLETE | 2 | CRITICAL | exit code 0 |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### CRITICAL · COMMAND_INJECTION_EVAL · scripts/compute.py:174
|  | value |
|---|---|
| Validation | Provisional label (AI-assisted, not independent human review) |
| Review ID | 4536303dec |
| Provisional label | uncertain |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | command_injection |
| Analyzer | static |
| Evidence check | exact |
| Title | Dangerous code execution functions that can execute arbitrary code |
Evidence snippet:

```text
exec(code, namespace)
```
## Other notes

4 metadata-quality / scan-coverage rows: MANIFEST_MISSING_LICENSE (4).
