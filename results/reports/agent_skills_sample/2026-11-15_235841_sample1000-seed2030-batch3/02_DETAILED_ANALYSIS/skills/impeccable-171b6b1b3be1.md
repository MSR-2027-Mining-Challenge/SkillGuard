# Skill `impeccable-171b6b1b3be1`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | M4F-S/Ultimate-Claude-Skills |
| SKILL.md path | UI-UX/impeccable/.github/skills/impeccable/SKILL.md |
| Sample stratum | scripts |
| Folder complete in GitSkills | False |
| Coverage | complete: every planned configuration produced a COMPLETE scan |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 0 | SAFE | exit code 0 |
| SKILL.md only \| behavioral | COMPLETE | 0 | SAFE | exit code 0 |
| Full folder \| default | COMPLETE | 39 | CRITICAL | exit code 0 |
| Full folder \| behavioral | COMPLETE | 39 | CRITICAL | exit code 0 |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/impeccable-paths.mjs:66
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | d77e082ba2 |
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
return { info: JSON.parse(fs.readFileSync(filePath, 'utf-8')), path: filePath };
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/impeccable-paths.mjs:77
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 6ac9d9f724 |
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
fs.writeFileSync(filePath, JSON.stringify(info));
```
### CRITICAL · COMMAND_INJECTION_JS_CHILD_PROCESS · scripts/is-generated.mjs:16
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | ac071ffaa4 |
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
### CRITICAL · COMMAND_INJECTION_JS_CHILD_PROCESS · scripts/is-generated.mjs:44
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | f87468e01b |
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
execSync(`git check-ignore --quiet ${JSON.stringify(absPath)}`, {
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/live-accept.mjs:125
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 97d54e2b2e |
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
fs.writeFileSync(targetFile, newLines.join('\n'), 'utf-8');
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/live-accept.mjs:205
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | c8a6f6a749 |
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
fs.writeFileSync(targetFile, newLines.join('\n'), 'utf-8');
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/live-accept.mjs:542
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 4eaf56dd8d |
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
const content = fs.readFileSync(result, 'utf-8');
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/live-accept.mjs:565
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 5bdcd3c68a |
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
const content = fs.readFileSync(filePath, 'utf-8');
```
### MEDIUM · DATA_EXFIL_JS_NETWORK · scripts/live-complete.mjs:60
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 730ed081c9 |
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
const res = await fetch(`http://localhost:${info.port}/poll`, {
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/live-inject.mjs:62
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 6fd5430553 |
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
cfg = JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf-8'));
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/live-inject.mjs:82
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 37909c3519 |
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
const config = JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf-8'));
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/live-inject.mjs:91
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 94b754b1cc |
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
const content = fs.readFileSync(absFile, 'utf-8');
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/live-inject.mjs:95
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 0d48c5353c |
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
fs.writeFileSync(absFile, updated, 'utf-8');
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/live-inject.mjs:117
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 0c1004c213 |
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
const content = fs.readFileSync(absFile, 'utf-8');
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/live-inject.mjs:124
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 75d2dffe91 |
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
fs.writeFileSync(absFile, updated, 'utf-8');
```
### CRITICAL · COMMAND_INJECTION_JS_CHILD_PROCESS · scripts/live-poll.mjs:11
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 679d08c770 |
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
### MEDIUM · DATA_EXFIL_JS_NETWORK · scripts/live-poll.mjs:37
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 9c72a97358 |
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
const res = await fetch(`${base}/poll`, {
```
### MEDIUM · DATA_EXFIL_JS_NETWORK · scripts/live-poll.mjs:117
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 3efc6af985 |
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
const res = await fetch(`${base}/poll?token=${info.token}&timeout=${slice}`);
```
### CRITICAL · COMMAND_INJECTION_JS_CHILD_PROCESS · scripts/live-server.mjs:18
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | f835b6a0c7 |
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
import { spawn, execFileSync } from 'node:child_process';
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/live-server.mjs:167
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | f5e23aacc1 |
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
try { detectScript = fs.readFileSync(p, 'utf-8'); break; } catch { /* try next */ }
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/live-server.mjs:283
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 4d4d84b744 |
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
sessionScript = fs.readFileSync(sessionPath, 'utf-8');
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/live-server.mjs:284
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | cd2555cdd0 |
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
liveScript = fs.readFileSync(livePath, 'utf-8');
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/live-server.mjs:320
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | a3c25a4512 |
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
res.end(fs.readFileSync(vendorPath));
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/live-server.mjs:369
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | cc12903262 |
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
fs.writeFileSync(absPath, Buffer.concat(chunks));
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/live-server.mjs:441
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 6baa9af03f |
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
res.end(fs.readFileSync(mdPath, 'utf-8'));
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/live-server.mjs:460
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 18b3859119 |
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
response.parsed = parseDesignMd(fs.readFileSync(mdPath, 'utf-8'));
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/live-server.mjs:468
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 3004d5a881 |
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
response.sidecar = JSON.parse(fs.readFileSync(jsonPath, 'utf-8'));
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/live-server.mjs:488
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 129205203b |
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
try { content = fs.readFileSync(absPath, 'utf-8'); }
```
### MEDIUM · DATA_EXFIL_JS_NETWORK · scripts/live-server.mjs:734
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 13d4a31528 |
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
const res = await fetch(`http://localhost:${info.port}/stop?token=${info.token}`);
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/live-session-store.mjs:50
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | af9cd0ebee |
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
fs.appendFileSync(journalPath, JSON.stringify(entry) + '\n');
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/live-session-store.mjs:132
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 9a01160bc6 |
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
const lines = fs.readFileSync(journalPath, 'utf-8').split('\n');
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/live-session-store.mjs:253
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 89dc8828fc |
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
fs.writeFileSync(snapshotPath, JSON.stringify(snapshot, null, 2) + '\n');
```
### MEDIUM · DATA_EXFIL_JS_NETWORK · scripts/live-status.mjs:16
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 002a75c5ae |
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
const res = await fetch(`http://localhost:${info.port}/status?token=${info.token}`);
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/live-wrap.mjs:120
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 98c01c4cac |
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
const content = fs.readFileSync(targetFile, 'utf-8');
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/live-wrap.mjs:251
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | a9966b07ae |
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
fs.writeFileSync(targetFile, newLines.join('\n'), 'utf-8');
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/live-wrap.mjs:435
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 6d60e49808 |
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
const content = fs.readFileSync(filePath, 'utf-8');
```
### CRITICAL · COMMAND_INJECTION_JS_CHILD_PROCESS · scripts/live.mjs:20
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | ab23f435fd |
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
### CRITICAL · COMMAND_INJECTION_JS_CHILD_PROCESS · scripts/live.mjs:209
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | de5f45de7e |
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
return execSync(cmd, { encoding: 'utf-8', cwd: process.cwd(), timeout: 15_000 });
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/load-context.mjs:126
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | d4b0123a71 |
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
try { return fs.readFileSync(p, 'utf-8'); } catch { return null; }
```
## Other notes

0 metadata-quality / scan-coverage rows: .
