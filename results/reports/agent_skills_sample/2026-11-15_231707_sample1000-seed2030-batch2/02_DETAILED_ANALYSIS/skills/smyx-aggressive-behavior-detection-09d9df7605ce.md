# Skill `smyx-aggressive-behavior-detection-09d9df7605ce`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | smyx-sunjinhui/smyx-open-claw-skills |
| SKILL.md path | skills/smyx-aggressive-behavior-detection-analysis/SKILL.md |
| Sample stratum | scripts |
| Folder complete in GitSkills | True |
| Coverage | complete: every planned configuration produced a COMPLETE scan |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 1 | INFO | exit code 0 |
| SKILL.md only \| behavioral | COMPLETE | 1 | INFO | exit code 0 |
| Full folder \| default | COMPLETE | 6 | MEDIUM | exit code 0 |
| Full folder \| behavioral | COMPLETE | 6 | MEDIUM | exit code 0 |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### MEDIUM · TOOL_ABUSE_UNDECLARED_NETWORK · SKILL.md:
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 0f4ac28b5a |
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
### MEDIUM · FILE_MAGIC_MISMATCH · scripts/__init__.py:
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | ae8bf0304c |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | obfuscation |
| Analyzer | static |
| Evidence check | unavailable |
| Title | File extension does not match actual content type |
Evidence snippet:

```text

```
### MEDIUM · DATA_EXFIL_NETWORK_REQUESTS · skills/smyx_common/scripts/util.py:42
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | dc3e650b12 |
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
http.client.HTTPConnection.debuglevel = 1
```
### MEDIUM · DATA_EXFIL_NETWORK_REQUESTS · skills/smyx_common/scripts/util.py:561
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 3a755bf681 |
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
_response = requests.post(_url, json=_data)
```
### MEDIUM · DATA_EXFIL_NETWORK_REQUESTS · skills/smyx_common/scripts/util.py:646
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 7ede9b7204 |
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
response = requests.request(method, url, *args, json=data, params=params, headers=headers,
```
## Other notes

4 metadata-quality / scan-coverage rows: MANIFEST_MISSING_LICENSE (4).
