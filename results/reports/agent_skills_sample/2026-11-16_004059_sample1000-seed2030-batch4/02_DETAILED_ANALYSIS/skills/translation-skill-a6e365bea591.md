# Skill `translation-skill-a6e365bea591`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | codata/the-minority-report |
| SKILL.md path | translation-skill/SKILL.md |
| Sample stratum | scripts |
| Folder complete in GitSkills | False |
| Coverage | no_complete_scan: Cisco ran, but no configuration produced a COMPLETE scan |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | PARTIAL | 1 | INFO | Cisco reported an analyzer failure (skill_loader: SkillLoadError:MISSING_REQUIRED_MANIFEST_FIELD) |
| SKILL.md only \| behavioral | PARTIAL | 1 | INFO | Cisco reported an analyzer failure (skill_loader: SkillLoadError:MISSING_REQUIRED_MANIFEST_FIELD) |
| Full folder \| default | PARTIAL | 24 | CRITICAL | Cisco reported an analyzer failure (skill_loader: SkillLoadError:MISSING_REQUIRED_MANIFEST_FIELD) |
| Full folder \| behavioral | PARTIAL | 28 | CRITICAL | Cisco reported an analyzer failure (behavioral: FindingContract:BEHAVIOR_CROSSFILE_EXFILTRATION_CHAIN:UNKNOWN_BUNDLED_PYTHON_RULE); Cisco reported an analyzer failure (behavioral: FindingContract:BEHAVIOR_CROSSFILE_ENV_VAR_EXFILTRATION:UNKNOWN_BUNDLED_PYTHON_RULE); Cisco reported an analyzer failure (skill_loader: SkillLoadError:MISSING_REQUIRED_MANIFEST_FIELD) |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### LOW · FILE_MAGIC_MISMATCH · prompts/keyword_extraction_prompt.md:
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 3970d6e89b |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | partial |
| Cisco category | obfuscation |
| Analyzer | static |
| Evidence check | unavailable |
| Title | File extension does not match actual content type |
Evidence snippet:

```text

```
### LOW · FILE_MAGIC_MISMATCH · prompts/metrics_extraction_prompt.md:
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 319dac3b36 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | partial |
| Cisco category | obfuscation |
| Analyzer | static |
| Evidence check | unavailable |
| Title | File extension does not match actual content type |
Evidence snippet:

```text

```
### LOW · FILE_MAGIC_MISMATCH · prompts/proofread_prompt.md:
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 02e802f8b7 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | partial |
| Cisco category | obfuscation |
| Analyzer | static |
| Evidence check | unavailable |
| Title | File extension does not match actual content type |
Evidence snippet:

```text

```
### MEDIUM · DATA_EXFIL_NETWORK_REQUESTS · scripts/api.py:149
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | d052466ab5 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | partial |
| Cisco category | data_exfiltration |
| Analyzer | static |
| Evidence check | exact |
| Title | Outbound network request primitives that can transmit data externally |
Evidence snippet:

```text
r = requests.get(ollama_host, timeout=2)
```
### MEDIUM · DATA_EXFIL_NETWORK_REQUESTS · scripts/api.py:159
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 79a7a25798 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | partial |
| Cisco category | data_exfiltration |
| Analyzer | static |
| Evidence check | exact |
| Title | Outbound network request primitives that can transmit data externally |
Evidence snippet:

```text
r = requests.get(ollama_keywords, timeout=2)
```
### CRITICAL · COMMAND_INJECTION_OS_SYSTEM · scripts/batch_update_hips.py:50
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | fb3c15d71a |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | partial |
| Cisco category | command_injection |
| Analyzer | static |
| Evidence check | exact |
| Title | Shell command execution with string formatting (potential injection) |
Evidence snippet:

```text
os.system(f"find {hips_root} -name 'final_translations.csv' -exec chmod o+r {{}} \\;")
```
### LOW · UNDECLARED_NETWORK_DESTINATION · scripts/generate_central_croissant.py:390
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 9a48ec2a97 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | partial |
| Cisco category | unauthorized_tool_use |
| Analyzer | static |
| Evidence check | unavailable |
| Title | Script contacts a destination the documentation never mentions |
Evidence snippet:

```text

```
### LOW · UNDECLARED_NETWORK_DESTINATION · scripts/generate_central_croissant.py:391
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 60a2a0f912 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | partial |
| Cisco category | unauthorized_tool_use |
| Analyzer | static |
| Evidence check | unavailable |
| Title | Script contacts a destination the documentation never mentions |
Evidence snippet:

```text

```
### LOW · UNDECLARED_NETWORK_DESTINATION · scripts/generate_central_croissant.py:399
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | a677e54c97 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | partial |
| Cisco category | unauthorized_tool_use |
| Analyzer | static |
| Evidence check | unavailable |
| Title | Script contacts a destination the documentation never mentions |
Evidence snippet:

```text

```
### LOW · UNDECLARED_NETWORK_DESTINATION · scripts/generate_central_croissant.py:401
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 0868766518 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | partial |
| Cisco category | unauthorized_tool_use |
| Analyzer | static |
| Evidence check | unavailable |
| Title | Script contacts a destination the documentation never mentions |
Evidence snippet:

```text

```
### LOW · UNDECLARED_NETWORK_DESTINATION · scripts/generate_central_croissant.py:428
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 715571b91f |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | partial |
| Cisco category | unauthorized_tool_use |
| Analyzer | static |
| Evidence check | unavailable |
| Title | Script contacts a destination the documentation never mentions |
Evidence snippet:

