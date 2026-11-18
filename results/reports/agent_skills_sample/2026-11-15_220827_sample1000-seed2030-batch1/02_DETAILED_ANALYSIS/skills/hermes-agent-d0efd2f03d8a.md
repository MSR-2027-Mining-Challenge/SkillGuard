# Skill `hermes-agent-d0efd2f03d8a`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | AlvaroBiano/bianinho-backup-1777760438 |
| SKILL.md path | skills/autonomous-ai-agents/hermes-agent/SKILL.md |
| Sample stratum | supporting_no_scripts |
| Folder complete in GitSkills | True |
| Coverage | complete: every planned configuration produced a COMPLETE scan |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 3 | HIGH | exit code 0 |
| SKILL.md only \| behavioral | COMPLETE | 4 | HIGH | exit code 0 |
| Full folder \| default | COMPLETE | 3 | HIGH | exit code 0 |
| Full folder \| behavioral | COMPLETE | 4 | HIGH | exit code 0 |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### LOW · PIPELINE_TAINT_FLOW · SKILL.md:2
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 38e86be5ad |
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
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
```
### HIGH · CORRELATED_NETWORK_EXECUTION_FLOW · SKILL.md:37
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 086b8b8cb3 |
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
### HIGH · ACTIVE_DYNAMIC_EXECUTION · SKILL.md:733
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 30b0a18967 |
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
### MEDIUM · MDBLOCK_PYTHON_SUBPROCESS · SKILL.md:719
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 3c9390f343 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | SKILL.md only \| behavioral; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | command_injection |
| Analyzer | behavioral |
| Evidence check | mismatch |
| Title | Python code block executes shell commands |
Evidence snippet:

```text
result = subprocess.run(
```
## Other notes

0 metadata-quality / scan-coverage rows: .
