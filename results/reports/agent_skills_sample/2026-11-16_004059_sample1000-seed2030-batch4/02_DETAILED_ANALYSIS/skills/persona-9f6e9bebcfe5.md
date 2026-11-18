# Skill `persona-9f6e9bebcfe5`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | eunsu0430/aiproject |
| SKILL.md path | persona/SKILL.md |
| Sample stratum | scripts |
| Folder complete in GitSkills | False |
| Coverage | partially_complete: some configurations are COMPLETE, others are partial, contract-only or failed |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 1 | INFO | exit code 0 |
| SKILL.md only \| behavioral | COMPLETE | 1 | INFO | exit code 0 |
| Full folder \| default | COMPLETE | 23 | HIGH | exit code 0 |
| Full folder \| behavioral | CONTRACT_ONLY | 27 | CRITICAL | Cisco reported an analyzer failure (behavioral: FindingContract:BEHAVIOR_CROSSFILE_EXFILTRATION_CHAIN:UNKNOWN_BUNDLED_PYTHON_RULE); Cisco reported an analyzer failure (behavioral: FindingContract:BEHAVIOR_CROSSFILE_ENV_VAR_EXFILTRATION:UNKNOWN_BUNDLED_PYTHON_RULE) |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### MEDIUM · TOOL_ABUSE_UNDECLARED_NETWORK · SKILL.md:
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 45a0a2c996 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete; contract_only |
| Cisco category | unauthorized_tool_use |
| Analyzer | static |
| Evidence check | unavailable |
| Title | Undeclared network usage |
Evidence snippet:

```text

```
### LOW · SUPPLY_CHAIN_UNPINNED_DEPENDENCY · requirements.txt:2
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 2e57a643d9 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete; contract_only |
| Cisco category | supply_chain_attack |
| Analyzer | static |
| Evidence check | exact |
| Title | Unpinned dependency |
Evidence snippet:

```text
datasets>=2.18
```
### LOW · SUPPLY_CHAIN_UNPINNED_DEPENDENCY · requirements.txt:3
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 16a63cf459 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete; contract_only |
| Cisco category | supply_chain_attack |
| Analyzer | static |
| Evidence check | exact |
| Title | Unpinned dependency |
Evidence snippet:

```text
huggingface_hub>=0.22
```
### LOW · SUPPLY_CHAIN_UNPINNED_DEPENDENCY · requirements.txt:4
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | e5b91ea90e |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete; contract_only |
| Cisco category | supply_chain_attack |
| Analyzer | static |
| Evidence check | exact |
| Title | Unpinned dependency |
Evidence snippet:

```text
duckdb>=0.10
```
### LOW · SUPPLY_CHAIN_UNPINNED_DEPENDENCY · requirements.txt:5
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | ca90049250 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete; contract_only |
| Cisco category | supply_chain_attack |
| Analyzer | static |
| Evidence check | exact |
| Title | Unpinned dependency |
Evidence snippet:

```text
pyarrow>=15
```
### LOW · SUPPLY_CHAIN_UNPINNED_DEPENDENCY · requirements.txt:6
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 16ab3f9c28 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete; contract_only |
| Cisco category | supply_chain_attack |
| Analyzer | static |
| Evidence check | exact |
| Title | Unpinned dependency |
Evidence snippet:

```text
beautifulsoup4>=4.12
```
### LOW · SUPPLY_CHAIN_UNPINNED_DEPENDENCY · requirements.txt:7
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 84672418fd |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete; contract_only |
| Cisco category | supply_chain_attack |
| Analyzer | static |
| Evidence check | exact |
| Title | Unpinned dependency |
Evidence snippet:

```text
requests>=2.31
```
### LOW · SUPPLY_CHAIN_UNPINNED_DEPENDENCY · requirements.txt:8
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 851082ac2e |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete; contract_only |
| Cisco category | supply_chain_attack |
| Analyzer | static |
| Evidence check | exact |
| Title | Unpinned dependency |
Evidence snippet:

```text
playwright>=1.40
```
### LOW · UNDECLARED_NETWORK_DESTINATION · scripts/fetch_assembly_statements.py:43
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 773eb59c4d |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete; contract_only |
| Cisco category | unauthorized_tool_use |
| Analyzer | static |
| Evidence check | unavailable |
| Title | Script contacts a destination the documentation never mentions |
Evidence snippet:

```text

```
### LOW · UNDECLARED_NETWORK_DESTINATION · scripts/fetch_assembly_statements.py:52
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 8e32ba9df2 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete; contract_only |
| Cisco category | unauthorized_tool_use |
| Analyzer | static |
| Evidence check | unavailable |
| Title | Script contacts a destination the documentation never mentions |
Evidence snippet:

```text

```
### LOW · UNDECLARED_NETWORK_DESTINATION · scripts/fetch_assembly_statements.py:61
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | b3f27959ba |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete; contract_only |
| Cisco category | unauthorized_tool_use |
| Analyzer | static |
| Evidence check | unavailable |
| Title | Script contacts a destination the documentation never mentions |
Evidence snippet:

```text

```
### LOW · UNDECLARED_NETWORK_DESTINATION · scripts/fetch_bai_data.py:16
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | a765149c21 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete; contract_only |
| Cisco category | unauthorized_tool_use |
| Analyzer | static |
| Evidence check | unavailable |
| Title | Script contacts a destination the documentation never mentions |
Evidence snippet:

