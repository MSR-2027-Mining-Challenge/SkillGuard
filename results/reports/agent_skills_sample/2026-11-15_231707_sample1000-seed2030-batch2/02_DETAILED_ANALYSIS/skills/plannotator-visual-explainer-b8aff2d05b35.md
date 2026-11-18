# Skill `plannotator-visual-explainer-b8aff2d05b35`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | twlgamesbr/Unity_Linux_LLM |
| SKILL.md path | .agents/skills/plannotator-visual-explainer/SKILL.md |
| Sample stratum | scripts |
| Folder complete in GitSkills | True |
| Coverage | complete: every planned configuration produced a COMPLETE scan |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 1 | INFO | exit code 0 |
| SKILL.md only \| behavioral | COMPLETE | 1 | INFO | exit code 0 |
| Full folder \| default | COMPLETE | 2 | CRITICAL | exit code 0 |
| Full folder \| behavioral | COMPLETE | 2 | CRITICAL | exit code 0 |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### CRITICAL · COMMAND_INJECTION_JS_FUNCTION_CONSTRUCTOR · SKILL.test.ts:30
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 835da63e07 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | command_injection |
| Analyzer | static |
| Evidence check | exact |
| Title | Dynamic code execution via Function constructor or string-based setTimeout/setInterval |
Evidence snippet:

```text
const runExample = new Function(
```
## Other notes

4 metadata-quality / scan-coverage rows: MANIFEST_MISSING_LICENSE (4).
