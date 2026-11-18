# Skill `operate-8d9c970463e7`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | feitianchengzi/arckit |
| SKILL.md path | arckit/intake/2026/2026-06-15-001-all-original/files/source/all/06-sre/operate/SKILL.md |
| Sample stratum | scripts |
| Folder complete in GitSkills | True |
| Coverage | complete: every planned configuration produced a COMPLETE scan |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 1 | INFO | exit code 0 |
| SKILL.md only \| behavioral | COMPLETE | 1 | INFO | exit code 0 |
| Full folder \| default | COMPLETE | 2 | HIGH | exit code 0 |
| Full folder \| behavioral | COMPLETE | 2 | HIGH | exit code 0 |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### HIGH · COMMAND_INJECTION_SHELL_TRUE · scripts/collect_baseline.py:26
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 2cc34cafaa |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | command_injection |
| Analyzer | static |
| Evidence check | exact |
| Title | Shell command execution with shell=True enabled |
Evidence snippet:

```text
r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
```
## Other notes

4 metadata-quality / scan-coverage rows: MANIFEST_MISSING_LICENSE (4).
