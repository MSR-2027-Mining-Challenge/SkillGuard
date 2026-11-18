# Skill `mean-reversion-66d706784017`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | agiprolabs/claude-trading-skills |
| SKILL.md path | skills/mean-reversion/SKILL.md |
| Sample stratum | scripts |
| Folder complete in GitSkills | True |
| Coverage | partially_complete: some configurations are COMPLETE, others are partial, contract-only or failed |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 1 | INFO | exit code 0 |
| SKILL.md only \| behavioral | COMPLETE | 1 | INFO | exit code 0 |
| Full folder \| default | COMPLETE | 4 | HIGH | exit code 0 |
| Full folder \| behavioral | CONTRACT_ONLY | 7 | CRITICAL | Cisco reported an analyzer failure (behavioral: FindingContract:BEHAVIOR_CROSSFILE_EXFILTRATION_CHAIN:UNKNOWN_BUNDLED_PYTHON_RULE); Cisco reported an analyzer failure (behavioral: FindingContract:BEHAVIOR_CROSSFILE_ENV_VAR_EXFILTRATION:UNKNOWN_BUNDLED_PYTHON_RULE) |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### MEDIUM · TOOL_ABUSE_UNDECLARED_NETWORK · SKILL.md:
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 6aa3602f36 |
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
### LOW · UNDECLARED_NETWORK_DESTINATION · scripts/mean_reversion_test.py:433
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 1788c0c460 |
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
### HIGH · CORRELATED_SENSITIVE_NETWORK_FLOW · scripts/mean_reversion_test.py:453
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 0a4584c53e |
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
### CRITICAL · BEHAVIOR_CROSSFILE_ENV_VAR_EXFILTRATION · :
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 3819abb03a |
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
### CRITICAL · BEHAVIOR_CROSSFILE_EXFILTRATION_CHAIN · :
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 5402b0fa76 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| behavioral |
| Scan outcomes | contract_only |
| Cisco category | data_exfiltration |
| Analyzer | behavioral |
| Evidence check | unavailable |
| Title | Cross-file exfiltration chain: 1 files |
Evidence snippet:

```text

```
### CRITICAL · BEHAVIOR_ENV_VAR_EXFILTRATION · scripts/mean_reversion_test.py:
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 0473cf9ffe |
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