```text

```
### HIGH · CORRELATED_SENSITIVE_NETWORK_FLOW · scripts/fetch_g2b_data.py:42
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | c74c8032dc |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete; contract_only |
| Cisco category | data_exfiltration |
| Analyzer | correlation |
| Evidence check | unavailable |
| Title | Sensitive source reaches a network sink |
Evidence snippet:

```text

```
### MEDIUM · DATA_EXFIL_NETWORK_REQUESTS · scripts/fetch_g2b_data.py:42
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 60fcac450d |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete; contract_only |
| Cisco category | data_exfiltration |
| Analyzer | static |
| Evidence check | exact |
| Title | Outbound network request primitives that can transmit data externally |
Evidence snippet:

```text
resp = requests.get(API_URL, params=params, timeout=REQUEST_TIMEOUT)
```
### LOW · UNDECLARED_NETWORK_DESTINATION · scripts/fetch_kdi_reports.py:17
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 373559dd8f |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete; contract_only |
| Cisco category | unauthorized_tool_use |
| Analyzer | static |
| Evidence check | unavailable |
| Title | Script contacts a destination the documentation never mentions |
Evidence snippet:

```text

```
### LOW · UNDECLARED_NETWORK_DESTINATION · scripts/fetch_kipa_reports.py:17
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | e41f0947e8 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete; contract_only |
| Cisco category | unauthorized_tool_use |
| Analyzer | static |
| Evidence check | unavailable |
| Title | Script contacts a destination the documentation never mentions |
Evidence snippet:

```text

```
### LOW · UNDECLARED_NETWORK_DESTINATION · scripts/fetch_kipa_reports.py:18
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 524955b9fd |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete; contract_only |
| Cisco category | unauthorized_tool_use |
| Analyzer | static |
| Evidence check | unavailable |
| Title | Script contacts a destination the documentation never mentions |
Evidence snippet:

```text

```
### MEDIUM · DATA_EXFIL_NETWORK_REQUESTS · scripts/fetch_kipa_reports.py:53
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 77750d49f0 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete; contract_only |
| Cisco category | data_exfiltration |
| Analyzer | static |
| Evidence check | exact |
| Title | Outbound network request primitives that can transmit data externally |
Evidence snippet:

```text
resp = requests.get(KIPA_API_URL, headers=headers, timeout=REQUEST_TIMEOUT)
```
### LOW · UNDECLARED_NETWORK_DESTINATION · scripts/fetch_kosis_data.py:21
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | a89c859eb0 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete; contract_only |
| Cisco category | unauthorized_tool_use |
| Analyzer | static |
| Evidence check | unavailable |
| Title | Script contacts a destination the documentation never mentions |
Evidence snippet:

```text

```
### MEDIUM · DATA_EXFIL_NETWORK_REQUESTS · scripts/fetch_kosis_data.py:76
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 5c56056cb1 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete; contract_only |
| Cisco category | data_exfiltration |
| Analyzer | static |
| Evidence check | exact |
| Title | Outbound network request primitives that can transmit data externally |
Evidence snippet:

```text
req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
```
### MEDIUM · DATA_EXFIL_NETWORK_REQUESTS · scripts/fetch_kosis_data.py:77
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 1c78b1be84 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete; contract_only |
| Cisco category | data_exfiltration |
| Analyzer | static |
| Evidence check | exact |
| Title | Outbound network request primitives that can transmit data externally |
Evidence snippet:

```text
with urllib.request.urlopen(req, timeout=timeout) as resp:
```
### LOW · UNDECLARED_NETWORK_DESTINATION · scripts/fetch_nia_data.py:17
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 09ae375af5 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete; contract_only |
| Cisco category | unauthorized_tool_use |
| Analyzer | static |
| Evidence check | unavailable |
| Title | Script contacts a destination the documentation never mentions |
Evidence snippet:

```text

```
### CRITICAL · BEHAVIOR_CROSSFILE_ENV_VAR_EXFILTRATION · :
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | ec05b55b23 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| behavioral |
| Scan outcomes | contract_only |
| Cisco category | data_exfiltration |
| Analyzer | behavioral |
| Evidence check | unavailable |
| Title | Cross-file env var exfiltration: 6 files |
Evidence snippet:

```text

```
### CRITICAL · BEHAVIOR_CROSSFILE_EXFILTRATION_CHAIN · :
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | b4ce25a6f2 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| behavioral |
| Scan outcomes | contract_only |
| Cisco category | data_exfiltration |
| Analyzer | behavioral |
| Evidence check | unavailable |
| Title | Cross-file exfiltration chain: 6 files |
Evidence snippet:

```text

```
### CRITICAL · BEHAVIOR_ENV_VAR_EXFILTRATION · scripts/fetch_g2b_data.py:
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 1bb5b12c79 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| behavioral |
| Scan outcomes | contract_only |
| Cisco category | data_exfiltration |
| Analyzer | behavioral |
| Evidence check | unavailable |
| Title | Environment variable access with network calls detected |
Evidence snippet:

```text

```
### CRITICAL · BEHAVIOR_ENV_VAR_EXFILTRATION · scripts/fetch_kosis_data.py:
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | d6b45aea27 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| behavioral |
| Scan outcomes | contract_only |
| Cisco category | data_exfiltration |
| Analyzer | behavioral |
| Evidence check | unavailable |
| Title | Environment variable access with network calls detected |
Evidence snippet:

```text

```
## Other notes

4 metadata-quality / scan-coverage rows: MANIFEST_MISSING_LICENSE (4).
