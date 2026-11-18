# Skill `ygopro-cdb48eb1b170`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | ZisIsNotZis/ygoskill |
| SKILL.md path | ygopro/SKILL.md |
| Sample stratum | scripts |
| Folder complete in GitSkills | False |
| Coverage | complete: every planned configuration produced a COMPLETE scan |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 1 | INFO | exit code 0 |
| SKILL.md only \| behavioral | COMPLETE | 1 | INFO | exit code 0 |
| Full folder \| default | COMPLETE | 5 | CRITICAL | exit code 0 |
| Full folder \| behavioral | COMPLETE | 5 | CRITICAL | exit code 0 |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### HIGH · RESOURCE_ABUSE_INFINITE_LOOP · tools/autokey/ygo.py:3
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 304ec237d3 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | resource_abuse |
| Analyzer | static |
| Evidence check | exact |
| Title | Infinite loop without clear exit condition |
Evidence snippet:

```text
while True:
```
### HIGH · RESOURCE_ABUSE_INFINITE_LOOP · tools/autokey/ygold.py:3
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 9a9c52aba2 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | resource_abuse |
| Analyzer | static |
| Evidence check | exact |
| Title | Infinite loop without clear exit condition |
Evidence snippet:

```text
while True:
```
### CRITICAL · COMMAND_INJECTION_EVAL · tools/ydkrename.py:30
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 012f9303c8 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | command_injection |
| Analyzer | static |
| Evidence check | exact |
| Title | Dangerous code execution functions that can execute arbitrary code |
Evidence snippet:

```text
SEP = compile(getenv('SEP', '[- ·/]'))
```
### CRITICAL · COMMAND_INJECTION_EVAL · tools/ydkshow.py:73
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 19db9a9c0f |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | command_injection |
| Analyzer | static |
| Evidence check | exact |
| Title | Dangerous code execution functions that can execute arbitrary code |
Evidence snippet:

```text
i = compile(i)
```
## Other notes

4 metadata-quality / scan-coverage rows: MANIFEST_MISSING_LICENSE (4).
