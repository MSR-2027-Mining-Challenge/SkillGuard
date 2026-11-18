# Skill `skill-5b7d9c666e2d`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | GuiPulp/hypertrend-trading-university |
| SKILL.md path | SKILL.md |
| Sample stratum | scripts |
| Folder complete in GitSkills | False |
| Coverage | complete: every planned configuration produced a COMPLETE scan |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 1 | INFO | exit code 0 |
| SKILL.md only \| behavioral | COMPLETE | 1 | INFO | exit code 0 |
| Full folder \| default | COMPLETE | 9 | MEDIUM | exit code 0 |
| Full folder \| behavioral | COMPLETE | 9 | MEDIUM | exit code 0 |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### MEDIUM · TOOL_ABUSE_UNDECLARED_NETWORK · SKILL.md:
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | ea0c50142e |
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
### LOW · SUPPLY_CHAIN_UNPINNED_DEPENDENCY · requirements.txt:4
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 74726b67e8 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | supply_chain_attack |
| Analyzer | static |
| Evidence check | exact |
| Title | Unpinned dependency |
Evidence snippet:

```text
urllib3>=2.0.0
```
### MEDIUM · DATA_EXFIL_NETWORK_REQUESTS · src/htu/api_client.py:37
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | d2e9ebb4e8 |
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
req = urllib.request.Request(url, headers=req_headers, method='GET')
```
### MEDIUM · DATA_EXFIL_NETWORK_REQUESTS · src/htu/api_client.py:40
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 2818d7719b |
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
req = urllib.request.Request(url, data=json_data, headers=req_headers, method=method)
```
### MEDIUM · DATA_EXFIL_NETWORK_REQUESTS · src/htu/api_client.py:42
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | be5e8290ef |
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
with urllib.request.urlopen(req, timeout=self.timeout) as response:
```
### MEDIUM · DATA_EXFIL_NETWORK_REQUESTS · src/htu/api_client_v2.py:87
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | e1e6d47448 |
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
req = urllib.request.Request(url, headers=req_headers, method='GET')
```
### MEDIUM · DATA_EXFIL_NETWORK_REQUESTS · src/htu/api_client_v2.py:90
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | a521494790 |
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
req = urllib.request.Request(url, data=json_data, headers=req_headers, method=method)
```
### MEDIUM · DATA_EXFIL_NETWORK_REQUESTS · src/htu/api_client_v2.py:92
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | d9e7242136 |
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
with urllib.request.urlopen(req, timeout=self.timeout) as response:
```
## Other notes

4 metadata-quality / scan-coverage rows: MANIFEST_MISSING_LICENSE (4).
