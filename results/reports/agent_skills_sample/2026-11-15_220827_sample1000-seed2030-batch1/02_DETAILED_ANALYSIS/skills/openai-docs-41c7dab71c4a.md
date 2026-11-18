# Skill `openai-docs-41c7dab71c4a`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | newmindsgroup/ai-agent-skills-library |
| SKILL.md path | sources/openai-codex-bundled-system-skills/skills/openai-docs/SKILL.md |
| Sample stratum | scripts |
| Folder complete in GitSkills | False |
| Coverage | complete: every planned configuration produced a COMPLETE scan |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 0 | SAFE | exit code 0 |
| SKILL.md only \| behavioral | COMPLETE | 0 | SAFE | exit code 0 |
| Full folder \| default | COMPLETE | 3 | MEDIUM | exit code 0 |
| Full folder \| behavioral | COMPLETE | 3 | MEDIUM | exit code 0 |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/resolve-latest-model-info.js:32
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | d0397fc01b |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | data_exfiltration |
| Analyzer | static |
| Evidence check | exact |
| Title | Node.js filesystem access candidate for sensitive-flow correlation |
Evidence snippet:

```text
return fs.readFile(new URL(source), "utf8");
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/resolve-latest-model-info.js:36
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 8d84594aef |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | data_exfiltration |
| Analyzer | static |
| Evidence check | exact |
| Title | Node.js filesystem access candidate for sensitive-flow correlation |
Evidence snippet:

```text
return fs.readFile(path.resolve(source), "utf8");
```
### MEDIUM · DATA_EXFIL_JS_NETWORK · scripts/resolve-latest-model-info.js:39
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | f77ac9f17c |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | data_exfiltration |
| Analyzer | static |
| Evidence check | exact |
| Title | Outbound network request primitives in JavaScript/TypeScript |
Evidence snippet:

```text
const response = await fetch(source, {
```
## Other notes

0 metadata-quality / scan-coverage rows: .
