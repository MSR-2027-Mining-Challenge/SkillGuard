# Skill `recovering-from-ransomware-attack-40a804f686b3`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | yanacuti1121/Yana-AI |
| SKILL.md path | .claude/skills/recovering-from-ransomware-attack/SKILL.md |
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
### HIGH · YARA_jailbreak_generic · scripts/agent.py:90
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | db23af892d |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | prompt_injection |
| Analyzer | static |
| Evidence check | exact |
| Title | JAILBREAK detected by YARA |
Evidence snippet:

```text
{"item": "Reset all Domain Admin passwords", "status": "pending",
```
### HIGH · YARA_jailbreak_generic · scripts/agent.py:102
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | fb43b982ad |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | prompt_injection |
| Analyzer | static |
| Evidence check | exact |
| Title | JAILBREAK detected by YARA |
Evidence snippet:

```text
{"item": "Deploy LAPS for local admin passwords", "status": "pending",
```
## Other notes

0 metadata-quality / scan-coverage rows: .
