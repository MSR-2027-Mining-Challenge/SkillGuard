# Skill `ai-podcast-creation-a4dfdebaa616`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | MikeCheng1208/BattleTree |
| SKILL.md path | .agents/skills/ai-podcast-creation/SKILL.md |
| Sample stratum | skill_md_only |
| Folder complete in GitSkills | True |
| Coverage | complete: every planned configuration produced a COMPLETE scan |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 3 | HIGH | exit code 0 |
| SKILL.md only \| behavioral | COMPLETE | 3 | HIGH | exit code 0 |
| Full folder \| default | COMPLETE | 3 | HIGH | exit code 0 |
| Full folder \| behavioral | COMPLETE | 3 | HIGH | exit code 0 |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### HIGH · PIPELINE_TAINT_FLOW · SKILL.md:1
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | e2e9ee72a7 |
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
curl -fsSL https://cli.inference.sh | sh && infsh login
```
### HIGH · CORRELATED_NETWORK_EXECUTION_FLOW · SKILL.md:16
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 5178779573 |
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

4 metadata-quality / scan-coverage rows: MANIFEST_MISSING_LICENSE (4).
