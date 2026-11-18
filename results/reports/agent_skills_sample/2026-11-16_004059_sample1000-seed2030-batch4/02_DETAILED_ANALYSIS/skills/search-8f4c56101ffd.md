# Skill `search-8f4c56101ffd`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | docxology/template |
| SKILL.md path | infrastructure/search/SKILL.md |
| Sample stratum | scripts |
| Folder complete in GitSkills | True |
| Coverage | partially_complete: some configurations are COMPLETE, others are partial, contract-only or failed |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 2 | LOW | exit code 0 |
| SKILL.md only \| behavioral | COMPLETE | 2 | LOW | exit code 0 |
| Full folder \| default | COMPLETE | 29 | MEDIUM | exit code 0 |
| Full folder \| behavioral | CONTRACT_ONLY | 32 | CRITICAL | Cisco reported an analyzer failure (behavioral: FindingContract:BEHAVIOR_CROSSFILE_EXFILTRATION_CHAIN:UNKNOWN_BUNDLED_PYTHON_RULE); Cisco reported an analyzer failure (behavioral: FindingContract:BEHAVIOR_CROSSFILE_ENV_VAR_EXFILTRATION:UNKNOWN_BUNDLED_PYTHON_RULE) |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### MEDIUM · LAZY_LOAD_DEEP_NESTING · SKILL.md:
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | c9dadd7d8b |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete; contract_only |
| Cisco category | obfuscation |
| Analyzer | static |
| Evidence check | unavailable |
| Title | Deeply nested file references detected |
Evidence snippet:

```text

```
### MEDIUM · SOCIAL_ENG_MISLEADING_DESC · SKILL.md:
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | bf1c0d4b3b |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete; contract_only |
| Cisco category | social_engineering |
| Analyzer | static |
| Evidence check | unavailable |
| Title | Potential description-behavior mismatch |
Evidence snippet:

```text

```
### MEDIUM · TOOL_ABUSE_UNDECLARED_NETWORK · SKILL.md:
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 0d5454101e |
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
### MEDIUM · DATA_EXFIL_NETWORK_REQUESTS · connectors/http.py:150
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 8f562711cc |
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
return urllib.request.Request(url, headers=headers)
```
### MEDIUM · DATA_EXFIL_NETWORK_REQUESTS · connectors/http.py:157
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 20e96752d4 |
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
with urllib.request.urlopen(req, timeout=self.timeout) as resp:  # nosec B310 — URLs are hard-coded to known public science APIs (OpenAlex, arXiv, etc.)
```
### LOW · UNDECLARED_NETWORK_DESTINATION · connectors/impl/biorxiv.py:3
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | ee4acaa83c |
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
### LOW · UNDECLARED_NETWORK_DESTINATION · connectors/impl/biorxiv.py:107
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | e3c000e36c |
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
### LOW · UNDECLARED_NETWORK_DESTINATION · connectors/impl/europepmc.py:3
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 5138b87f25 |
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
### LOW · UNDECLARED_NETWORK_DESTINATION · connectors/impl/europepmc.py:19
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 866ee4e424 |
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
### LOW · UNDECLARED_NETWORK_DESTINATION · connectors/impl/openalex.py:3
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | a73e1bf497 |
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
### LOW · UNDECLARED_NETWORK_DESTINATION · connectors/impl/pdb.py:3
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | eeabe955dd |
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
### LOW · UNDECLARED_NETWORK_DESTINATION · connectors/impl/pdb.py:21
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | c8c0db9c2f |
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
### LOW · UNDECLARED_NETWORK_DESTINATION · connectors/impl/pdb.py:97
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | be4818610a |
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
### LOW · UNDECLARED_NETWORK_DESTINATION · connectors/impl/semantic_scholar.py:3
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | d5ab22e9c9 |
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
### LOW · UNDECLARED_NETWORK_DESTINATION · connectors/impl/semantic_scholar.py:106
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 43682d0f40 |
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
### LOW · UNDECLARED_NETWORK_DESTINATION · connectors/impl/uniprot.py:3
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | f69dbc9e7d |
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
### LOW · UNDECLARED_NETWORK_DESTINATION · connectors/impl/uniprot.py:19
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | fae47d4c1c |
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
### LOW · UNDECLARED_NETWORK_DESTINATION · connectors/types.py:38
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | eb1890cdb8 |
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
### MEDIUM · DATA_EXFIL_NETWORK_REQUESTS · exa/http.py:67
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 39c603cdf2 |
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
req = urllib.request.Request(url, data=body, headers=dict(headers), method="POST")
```
### MEDIUM · DATA_EXFIL_NETWORK_REQUESTS · exa/http.py:69
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | ae22f305fc |
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
with urllib.request.urlopen(req, timeout=timeout) as resp:  # nosec B310
```
### LOW · UNDECLARED_NETWORK_DESTINATION · literature/crossref_backend.py:25
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | f37bcb486c |
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
### MEDIUM · DATA_EXFIL_NETWORK_REQUESTS · literature/http_client.py:76
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 4c7f8efdae |
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
req = urllib.request.Request(url, headers=dict(headers or {}))
```
### MEDIUM · DATA_EXFIL_NETWORK_REQUESTS · literature/http_client.py:78
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 3971d743e9 |
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
with urllib.request.urlopen(req, timeout=timeout) as resp:  # nosec B310
```
### MEDIUM · DATA_EXFIL_NETWORK_REQUESTS · literature/http_client.py:110
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | e7fe88311e |
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
req = urllib.request.Request(url, headers=dict(headers or {}))
```
### MEDIUM · DATA_EXFIL_NETWORK_REQUESTS · literature/http_client.py:112
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 4fbfc6d6c6 |
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
with urllib.request.urlopen(req, timeout=timeout) as resp:  # nosec B310
```
### MEDIUM · DATA_EXFIL_NETWORK_REQUESTS · literature/http_client.py:146
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 4c7a87250c |
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
req = urllib.request.Request(url, data=body, headers=hdrs, method="POST")
```
### MEDIUM · DATA_EXFIL_NETWORK_REQUESTS · literature/http_client.py:148
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | e06fec52a6 |
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
with urllib.request.urlopen(req, timeout=timeout) as resp:  # nosec B310
```
### CRITICAL · BEHAVIOR_CROSSFILE_ENV_VAR_EXFILTRATION · :
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 40eabdd36f |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| behavioral |
| Scan outcomes | contract_only |
| Cisco category | data_exfiltration |
| Analyzer | behavioral |
| Evidence check | unavailable |
| Title | Cross-file env var exfiltration: 4 files |
Evidence snippet:

```text

```
### CRITICAL · BEHAVIOR_CROSSFILE_EXFILTRATION_CHAIN · :
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | bb3d998550 |
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
### HIGH · MDBLOCK_PYTHON_EVAL_EXEC · exa/README.md:43
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 3031154f49 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| behavioral |
| Scan outcomes | contract_only |
| Cisco category | command_injection |
| Analyzer | behavioral |
| Evidence check | mismatch |
| Title | Python code block uses eval/exec |
Evidence snippet:

```text
# Raw retrieval (token-efficient highlights — the default)
```
## Other notes

8 metadata-quality / scan-coverage rows: MANIFEST_DESCRIPTION_TOO_LONG (4), MANIFEST_MISSING_LICENSE (4).
