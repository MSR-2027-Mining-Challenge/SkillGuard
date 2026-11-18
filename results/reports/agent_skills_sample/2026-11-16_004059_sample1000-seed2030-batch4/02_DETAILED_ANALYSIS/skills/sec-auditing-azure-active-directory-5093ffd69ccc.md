# Skill `sec-auditing-azure-active-directory-5093ffd69ccc`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | Mutfak-Yazilimevi/.github |
| SKILL.md path | project-template/.claude/skills/sec-auditing-azure-active-directory-configuration/SKILL.md |
| Sample stratum | scripts |
| Folder complete in GitSkills | True |
| Coverage | partially_complete: some configurations are COMPLETE, others are partial, contract-only or failed |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 0 | SAFE | exit code 0 |
| SKILL.md only \| behavioral | COMPLETE | 0 | SAFE | exit code 0 |
| Full folder \| default | COMPLETE | 2 | MEDIUM | exit code 0 |
| Full folder \| behavioral | CONTRACT_ONLY | 4 | CRITICAL | Cisco reported an analyzer failure (behavioral: FindingContract:BEHAVIOR_CROSSFILE_ENV_VAR_EXFILTRATION:UNKNOWN_BUNDLED_PYTHON_RULE) |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### MEDIUM · TOOL_ABUSE_UNDECLARED_NETWORK · SKILL.md:
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | a3a7c0ff7c |
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
### MEDIUM · DATA_EXFIL_NETWORK_REQUESTS · scripts/agent.py:23
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 78db1b3691 |
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
resp = requests.get(url, headers=headers, params=params, timeout=30)
```
### CRITICAL · BEHAVIOR_CROSSFILE_ENV_VAR_EXFILTRATION · :
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | e62d6df103 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| behavioral |
| Scan outcomes | contract_only |
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
| Review ID | a251fb181f |
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

0 metadata-quality / scan-coverage rows: .
