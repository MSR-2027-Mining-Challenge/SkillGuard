# Skill `implementing-canary-tokens-for-netw-460e0a897b56`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | 26zl/cybersec-toolkit |
| SKILL.md path | .claude/skills/implementing-canary-tokens-for-network-intrusion/SKILL.md |
| Sample stratum |  |
| Folder complete in GitSkills | True |
| Coverage | partially_complete: some configurations are COMPLETE, others are partial, contract-only or failed |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 0 | SAFE | exit code not recorded (saved before run records existed) |
| SKILL.md only \| behavioral | COMPLETE | 4 | MEDIUM | exit code not recorded (saved before run records existed) |
| Full folder \| default | COMPLETE | 12 | CRITICAL | exit code not recorded (saved before run records existed) |
| Full folder \| behavioral | PARTIAL | 22 | CRITICAL | Cisco reported an analyzer failure (behavioral: FindingContract:BEHAVIOR_CROSSFILE_ENV_VAR_EXFILTRATION:UNKNOWN_BUNDLED_PYTHON_RULE) |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### MEDIUM · MDBLOCK_PYTHON_HTTP_POST · SKILL.md:65
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 05ab50bb1d |
| Provisional label |  |
| Final (human) label |  |
| Configurations | SKILL.md only \| behavioral; Full folder \| behavioral |
| Scan outcomes | complete; partial |
| Cisco category | data_exfiltration |
| Analyzer | behavioral |
| Evidence check | ambiguous |
| Title | Python code block sends HTTP POST request |
Evidence snippet:

```text
response = requests.post("https://canarytokens.org/generate", data={
```
### MEDIUM · MDBLOCK_PYTHON_HTTP_POST · SKILL.md:91
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 2ebd558264 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | SKILL.md only \| behavioral; Full folder \| behavioral |
| Scan outcomes | complete; partial |
| Cisco category | data_exfiltration |
| Analyzer | behavioral |
| Evidence check | ambiguous |
| Title | Python code block sends HTTP POST request |
Evidence snippet:

```text
response = requests.post("https://canarytokens.org/generate", data={
```
### MEDIUM · MDBLOCK_PYTHON_HTTP_POST · SKILL.md:117
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | e1d17f5c02 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | SKILL.md only \| behavioral; Full folder \| behavioral |
| Scan outcomes | complete; partial |
| Cisco category | data_exfiltration |
| Analyzer | behavioral |
| Evidence check | ambiguous |
| Title | Python code block sends HTTP POST request |
Evidence snippet:

```text
response = requests.post("https://canarytokens.org/generate", data={
```
### MEDIUM · MDBLOCK_PYTHON_HTTP_POST · SKILL.md:165
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 903b2d182e |
| Provisional label |  |
| Final (human) label |  |
| Configurations | SKILL.md only \| behavioral; Full folder \| behavioral |
| Scan outcomes | complete; partial |
| Cisco category | data_exfiltration |
| Analyzer | behavioral |
| Evidence check | mismatch |
| Title | Python code block sends HTTP POST request |
Evidence snippet:

```text
requests.post(webhook_url, json=payload, timeout=10)
```
### MEDIUM · TOOL_ABUSE_UNDECLARED_NETWORK · SKILL.md:
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | ceb1332be5 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete; partial |
| Cisco category | unauthorized_tool_use |
| Analyzer | static |
| Evidence check | unavailable |
| Title | Undeclared network usage |
Evidence snippet:

```text

```
### HIGH · CORRELATED_SENSITIVE_NETWORK_FLOW · scripts/agent.py:91
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 0da32bf415 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete; partial |
| Cisco category | data_exfiltration |
| Analyzer | correlation |
| Evidence check | unavailable |
| Title | Sensitive source reaches a network sink |
Evidence snippet:

```text

```
### MEDIUM · DATA_EXFIL_NETWORK_REQUESTS · scripts/agent.py:91
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 0a51704a5a |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete; partial |
| Cisco category | data_exfiltration |
| Analyzer | static |
| Evidence check | exact |
| Title | Outbound network request primitives that can transmit data externally |
Evidence snippet:

```text
resp = requests.post(CANARYTOKENS_API_URL, data=data, timeout=30)
```
### MEDIUM · DATA_EXFIL_NETWORK_REQUESTS · scripts/agent.py:179
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 5d5e7af6c9 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete; partial |
| Cisco category | data_exfiltration |
| Analyzer | static |
| Evidence check | exact |
| Title | Outbound network request primitives that can transmit data externally |
Evidence snippet:

```text
resp = requests.post(url, data=payload, timeout=30)
```
### MEDIUM · DATA_EXFIL_NETWORK_REQUESTS · scripts/agent.py:187
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | a09cd2f0d0 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete; partial |
| Cisco category | data_exfiltration |
| Analyzer | static |
| Evidence check | exact |
| Title | Outbound network request primitives that can transmit data externally |
Evidence snippet:

