# Skill `play-audio-abdb9853c39c`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | tps2015gh/auto-news-reader |
| SKILL.md path | play-audio/SKILL.md |
| Sample stratum | scripts |
| Folder complete in GitSkills | True |
| Coverage | complete: every planned configuration produced a COMPLETE scan |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 1 | INFO | exit code 0 |
| SKILL.md only \| behavioral | COMPLETE | 1 | INFO | exit code 0 |
| Full folder \| default | COMPLETE | 3 | CRITICAL | exit code 0 |
| Full folder \| behavioral | COMPLETE | 3 | CRITICAL | exit code 0 |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### HIGH · COMMAND_INJECTION_SHELL_TRUE · play_audio.py:15
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | ec489279bc |
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
os.system('pip install pygame')
```
### CRITICAL · COMMAND_INJECTION_OS_SYSTEM · play_audio.py:43
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 9a0148bca9 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | command_injection |
| Analyzer | static |
| Evidence check | exact |
| Title | Shell command execution with string formatting (potential injection) |
Evidence snippet:

```text
os.system(f'start "" "{filepath}"')
```
## Other notes

4 metadata-quality / scan-coverage rows: MANIFEST_MISSING_LICENSE (4).
