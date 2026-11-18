# Skill `performing-brand-monitoring-for-imp-56bdaa80d443`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | yanacuti1121/Yana-AI |
| SKILL.md path | .claude/skills/performing-brand-monitoring-for-impersonation/SKILL.md |
| Sample stratum | scripts |
| Folder complete in GitSkills | True |
| Coverage | complete: every planned configuration produced a COMPLETE scan |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 1 | HIGH | exit code 0 |
| SKILL.md only \| behavioral | COMPLETE | 3 | HIGH | exit code 0 |
| Full folder \| default | COMPLETE | 4 | CRITICAL | exit code 0 |
| Full folder \| behavioral | COMPLETE | 6 | CRITICAL | exit code 0 |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### HIGH · ACTIVE_DYNAMIC_EXECUTION · SKILL.md:97
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | ca70981944 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | SKILL.md only \| default; SKILL.md only \| behavioral; Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | command_injection |
| Analyzer | static |
| Evidence check | exact |
| Title | Active instruction invokes dynamic code or process execution |
Evidence snippet:

```text
result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
```
### MEDIUM · MDBLOCK_PYTHON_SUBPROCESS · SKILL.md:64
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 0fb18b2fc8 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | SKILL.md only \| behavioral; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | command_injection |
| Analyzer | behavioral |
| Evidence check | mismatch |
| Title | Python code block executes shell commands |
Evidence snippet:

```text
result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
```
### MEDIUM · MDBLOCK_PYTHON_HTTP_POST · SKILL.md:97
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 72e1f72e64 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | SKILL.md only \| behavioral; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | data_exfiltration |
| Analyzer | behavioral |
| Evidence check | mismatch |
| Title | Python code block sends HTTP POST request |
Evidence snippet:

```text
resp = requests.post(url, json=body, timeout=15)
```
### MEDIUM · TOOL_ABUSE_UNDECLARED_NETWORK · SKILL.md:
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | ae231e9999 |
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
### CRITICAL · DATA_EXFIL_SOCKET_CONNECT · scripts/agent.py:74
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 0694dfd4fd |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | data_exfiltration |
| Analyzer | static |
| Evidence check | exact |
| Title | Direct socket connection to external server |
Evidence snippet:

```text
ip = socket.gethostbyname(domain)
```
### MEDIUM · DATA_EXFIL_NETWORK_REQUESTS · scripts/agent.py:92
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 3970feca76 |
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
resp = requests.get(
```
## Other notes

0 metadata-quality / scan-coverage rows: .