```text
resp = requests.get(url, params={"auth_token": auth_token}, timeout=30)
```
### MEDIUM · DATA_EXFIL_NETWORK_REQUESTS · scripts/agent.py:195
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 0ade0e9a72 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete; partial |
| Cisco category | data_exfiltration |
| Analyzer | static |
| Evidence check | exact |
| Title | Outbound network request primitives that can transmit data externally |
Evidence snippet:

```text
resp = requests.get(url, params={"auth_token": auth_token}, timeout=30)
```
### HIGH · SECRET_CONNECTION_STRING · scripts/agent.py:331
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 85440d53ad |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete; partial |
| Cisco category | hardcoded_secrets |
| Analyzer | static |
| Evidence check | exact |
| Title | Database connection string with embedded credentials |
Evidence snippet:

```text
"DATABASE_URL=post****db.internal:5432/app",
```
### CRITICAL · DATA_EXFIL_HTTP_POST · scripts/agent.py:402
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | dd3f1f7c83 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete; partial |
| Cisco category | data_exfiltration |
| Analyzer | static |
| Evidence check | exact |
| Title | HTTP POST request that may send data externally |
Evidence snippet:

```text
resp = requests.post(webhook_url, json=payload, timeout=10)
```
### CRITICAL · DATA_EXFIL_HTTP_POST · scripts/agent.py:433
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 727bd7a79b |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete; partial |
| Cisco category | data_exfiltration |
| Analyzer | static |
| Evidence check | exact |
| Title | HTTP POST request that may send data externally |
Evidence snippet:

```text
resp = requests.post(webhook_url, json=payload, timeout=10)
```
### MEDIUM · DATA_EXFIL_NETWORK_REQUESTS · scripts/agent.py:515
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | f406134ddf |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete; partial |
| Cisco category | data_exfiltration |
| Analyzer | static |
| Evidence check | exact |
| Title | Outbound network request primitives that can transmit data externally |
Evidence snippet:

```text
resp = requests.post(siem_url, json=siem_event, headers=headers, timeout=15)
```
### CRITICAL · DATA_EXFIL_SOCKET_CONNECT · scripts/agent.py:683
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 4f2e4ddd1f |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete; partial |
| Cisco category | data_exfiltration |
| Analyzer | static |
| Evidence check | exact |
| Title | Direct socket connection to external server |
Evidence snippet:

```text
resolved = socket.getaddrinfo(token_hostname, None)
```
### MEDIUM · DATA_EXFIL_NETWORK_REQUESTS · scripts/agent.py:700
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | bb1b377987 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete; partial |
| Cisco category | data_exfiltration |
| Analyzer | static |
| Evidence check | exact |
| Title | Outbound network request primitives that can transmit data externally |
Evidence snippet:

```text
resp = requests.get(token_url, timeout=10, allow_redirects=True)
```
### CRITICAL · BEHAVIOR_CROSSFILE_ENV_VAR_EXFILTRATION · :
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 95bf9a7d02 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| behavioral |
| Scan outcomes | partial |
| Cisco category | data_exfiltration |
| Analyzer | behavioral |
| Evidence check | unavailable |
| Title | Cross-file env var exfiltration: 1 files |
Evidence snippet:

```text

```
### CRITICAL · BEHAVIOR_ENV_VAR_EXFILTRATION · scripts/agent.py:
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 0e01b0be12 |
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
### MEDIUM · MDBLOCK_PYTHON_HTTP_POST · references/api-reference.md:24
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | be37152bac |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| behavioral |
| Scan outcomes | partial |
| Cisco category | data_exfiltration |
| Analyzer | behavioral |
| Evidence check | ambiguous |
| Title | Python code block sends HTTP POST request |
Evidence snippet:

```text
resp = requests.post("https://canarytokens.org/generate", data={
```
### MEDIUM · MDBLOCK_PYTHON_HTTP_POST · references/api-reference.md:36
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 35797f1b14 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| behavioral |
| Scan outcomes | partial |
| Cisco category | data_exfiltration |
| Analyzer | behavioral |
| Evidence check | ambiguous |
| Title | Python code block sends HTTP POST request |
Evidence snippet:

```text
resp = requests.post("https://canarytokens.org/generate", data={
```
### MEDIUM · MDBLOCK_PYTHON_HTTP_POST · references/api-reference.md:47
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 5e8eb00ebe |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| behavioral |
| Scan outcomes | partial |
| Cisco category | data_exfiltration |
| Analyzer | behavioral |
| Evidence check | ambiguous |
| Title | Python code block sends HTTP POST request |
Evidence snippet:

```text
resp = requests.post("https://canarytokens.org/generate", data={
```
### MEDIUM · MDBLOCK_PYTHON_HTTP_POST · references/api-reference.md:87
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 4cc08ece66 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| behavioral |
| Scan outcomes | partial |
| Cisco category | data_exfiltration |
| Analyzer | behavioral |
| Evidence check | mismatch |
| Title | Python code block sends HTTP POST request |
Evidence snippet:

```text
resp = requests.post(url, data={
```
## Other notes

0 metadata-quality / scan-coverage rows: .
