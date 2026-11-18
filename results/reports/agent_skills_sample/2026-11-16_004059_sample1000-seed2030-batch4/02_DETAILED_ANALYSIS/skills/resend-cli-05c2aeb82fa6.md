# Skill `resend-cli-05c2aeb82fa6`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | jchademwiri/tender-track-360 |
| SKILL.md path | .claude/skills/resend-cli/SKILL.md |
| Sample stratum | supporting_no_scripts |
| Folder complete in GitSkills | True |
| Coverage | complete: every planned configuration produced a COMPLETE scan |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 3 | HIGH | exit code 0 |
| SKILL.md only \| behavioral | COMPLETE | 3 | HIGH | exit code 0 |
| Full folder \| default | COMPLETE | 5 | HIGH | exit code 0 |
| Full folder \| behavioral | COMPLETE | 5 | HIGH | exit code 0 |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### LOW · PIPELINE_TAINT_FLOW · SKILL.md:1
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | b16326bc8a |
| Provisional label |  |
| Final (human) label |  |
| Configurations | SKILL.md only \| default; SKILL.md only \| behavioral; Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | data_exfiltration |
| Analyzer | pipeline |
| Evidence check | mismatch |
| Title | Dangerous data flow in command pipeline |
Evidence snippet:

```text
curl -fsSL https://resend.com/install.sh | bash
```
### HIGH · CORRELATED_NETWORK_EXECUTION_FLOW · SKILL.md:51
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 3968ecf126 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | SKILL.md only \| default; SKILL.md only \| behavioral; Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | command_injection |
| Analyzer | correlation |
| Evidence check | unavailable |
| Title | Network-derived content reaches code execution |
Evidence snippet:

```text

```
### LOW · PIPELINE_TAINT_FLOW · references/workflows.md:2
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 8cadaaaf28 |
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
curl -fsSL https://resend.com/install.sh | bash   # Linux / macOS
```
### LOW · PIPELINE_TAINT_FLOW · references/workflows.md:5
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | d48aa6781e |
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
irm https://resend.com/install.ps1 | iex           # Windows PowerShell
```
## Other notes

0 metadata-quality / scan-coverage rows: .
