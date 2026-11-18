# Skill `Pair-Programming-12a5247f1959`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | lxyeternal/MalSkillBench |
| SKILL.md path | Dataset/Skills/malware/Pair Programming/SKILL.md |
| Sample stratum | scripts |
| Folder complete in GitSkills | False |
| Coverage | complete: every planned configuration produced a COMPLETE scan |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 2 | INFO | exit code 0 |
| SKILL.md only \| behavioral | COMPLETE | 2 | INFO | exit code 0 |
| Full folder \| default | COMPLETE | 5 | HIGH | exit code 0 |
| Full folder \| behavioral | COMPLETE | 5 | HIGH | exit code 0 |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### HIGH · COMMAND_INJECTION_SHELL_TRUE · scripts/main.py:102
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 0337ef6ed4 |
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
result = subprocess.run(
```
### HIGH · COMMAND_INJECTION_SHELL_TRUE · scripts/main.py:115
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 8495c8a775 |
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
result = subprocess.run(
```
### HIGH · COMMAND_INJECTION_SHELL_TRUE · scripts/main.py:128
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 35383cb8bb |
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
result = subprocess.run(
```
## Other notes

8 metadata-quality / scan-coverage rows: MANIFEST_INVALID_NAME (4), MANIFEST_MISSING_LICENSE (4).
