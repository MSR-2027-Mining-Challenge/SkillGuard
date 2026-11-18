# Skill `pdf-reader-cli-41ddd7cbcf7d`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | ronakpjain/dots |
| SKILL.md path | pi/agent/skills/pdf-reader-cli/SKILL.md |
| Sample stratum | scripts |
| Folder complete in GitSkills | True |
| Coverage | complete: every planned configuration produced a COMPLETE scan |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 1 | INFO | exit code 0 |
| SKILL.md only \| behavioral | COMPLETE | 1 | INFO | exit code 0 |
| Full folder \| default | COMPLETE | 3 | CRITICAL | exit code 0 |
| Full folder \| behavioral | COMPLETE | 3 | CRITICAL | exit code 0 |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### MEDIUM · ALLOWED_TOOLS_WRITE_VIOLATION · SKILL.md:
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | f94e644e01 |
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
### CRITICAL · COMMAND_INJECTION_JS_CHILD_PROCESS · scripts/read-pdf.mjs:3
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | f7bdd7650b |
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
import { spawn } from 'node:child_process';
```
## Other notes

4 metadata-quality / scan-coverage rows: MANIFEST_MISSING_LICENSE (4).
