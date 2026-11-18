# Skill `writing-skills-d2ab59c9e608`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | He-Jiahui/ZirconEngine |
| SKILL.md path | .codex/skills/superpowers/skill-authoring/writing-skills/SKILL.md |
| Sample stratum | scripts |
| Folder complete in GitSkills | False |
| Coverage | complete: every planned configuration produced a COMPLETE scan |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 1 | INFO | exit code 0 |
| SKILL.md only \| behavioral | COMPLETE | 1 | INFO | exit code 0 |
| Full folder \| default | COMPLETE | 8 | CRITICAL | exit code 0 |
| Full folder \| behavioral | COMPLETE | 8 | CRITICAL | exit code 0 |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### CRITICAL · COMMAND_INJECTION_JS_CHILD_PROCESS · render-graphs.js:18
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 8b7a1a7e97 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | command_injection |
| Analyzer | static |
| Evidence check | exact |
| Title | Node.js child_process module usage for shell command execution |
Evidence snippet:

```text
const { execSync } = require('child_process');
```
### CRITICAL · COMMAND_INJECTION_JS_CHILD_PROCESS · render-graphs.js:72
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 65bfe48c06 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | command_injection |
| Analyzer | static |
| Evidence check | exact |
| Title | Node.js child_process module usage for shell command execution |
Evidence snippet:

```text
return execSync('dot -Tsvg', {
```
### CRITICAL · COMMAND_INJECTION_JS_CHILD_PROCESS · render-graphs.js:112
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | f5586d5f56 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | command_injection |
| Analyzer | static |
| Evidence check | exact |
| Title | Node.js child_process module usage for shell command execution |
Evidence snippet:

```text
execSync('which dot', { encoding: 'utf-8' });
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · render-graphs.js:120
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 92449815ce |
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
const markdown = fs.readFileSync(skillFile, 'utf-8');
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · render-graphs.js:141
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | ef064e4315 |
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
fs.writeFileSync(outputPath, svg);
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · render-graphs.js:146
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | bbb7fe0e47 |
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
fs.writeFileSync(dotPath, combined);
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · render-graphs.js:157
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | b952b2b8af |
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
fs.writeFileSync(outputPath, svg);
```
## Other notes

4 metadata-quality / scan-coverage rows: MANIFEST_MISSING_LICENSE (4).
