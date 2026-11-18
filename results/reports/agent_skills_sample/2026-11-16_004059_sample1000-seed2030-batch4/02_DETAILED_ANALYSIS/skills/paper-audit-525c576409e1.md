# Skill `paper-audit-525c576409e1`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | brycewang-stanford/Auto-Empirical-Research-Skills |
| SKILL.md path | skills/35-bahayonghang-academic-writing-skills/skills/paper-audit/SKILL.md |
| Sample stratum | scripts |
| Folder complete in GitSkills | False |
| Coverage | complete: every planned configuration produced a COMPLETE scan |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 1 | INFO | exit code 0 |
| SKILL.md only \| behavioral | COMPLETE | 1 | INFO | exit code 0 |
| Full folder \| default | COMPLETE | 14 | HIGH | exit code 0 |
| Full folder \| behavioral | COMPLETE | 14 | HIGH | exit code 0 |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### HIGH · ALLOWED_TOOLS_BASH_VIOLATION · SKILL.md:
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 845477aa09 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | unauthorized_tool_use |
| Analyzer | static |
| Evidence check | unavailable |
| Title | Code executes bash but Bash tool not in allowed-tools |
Evidence snippet:

```text

```
### MEDIUM · ALLOWED_TOOLS_NETWORK_USAGE · SKILL.md:
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 33201691fc |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | unauthorized_tool_use |
| Analyzer | static |
| Evidence check | unavailable |
| Title | Code makes network requests |
Evidence snippet:

```text

```
### MEDIUM · SOCIAL_ENG_MISLEADING_DESC · SKILL.md:
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 80a1a076bf |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
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
| Review ID | 26113d61e2 |
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
### LOW · UNDECLARED_NETWORK_DESTINATION · scripts/literature_search.py:65
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 080f9e334f |
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
### MEDIUM · DATA_EXFIL_NETWORK_REQUESTS · scripts/literature_search.py:88
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 25990c6c99 |
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
req = urllib.request.Request(url, headers=headers)
```
### MEDIUM · DATA_EXFIL_NETWORK_REQUESTS · scripts/literature_search.py:89
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 267c2c9bca |
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
with urllib.request.urlopen(req, timeout=15) as resp:
```
### LOW · UNDECLARED_NETWORK_DESTINATION · scripts/literature_search.py:125
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 3eae580bba |
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
### MEDIUM · DATA_EXFIL_NETWORK_REQUESTS · scripts/literature_search.py:141
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 8de61438a5 |
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
req = urllib.request.Request(url)
```
### MEDIUM · DATA_EXFIL_NETWORK_REQUESTS · scripts/literature_search.py:142
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 355388225c |
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
with urllib.request.urlopen(req, timeout=15) as resp:
```
### LOW · UNDECLARED_NETWORK_DESTINATION · scripts/literature_search.py:202
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 69e5f1bc0f |
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
### MEDIUM · DATA_EXFIL_NETWORK_REQUESTS · scripts/literature_search.py:223
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 6e99e357e8 |
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
### MEDIUM · DATA_EXFIL_NETWORK_REQUESTS · scripts/literature_search.py:229
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 672fe79d3b |
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
with urllib.request.urlopen(req, timeout=20) as resp:
```
## Other notes

4 metadata-quality / scan-coverage rows: MANIFEST_MISSING_LICENSE (4).
