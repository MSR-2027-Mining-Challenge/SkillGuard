# Skill `migrate-header-73343b5f466c`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | catalan-adobe/skills |
| SKILL.md path | skills/migrate-header/SKILL.md |
| Sample stratum | scripts |
| Folder complete in GitSkills | False |
| Coverage | complete: every planned configuration produced a COMPLETE scan |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 1 | INFO | exit code 0 |
| SKILL.md only \| behavioral | COMPLETE | 1 | INFO | exit code 0 |
| Full folder \| default | COMPLETE | 12 | CRITICAL | exit code 0 |
| Full folder \| behavioral | COMPLETE | 12 | CRITICAL | exit code 0 |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### MEDIUM · DATA_EXFIL_JS_NETWORK · block-files/header.js:368
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 1ef557b447 |
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
const resp = await fetch(`${navPath}.plain.html`);
```
### CRITICAL · COMMAND_INJECTION_JS_CHILD_PROCESS · scripts/capture-visual-tree.js:25
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 543b64ca50 |
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
import { execFileSync } from 'node:child_process';
```
### CRITICAL · COMMAND_INJECTION_JS_CHILD_PROCESS · scripts/css-query.js:14
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 31e07385ec |
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
import { execFileSync } from 'node:child_process';
```
### CRITICAL · COMMAND_INJECTION_JS_CHILD_PROCESS · scripts/detect-overlays-fallback.js:22
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 22ef246739 |
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
import { execFileSync, execSync } from 'node:child_process';
```
### CRITICAL · COMMAND_INJECTION_JS_CHILD_PROCESS · scripts/detect-overlays-fallback.js:124
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 3421f79b11 |
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
execSync(`node "${join(prepDir, 'overlay-db.js')}" refresh`, {
```
### CRITICAL · COMMAND_INJECTION_JS_CHILD_PROCESS · scripts/detect-overlays-fallback.js:128
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 816ce239db |
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
const bundle = execSync(
```
### CRITICAL · COMMAND_INJECTION_JS_CHILD_PROCESS · scripts/extract-row-content.js:17
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 970729ca36 |
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
import { execFileSync } from 'node:child_process';
```
### CRITICAL · COMMAND_INJECTION_JS_CHILD_PROCESS · scripts/setup-polish-loop.js:23
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 1511789a15 |
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
import { execSync } from 'node:child_process';
```
### CRITICAL · COMMAND_INJECTION_JS_CHILD_PROCESS · scripts/setup-polish-loop.js:305
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | c97f8bdb71 |
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
const gitDir = execSync('git rev-parse --git-dir', {
```
### CRITICAL · COMMAND_INJECTION_JS_CHILD_PROCESS · scripts/setup-polish-loop.js:344
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 3d0f52868e |
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
execSync('npm init -y', { cwd: autoresearchDir, stdio: 'pipe' });
```
### CRITICAL · COMMAND_INJECTION_JS_CHILD_PROCESS · scripts/setup-polish-loop.js:349
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | c0a1eabcae |
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
execSync('npm install pixelmatch pngjs', {
```
## Other notes

4 metadata-quality / scan-coverage rows: MANIFEST_MISSING_LICENSE (4).
