# Skill `video-editor-d2b8fc3e8591`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | minicoohei/ai-agent-camp |
| SKILL.md path | skills/video-editor/SKILL.md |
| Sample stratum | scripts |
| Folder complete in GitSkills | True |
| Coverage | complete: every planned configuration produced a COMPLETE scan |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 1 | INFO | exit code 0 |
| SKILL.md only \| behavioral | COMPLETE | 1 | INFO | exit code 0 |
| Full folder \| default | COMPLETE | 12 | CRITICAL | exit code 0 |
| Full folder \| behavioral | COMPLETE | 12 | CRITICAL | exit code 0 |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### MEDIUM · TOOL_ABUSE_UNDECLARED_NETWORK · SKILL.md:
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 2e299e254e |
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
### CRITICAL · COMMAND_INJECTION_OS_SYSTEM · scripts/compose_video.py:52
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 9aadf68a09 |
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
result = subprocess.run(["fc-list", ":style=Bold", "-f", "%{file}\n"],
```
### CRITICAL · COMMAND_INJECTION_OS_SYSTEM · scripts/compose_video.py:334
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | f089a3848a |
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
upload_result = subprocess.run(
```
### LOW · UNDECLARED_NETWORK_DESTINATION · scripts/compose_video.py:337
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 2d25c744f8 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | unauthorized_tool_use |
| Analyzer | static |
| Evidence check | unavailable |
| Title | Script contacts a destination the documentation never mentions |
Evidence snippet:

```text

```
### MEDIUM · DATA_EXFIL_NETWORK_REQUESTS · scripts/compose_video.py:360
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 46848b173d |
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
req = urllib.request.Request(
```
### LOW · UNDECLARED_NETWORK_DESTINATION · scripts/compose_video.py:361
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 34f0da46c9 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | unauthorized_tool_use |
| Analyzer | static |
| Evidence check | unavailable |
| Title | Script contacts a destination the documentation never mentions |
Evidence snippet:

```text

```
### MEDIUM · DATA_EXFIL_NETWORK_REQUESTS · scripts/compose_video.py:365
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 67dbe447c6 |
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
with urllib.request.urlopen(req, timeout=30) as resp:
```
### MEDIUM · DATA_EXFIL_NETWORK_REQUESTS · scripts/compose_video.py:384
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | f655043e25 |
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
req = urllib.request.Request(
```
### MEDIUM · DATA_EXFIL_NETWORK_REQUESTS · scripts/compose_video.py:388
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 987ce6f9c5 |
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
with urllib.request.urlopen(req, timeout=10) as resp:
```
### MEDIUM · DATA_EXFIL_NETWORK_REQUESTS · scripts/compose_video.py:394
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 7e43237adc |
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
req2 = urllib.request.Request(
```
### MEDIUM · DATA_EXFIL_NETWORK_REQUESTS · scripts/compose_video.py:398
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 6f9f306a45 |
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
with urllib.request.urlopen(req2, timeout=30) as resp2:
```
## Other notes

4 metadata-quality / scan-coverage rows: MANIFEST_MISSING_LICENSE (4).
