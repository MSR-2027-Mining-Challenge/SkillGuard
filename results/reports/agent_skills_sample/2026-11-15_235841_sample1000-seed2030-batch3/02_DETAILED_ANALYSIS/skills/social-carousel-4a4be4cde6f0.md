# Skill `social-carousel-4a4be4cde6f0`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | diegoclair/skills |
| SKILL.md path | social-carousel/SKILL.md |
| Sample stratum | scripts |
| Folder complete in GitSkills | False |
| Coverage | complete: every planned configuration produced a COMPLETE scan |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 1 | INFO | exit code 0 |
| SKILL.md only \| behavioral | COMPLETE | 1 | INFO | exit code 0 |
| Full folder \| default | COMPLETE | 6 | HIGH | exit code 0 |
| Full folder \| behavioral | COMPLETE | 6 | HIGH | exit code 0 |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### LOW · PIPELINE_TAINT_FLOW · README.md:1
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 596779424e |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | data_exfiltration |
| Analyzer | pipeline |
| Evidence check | mismatch |
| Title | Dangerous data flow in command pipeline |
Evidence snippet:

```text
curl -fsSL https://raw.githubusercontent.com/diegoclair/skills/main/social-carousel/install/install.sh | bash
```
### HIGH · ALLOWED_TOOLS_BASH_VIOLATION · SKILL.md:
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | bf1091430e |
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
### HIGH · PIPELINE_TAINT_FLOW · cli/cmd_postinstall.go:1
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 4a01c45bdd |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | data_exfiltration |
| Analyzer | pipeline |
| Evidence check | mismatch |
| Title | Dangerous data flow in command pipeline |
Evidence snippet:

```text
curl | bash
```
### HIGH · CORRELATED_NETWORK_EXECUTION_FLOW · install/install.sh:19
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | a23aa2ace4 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | command_injection |
| Analyzer | correlation |
| Evidence check | unavailable |
| Title | Network-derived content reaches code execution |
Evidence snippet:

```text

```
### HIGH · PIPELINE_TAINT_FLOW · research/B-landscape-competitivo.md:1
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 582f576768 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | data_exfiltration |
| Analyzer | pipeline |
| Evidence check | ambiguous |
| Title | Dangerous data flow in command pipeline |
Evidence snippet:

```text
curl | bash
```
## Other notes

4 metadata-quality / scan-coverage rows: MANIFEST_MISSING_LICENSE (4).
