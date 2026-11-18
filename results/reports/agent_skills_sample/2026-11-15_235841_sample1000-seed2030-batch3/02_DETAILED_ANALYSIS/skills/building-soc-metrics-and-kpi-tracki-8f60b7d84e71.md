# Skill `building-soc-metrics-and-kpi-tracki-8f60b7d84e71`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | Kimurist2024/rverythong-skills |
| SKILL.md path | skills/building-soc-metrics-and-kpi-tracking/SKILL.md |
| Sample stratum | scripts |
| Folder complete in GitSkills | True |
| Coverage | complete: every planned configuration produced a COMPLETE scan |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 0 | SAFE | exit code 0 |
| SKILL.md only \| behavioral | COMPLETE | 0 | SAFE | exit code 0 |
| Full folder \| default | COMPLETE | 8 | CRITICAL | exit code 0 |
| Full folder \| behavioral | COMPLETE | 8 | CRITICAL | exit code 0 |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### MEDIUM · TOOL_ABUSE_UNDECLARED_NETWORK · SKILL.md:
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | bf72ac6977 |
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
### MEDIUM · DATA_EXFIL_NETWORK_REQUESTS · scripts/agent.py:22
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 1af8986737 |
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
resp = requests.post(
```
### MEDIUM · DATA_EXFIL_NETWORK_REQUESTS · scripts/agent.py:42
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 348e0e2883 |
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
resp = requests.post(
```
### MEDIUM · DATA_EXFIL_NETWORK_REQUESTS · scripts/agent.py:53
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | cfc57739b9 |
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
status = requests.get(
```
### MEDIUM · DATA_EXFIL_NETWORK_REQUESTS · scripts/agent.py:64
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 74eb8e4a8b |
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
results = requests.get(
```
### CRITICAL · COMMAND_INJECTION_EVAL · scripts/agent.py:106
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 8aba790cbc |
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
'sum(eval(if(status_label="Resolved - True Positive", 1, 0))) AS tp, '
```
### CRITICAL · COMMAND_INJECTION_EVAL · scripts/agent.py:107
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 5017456ee6 |
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
'sum(eval(if(status_label="Resolved - False Positive", 1, 0))) AS fp '
```
### CRITICAL · COMMAND_INJECTION_EVAL · scripts/agent.py:120
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 8ecfb58f45 |
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
"avg(eval((status_end - status_transition_time) / 60)) AS avg_triage_min "
```
## Other notes

0 metadata-quality / scan-coverage rows: .
