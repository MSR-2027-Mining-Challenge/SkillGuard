# Skill `performing-kubernetes-penetration-t-0e7d90397422`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | RobotFlow-Labs/skills-repo |
| SKILL.md path | skills/performing-kubernetes-penetration-testing/SKILL.md |
| Sample stratum | scripts |
| Folder complete in GitSkills | True |
| Coverage | complete: every planned configuration produced a COMPLETE scan |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 2 | HIGH | exit code 0 |
| SKILL.md only \| behavioral | COMPLETE | 2 | HIGH | exit code 0 |
| Full folder \| default | COMPLETE | 2 | HIGH | exit code 0 |
| Full folder \| behavioral | COMPLETE | 2 | HIGH | exit code 0 |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### LOW · PIPELINE_TAINT_FLOW · SKILL.md:2
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | d668ceb095 |
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
curl -s https://raw.githubusercontent.com/kubescape/kubescape/master/install.sh | /bin/bash
```
### HIGH · CORRELATED_NETWORK_EXECUTION_FLOW · SKILL.md:113
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | ea2e4910c9 |
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
## Other notes

0 metadata-quality / scan-coverage rows: .
