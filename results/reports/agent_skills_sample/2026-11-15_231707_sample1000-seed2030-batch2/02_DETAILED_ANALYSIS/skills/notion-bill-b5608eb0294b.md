# Skill `notion-bill-b5608eb0294b`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | publieople/hermes-config-kit |
| SKILL.md path | skills/productivity/notion-bill/SKILL.md |
| Sample stratum | scripts |
| Folder complete in GitSkills | True |
| Coverage | complete: every planned configuration produced a COMPLETE scan |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 1 | INFO | exit code 0 |
| SKILL.md only \| behavioral | COMPLETE | 1 | INFO | exit code 0 |
| Full folder \| default | COMPLETE | 14 | MEDIUM | exit code 0 |
| Full folder \| behavioral | COMPLETE | 14 | MEDIUM | exit code 0 |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### MEDIUM · TOOL_ABUSE_UNDECLARED_NETWORK · SKILL.md:
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | a8ee660b27 |
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
### LOW · UNDECLARED_NETWORK_DESTINATION · scripts/create-bill-safe.py:31
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 9a78218e97 |
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
### MEDIUM · DATA_EXFIL_NETWORK_REQUESTS · scripts/create-bill-safe.py:32
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | c0311dba9e |
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
req = urllib.request.Request(url, data=json.dumps(body).encode(), headers=HEADERS, method="POST")
```
### MEDIUM · DATA_EXFIL_NETWORK_REQUESTS · scripts/create-bill-safe.py:33
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | e9981d8d09 |
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
with urllib.request.urlopen(req) as resp:
```
### MEDIUM · DATA_EXFIL_NETWORK_REQUESTS · scripts/create-bill-safe.py:38
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 44e67393fb |
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
req = urllib.request.Request(url, headers=HEADERS, method="GET")
```
### MEDIUM · DATA_EXFIL_NETWORK_REQUESTS · scripts/create-bill-safe.py:39
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | b1c4f12ba0 |
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
with urllib.request.urlopen(req) as resp:
```
### MEDIUM · DATA_EXFIL_NETWORK_REQUESTS · scripts/create-bill-safe.py:44
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | e6a0331eca |
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
req = urllib.request.Request(url, data=json.dumps(body).encode(), headers=HEADERS, method="PATCH")
```
### MEDIUM · DATA_EXFIL_NETWORK_REQUESTS · scripts/create-bill-safe.py:45
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | a8bfe36ce0 |
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
with urllib.request.urlopen(req) as resp:
```
### LOW · UNDECLARED_NETWORK_DESTINATION · scripts/ocr.py:13
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | e348c086e0 |
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
### MEDIUM · DATA_EXFIL_NETWORK_REQUESTS · scripts/ocr.py:38
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 64850e0bc0 |
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
### MEDIUM · DATA_EXFIL_NETWORK_REQUESTS · scripts/ocr.py:48
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 75f2a289a8 |
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
with urllib.request.urlopen(req, timeout=120) as resp:
```
### MEDIUM · DATA_EXFIL_NETWORK_REQUESTS · scripts/query-bills.py:25
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 60e837f824 |
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
req = urllib.request.Request(url, data=json.dumps(body).encode(), headers=HEADERS, method="POST")
```
### MEDIUM · DATA_EXFIL_NETWORK_REQUESTS · scripts/query-bills.py:26
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | b3ead79de9 |
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
with urllib.request.urlopen(req) as resp:
```
## Other notes

4 metadata-quality / scan-coverage rows: MANIFEST_MISSING_LICENSE (4).
