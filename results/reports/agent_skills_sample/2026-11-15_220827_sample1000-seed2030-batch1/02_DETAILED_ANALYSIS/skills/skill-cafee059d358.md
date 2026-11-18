# Skill `skill-cafee059d358`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | dt418/github-repo-manager |
| SKILL.md path | SKILL.md |
| Sample stratum | scripts |
| Folder complete in GitSkills | False |
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
### CRITICAL · COMMAND_INJECTION_JS_CHILD_PROCESS · src/index.ts:7
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 63cc8fdafb |
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
import { spawn } from "child_process";
```
### MEDIUM · DATA_EXFIL_JS_NETWORK · src/index.ts:32
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | aee0d001f3 |
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
limit: { type: "number", description: "Number of repos to fetch (default 100)", default: 100 },
```
## Other notes

4 metadata-quality / scan-coverage rows: MANIFEST_MISSING_LICENSE (4).
