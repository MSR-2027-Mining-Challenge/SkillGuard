# Skill `implementing-patch-management-workf-db65d28e0d7a`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | Molly-agi/Molly-Core |
| SKILL.md path | src/skills/registry/skills/cybersecurity/skills/implementing-patch-management-workflow/SKILL.md |
| Sample stratum | scripts |
| Folder complete in GitSkills | True |
| Coverage | complete: every planned configuration produced a COMPLETE scan |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 1 | HIGH | exit code 0 |
| SKILL.md only \| behavioral | COMPLETE | 2 | HIGH | exit code 0 |
| Full folder \| default | COMPLETE | 4 | HIGH | exit code 0 |
| Full folder \| behavioral | COMPLETE | 7 | HIGH | exit code 0 |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### HIGH · ACTIVE_DYNAMIC_EXECUTION · SKILL.md:144
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 7b3227ba33 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | SKILL.md only \| default; SKILL.md only \| behavioral; Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | command_injection |
| Analyzer | static |
| Evidence check | exact |
| Title | Active instruction invokes dynamic code or process execution |
Evidence snippet:

```text
result = subprocess.run(
```
### MEDIUM · MDBLOCK_PYTHON_SUBPROCESS · SKILL.md:114
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | d73a7c3033 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | SKILL.md only \| behavioral; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | command_injection |
| Analyzer | behavioral |
| Evidence check | ambiguous |
| Title | Python code block executes shell commands |
Evidence snippet:

```text
result = subprocess.run(
```
### MEDIUM · TOOL_ABUSE_UNDECLARED_NETWORK · SKILL.md:
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 277d6260b7 |
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
### LOW · UNDECLARED_NETWORK_DESTINATION · scripts/agent.py:137
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 265accbb29 |
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
### MEDIUM · DATA_EXFIL_NETWORK_REQUESTS · scripts/agent.py:139
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 23a091a0ff |
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
resp = requests.get(kev_url, timeout=30)
```
### MEDIUM · MDBLOCK_PYTHON_SUBPROCESS · references/api-reference.md:113
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | f60c4995bc |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | command_injection |
| Analyzer | behavioral |
| Evidence check | mismatch |
| Title | Python code block executes shell commands |
Evidence snippet:

```text
result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
```
### MEDIUM · MDBLOCK_PYTHON_SUBPROCESS · references/api-reference.md:125
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | d3219c23aa |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | command_injection |
| Analyzer | behavioral |
| Evidence check | mismatch |
| Title | Python code block executes shell commands |
Evidence snippet:

```text
result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
```
## Other notes

0 metadata-quality / scan-coverage rows: .
