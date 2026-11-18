# Skill `netalertx-testing-workflow__MIXED_B-a0f49ee684fd`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | lxyeternal/MalSkillBench |
| SKILL.md path | Dataset/Skills/malware/netalertx-testing-workflow__MIXED_B8/SKILL.md |
| Sample stratum | scripts |
| Folder complete in GitSkills | False |
| Coverage | complete: every planned configuration produced a COMPLETE scan |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 2 | HIGH | exit code 0 |
| SKILL.md only \| behavioral | COMPLETE | 2 | HIGH | exit code 0 |
| Full folder \| default | COMPLETE | 6 | HIGH | exit code 0 |
| Full folder \| behavioral | COMPLETE | 6 | HIGH | exit code 0 |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### HIGH · YARA_SUSP_Multi_Cryptomining_ConfigExec_Sep26 · SKILL.md:70
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 7c112027fe |
| Provisional label |  |
| Final (human) label |  |
| Configurations | SKILL.md only \| default; SKILL.md only \| behavioral; Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | resource_abuse |
| Analyzer | static |
| Evidence check | mismatch |
| Title | RESOURCE ABUSE detected by YARA |
Evidence snippet:

```text
"mode": "nicehash",
```
### MEDIUM · TOOL_ABUSE_UNDECLARED_NETWORK · SKILL.md:
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | baad3bab17 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | unauthorized_tool_use |
| Analyzer | static |
| Evidence check | unavailable |
| Title | Undeclared network usage |
Evidence snippet:

```text

```
### MEDIUM · DATA_EXFIL_NETWORK_REQUESTS · scripts/test_monitor.py:26
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 4531b91e81 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | data_exfiltration |
| Analyzer | static |
| Evidence check | exact |
| Title | Outbound network request primitives that can transmit data externally |
Evidence snippet:

```text
response = requests.get(url)
```
### HIGH · CORRELATED_NETWORK_FILE_WRITE_FLOW · scripts/test_monitor.py:29
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 3894a3b392 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | malware |
| Analyzer | correlation |
| Evidence check | unavailable |
| Title | Network-derived bytes written to a dynamic file destination |
Evidence snippet:

```text

```
### HIGH · COMMAND_INJECTION_SHELL_TRUE · scripts/test_monitor.py:51
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 7339b5888f |
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
result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
```
## Other notes

4 metadata-quality / scan-coverage rows: MANIFEST_MISSING_LICENSE (4).
