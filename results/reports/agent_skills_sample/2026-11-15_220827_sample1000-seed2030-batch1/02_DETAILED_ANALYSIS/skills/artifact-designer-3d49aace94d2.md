# Skill `artifact-designer-3d49aace94d2`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | latitude-dev/latitude-llm |
| SKILL.md path | .agents/skills/artifact-designer/SKILL.md |
| Sample stratum | scripts |
| Folder complete in GitSkills | True |
| Coverage | complete: every planned configuration produced a COMPLETE scan |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 1 | INFO | exit code 0 |
| SKILL.md only \| behavioral | COMPLETE | 1 | INFO | exit code 0 |
| Full folder \| default | COMPLETE | 6 | CRITICAL | exit code 0 |
| Full folder \| behavioral | COMPLETE | 6 | CRITICAL | exit code 0 |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### MEDIUM · FILE_MAGIC_MISMATCH · references/artifact-template.html:
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 6c6fff8e71 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | obfuscation |
| Analyzer | static |
| Evidence check | unavailable |
| Title | File extension does not match actual content type |
Evidence snippet:

```text

```
### CRITICAL · COMMAND_INJECTION_JS_CHILD_PROCESS · scripts/artifact.mjs:6
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 5064cd5403 |
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
### MEDIUM · DATA_EXFIL_JS_NETWORK · scripts/artifact.mjs:213
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | a55b44dc60 |
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
[/\bfetch\s*\(/i, 'fetch', 'fetch() detected; artifacts must not call APIs at view time.'],
```
### MEDIUM · DATA_EXFIL_JS_NETWORK · scripts/artifact.mjs:234
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 83dd5880a5 |
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
[/\bfetch\s*\(/i, 'fetch', 'fetch() detected; published artifacts should not call APIs at view time unless explicitly intended.'],
```
### MEDIUM · DATA_EXFIL_JS_NETWORK · scripts/artifact.mjs:294
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 8de20dbb47 |
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
const response = await fetch(url);
```
## Other notes

4 metadata-quality / scan-coverage rows: MANIFEST_MISSING_LICENSE (4).
