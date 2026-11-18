# Skill `s2-docs-1f06e131d2bb`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | adobe/spectrum-design-data |
| SKILL.md path | tools/s2-docs-mcp/skills/s2-docs/SKILL.md |
| Sample stratum | scripts |
| Folder complete in GitSkills | True |
| Coverage | complete: every planned configuration produced a COMPLETE scan |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 1 | INFO | exit code 0 |
| SKILL.md only \| behavioral | COMPLETE | 1 | INFO | exit code 0 |
| Full folder \| default | COMPLETE | 4 | CRITICAL | exit code 0 |
| Full folder \| behavioral | COMPLETE | 4 | CRITICAL | exit code 0 |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### MEDIUM · ALLOWED_TOOLS_WRITE_VIOLATION · SKILL.md:
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 91a78364b8 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | policy_violation |
| Analyzer | static |
| Evidence check | unavailable |
| Title | Skill declares no Write tool but bundled scripts write files |
Evidence snippet:

```text

```
### CRITICAL · COMMAND_INJECTION_JS_CHILD_PROCESS · scripts/lookup.js:23
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 4507565d86 |
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
import { spawnSync } from "node:child_process";
```
### CRITICAL · COMMAND_INJECTION_JS_CHILD_PROCESS · scripts/lookup.js:46
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | f45128d048 |
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
const result = spawnSync(process.execPath, [binPath, ...cleanArgs], {
```
## Other notes

4 metadata-quality / scan-coverage rows: MANIFEST_MISSING_LICENSE (4).