```text

```
### LOW · UNDECLARED_NETWORK_DESTINATION · scripts/generate_central_croissant.py:435
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 6b8aad80ba |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | partial |
| Cisco category | unauthorized_tool_use |
| Analyzer | static |
| Evidence check | unavailable |
| Title | Script contacts a destination the documentation never mentions |
Evidence snippet:

```text

```
### LOW · UNDECLARED_NETWORK_DESTINATION · scripts/ontoportal.py:13
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 0606d42f87 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | partial |
| Cisco category | unauthorized_tool_use |
| Analyzer | static |
| Evidence check | unavailable |
| Title | Script contacts a destination the documentation never mentions |
Evidence snippet:

```text

```
### MEDIUM · DATA_EXFIL_NETWORK_REQUESTS · scripts/ontoportal.py:51
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 34bff627f3 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | partial |
| Cisco category | data_exfiltration |
| Analyzer | static |
| Evidence check | exact |
| Title | Outbound network request primitives that can transmit data externally |
Evidence snippet:

```text
response = requests.get(endpoint, headers=self.headers, params=params)
```
### MEDIUM · DATA_EXFIL_NETWORK_REQUESTS · scripts/ontoportal.py:76
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 2f3aaad122 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | partial |
| Cisco category | data_exfiltration |
| Analyzer | static |
| Evidence check | exact |
| Title | Outbound network request primitives that can transmit data externally |
Evidence snippet:

```text
response = requests.get(term_uri, headers=self.headers)
```
### MEDIUM · DATA_EXFIL_NETWORK_REQUESTS · scripts/ontoportal.py:113
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | a6ddd14cf7 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | partial |
| Cisco category | data_exfiltration |
| Analyzer | static |
| Evidence check | exact |
| Title | Outbound network request primitives that can transmit data externally |
Evidence snippet:

```text
response = requests.get(endpoint, headers=sparql_headers, params=params)
```
### LOW · UNDECLARED_NETWORK_DESTINATION · scripts/orchestrator.py:42
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | d86ad45fbc |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | partial |
| Cisco category | unauthorized_tool_use |
| Analyzer | static |
| Evidence check | unavailable |
| Title | Script contacts a destination the documentation never mentions |
Evidence snippet:

```text

```
### MEDIUM · DATA_EXFIL_ENV_VARS · scripts/orchestrator.py:118
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 8444c4b899 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | partial |
| Cisco category | data_exfiltration |
| Analyzer | static |
| Evidence check | exact |
| Title | Bulk process environment snapshot can expose credentials and tokens |
Evidence snippet:

```text
env = os.environ.copy()
```
### MEDIUM · DATA_EXFIL_NETWORK_REQUESTS · scripts/orchestrator.py:265
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | c5f3c27edc |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | partial |
| Cisco category | data_exfiltration |
| Analyzer | static |
| Evidence check | exact |
| Title | Outbound network request primitives that can transmit data externally |
Evidence snippet:

```text
resp = requests.get(url, headers=headers)
```
### MEDIUM · DATA_EXFIL_NETWORK_REQUESTS · scripts/orchestrator.py:297
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 1650381861 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | partial |
| Cisco category | data_exfiltration |
| Analyzer | static |
| Evidence check | exact |
| Title | Outbound network request primitives that can transmit data externally |
Evidence snippet:

```text
response = requests.get(index_url, headers=headers)
```
### MEDIUM · DATA_EXFIL_NETWORK_REQUESTS · scripts/orchestrator.py:666
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 43a92a1980 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | partial |
| Cisco category | data_exfiltration |
| Analyzer | static |
| Evidence check | exact |
| Title | Outbound network request primitives that can transmit data externally |
Evidence snippet:

```text
response = requests.post(f"{ollama_host}/api/generate", json=payload)
```
### LOW · UNDECLARED_NETWORK_DESTINATION · tests/test_orchestrator.py:36
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 5a875198ce |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | partial |
| Cisco category | unauthorized_tool_use |
| Analyzer | static |
| Evidence check | unavailable |
| Title | Script contacts a destination the documentation never mentions |
Evidence snippet:

```text

```
### LOW · UNDECLARED_NETWORK_DESTINATION · tests/test_orchestrator.py:40
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 1a2962f729 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | partial |
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
| Review ID | 8963bddaa9 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| behavioral |
| Scan outcomes | partial |
| Cisco category | data_exfiltration |
| Analyzer | behavioral |
| Evidence check | unavailable |
| Title | Cross-file env var exfiltration: 3 files |
Evidence snippet:

```text

```
### CRITICAL · BEHAVIOR_CROSSFILE_EXFILTRATION_CHAIN · :
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 5e969e99b1 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| behavioral |
| Scan outcomes | partial |
| Cisco category | data_exfiltration |
| Analyzer | behavioral |
| Evidence check | unavailable |
| Title | Cross-file exfiltration chain: 5 files |
Evidence snippet:

```text

```
### CRITICAL · BEHAVIOR_ENV_VAR_EXFILTRATION · scripts/api.py:
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 1afecd9603 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| behavioral |
| Scan outcomes | partial |
| Cisco category | data_exfiltration |
| Analyzer | behavioral |
| Evidence check | unavailable |
| Title | Environment variable access with network calls detected |
Evidence snippet:

```text

```
### CRITICAL · BEHAVIOR_ENV_VAR_EXFILTRATION · scripts/orchestrator.py:
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 2eb8bb7c59 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| behavioral |
| Scan outcomes | partial |
| Cisco category | data_exfiltration |
| Analyzer | behavioral |
| Evidence check | unavailable |
| Title | Environment variable access with network calls detected |
Evidence snippet:

```text

```
## Other notes

4 metadata-quality / scan-coverage rows: SKILL_LOAD_FALLBACK_USED (4).
