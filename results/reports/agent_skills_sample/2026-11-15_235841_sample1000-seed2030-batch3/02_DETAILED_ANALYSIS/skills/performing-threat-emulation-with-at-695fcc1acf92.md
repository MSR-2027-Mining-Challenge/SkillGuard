# Skill `performing-threat-emulation-with-at-695fcc1acf92`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | Molly-agi/Molly-Core |
| SKILL.md path | src/skills/registry/skills/cybersecurity/skills/performing-threat-emulation-with-atomic-red-team/SKILL.md |
| Sample stratum | scripts |
| Folder complete in GitSkills | True |
| Coverage | complete: every planned configuration produced a COMPLETE scan |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 0 | SAFE | exit code 0 |
| SKILL.md only \| behavioral | COMPLETE | 0 | SAFE | exit code 0 |
| Full folder \| default | COMPLETE | 2 | HIGH | exit code 0 |
| Full folder \| behavioral | COMPLETE | 2 | HIGH | exit code 0 |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### HIGH · COMMAND_INJECTION_SHELL_TRUE · scripts/agent.py:99
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 839e2f6129 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | command_injection |
| Analyzer | static |
| Evidence check | exact |
| Title | Shell command execution with shell=True enabled |
Evidence snippet:

```text
result = subprocess.run(
```
### HIGH · COMMAND_INJECTION_SHELL_TRUE · scripts/agent.py:131
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 2424c35f14 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | command_injection |
| Analyzer | static |
| Evidence check | exact |
| Title | Shell command execution with shell=True enabled |
Evidence snippet:

```text
subprocess.run(cleanup_cmd, shell=True, capture_output=True, timeout=30)
```
## Other notes

0 metadata-quality / scan-coverage rows: .
