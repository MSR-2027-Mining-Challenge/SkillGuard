# Skill `pr-review-d32033bd5783`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | JocysCom/FocusLogger |
| SKILL.md path | .claude/skills/pr-review/SKILL.md |
| Sample stratum | scripts |
| Folder complete in GitSkills | False |
| Coverage | partially_complete: some configurations are COMPLETE, others are partial, contract-only or failed |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 1 | INFO | exit code 0 |
| SKILL.md only \| behavioral | COMPLETE | 1 | INFO | exit code 0 |
| Full folder \| default | COMPLETE | 17 | CRITICAL | exit code 0 |
| Full folder \| behavioral | CONTRACT_ONLY | 20 | CRITICAL | Cisco reported an analyzer failure (behavioral: FindingContract:BEHAVIOR_CROSSFILE_EXFILTRATION_CHAIN:UNKNOWN_BUNDLED_PYTHON_RULE); Cisco reported an analyzer failure (behavioral: FindingContract:BEHAVIOR_CROSSFILE_ENV_VAR_EXFILTRATION:UNKNOWN_BUNDLED_PYTHON_RULE) |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### MEDIUM · TOOL_ABUSE_UNDECLARED_NETWORK · SKILL.md:
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 7be970eeef |
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
### LOW · SUPPLY_CHAIN_UNPINNED_DEPENDENCY · scripts/requirements.txt:1
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 5c3fd28227 |
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
requests>=2.28.0
```
### LOW · SUPPLY_CHAIN_UNPINNED_DEPENDENCY · scripts/requirements.txt:2
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 833fdd106d |
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
requests-ntlm>=1.2.0
```
### LOW · SUPPLY_CHAIN_UNPINNED_DEPENDENCY · scripts/requirements.txt:7
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 011852845e |
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
Pillow>=10.0.0
```
### LOW · UNDECLARED_NETWORK_DESTINATION · scripts/review_config.py:162
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 19c881900f |
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
### MEDIUM · DATA_EXFIL_NETWORK_REQUESTS · scripts/review_config.py:461
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 0d17d6f9c7 |
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
response = requests.request(method, url, **kwargs)
```
### MEDIUM · DATA_EXFIL_NETWORK_REQUESTS · scripts/s02_get_azure_devops_info.py:39
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 0957709b66 |
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
response = requests.get(url, **kwargs)
```
### MEDIUM · DATA_EXFIL_NETWORK_REQUESTS · scripts/s03_extract_attachments.py:151
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 471c359786 |
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
response = requests.get(url, **kwargs)
```
### CRITICAL · COMMAND_INJECTION_OS_SYSTEM · scripts/s06_export_diff_artifacts.py:45
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 9f1ff0f0ea |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete; contract_only |
| Cisco category | command_injection |
| Analyzer | static |
| Evidence check | exact |
| Title | Shell command execution with string formatting (potential injection) |
Evidence snippet:

```text
result = subprocess.run(
```
### CRITICAL · COMMAND_INJECTION_OS_SYSTEM · scripts/s06_export_diff_artifacts.py:60
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | afc48fe2b8 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete; contract_only |
| Cisco category | command_injection |
| Analyzer | static |
| Evidence check | exact |
| Title | Shell command execution with string formatting (potential injection) |
Evidence snippet:

```text
result = subprocess.run(
```
### MEDIUM · DATA_EXFIL_NETWORK_REQUESTS · scripts/s09_upsert_review_attachments.py:86
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 9aa02514c3 |
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
response = requests.post(url, **kwargs)
```
### MEDIUM · DATA_EXFIL_NETWORK_REQUESTS · scripts/s10_upsert_review_comment.py:47
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 25c1645098 |
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
response = requests.request(method, url, **kwargs)
```
### HIGH · CORRELATED_SENSITIVE_NETWORK_FLOW · scripts/s10_upsert_review_comment.py:69
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 8a02fb14b7 |
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
### MEDIUM · DATA_EXFIL_NETWORK_REQUESTS · scripts/s10_upsert_review_comment.py:69
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | d2972fe9fd |
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
response = requests.request(method, url, **kwargs)
```
### MEDIUM · DATA_EXFIL_NETWORK_REQUESTS · scripts/s11_upsert_pr_description.py:67
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 2c1801ffe1 |
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
response = requests.request(method, url, **kwargs)
```
### MEDIUM · DATA_EXFIL_NETWORK_REQUESTS · scripts/s12_upsert_suggestion_threads.py:48
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | b855d7ee8a |
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
response = requests.request(method, url, **kwargs)
```
### CRITICAL · BEHAVIOR_CROSSFILE_ENV_VAR_EXFILTRATION · :
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 97a7d9527f |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| behavioral |
| Scan outcomes | contract_only |
| Cisco category | data_exfiltration |
| Analyzer | behavioral |
| Evidence check | unavailable |
| Title | Cross-file env var exfiltration: 7 files |
Evidence snippet:

```text

```
### CRITICAL · BEHAVIOR_CROSSFILE_EXFILTRATION_CHAIN · :
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 3ec67c0be4 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| behavioral |
| Scan outcomes | contract_only |
| Cisco category | data_exfiltration |
| Analyzer | behavioral |
| Evidence check | unavailable |
| Title | Cross-file exfiltration chain: 8 files |
Evidence snippet:

```text

```
### CRITICAL · BEHAVIOR_ENV_VAR_EXFILTRATION · scripts/s10_upsert_review_comment.py:
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | c48975e97f |
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
