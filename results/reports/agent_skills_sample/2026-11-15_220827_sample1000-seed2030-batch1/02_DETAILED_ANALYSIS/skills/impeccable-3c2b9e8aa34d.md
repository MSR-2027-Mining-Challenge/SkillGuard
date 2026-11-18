# Skill `impeccable-3c2b9e8aa34d`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | kautsrakbr/Simulasi-Reservoir |
| SKILL.md path | impeccable/impeccable-main/.rovodev/skills/impeccable/SKILL.md |
| Sample stratum | scripts |
| Folder complete in GitSkills | False |
| Coverage | complete: every planned configuration produced a COMPLETE scan |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 0 | SAFE | exit code 0 |
| SKILL.md only \| behavioral | COMPLETE | 0 | SAFE | exit code 0 |
| Full folder \| default | COMPLETE | 141 | CRITICAL | exit code 0 |
| Full folder \| behavioral | COMPLETE | 142 | CRITICAL | exit code 0 |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### MEDIUM · ALLOWED_TOOLS_WRITE_VIOLATION · SKILL.md:
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 91af6d3cf1 |
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
### LOW · ALLOWED_TOOLS_GREP_VIOLATION · SKILL.md:
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 902cdb4c7f |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | unauthorized_tool_use |
| Analyzer | static |
| Evidence check | unavailable |
| Title | Code uses search/grep patterns but Grep tool not in allowed-tools |
Evidence snippet:

```text

```
### CRITICAL · COMMAND_INJECTION_JS_CHILD_PROCESS · scripts/context-signals.mjs:23
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | eebae3904a |
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
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/context-signals.mjs:48
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | f100c645eb |
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
const text = fs.readFileSync(path.join(dir, newest), 'utf-8');
```
### LOW · UNDECLARED_NETWORK_DESTINATION · scripts/context.mjs:34
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 21c1f42bb8 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | unauthorized_tool_use |
| Analyzer | static |
| Evidence check | unavailable |
| Title | Script contacts a destination the documentation never mentions |
Evidence snippet:

```text

```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/context.mjs:86
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 76a69bdc48 |
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
return fs.readFileSync(p, 'utf-8');
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/context.mjs:123
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 9a79876411 |
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
const content = fs.readFileSync(skillMd, 'utf-8');
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/context.mjs:133
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | ce318e03e2 |
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
return JSON.parse(fs.readFileSync(UPDATE_CACHE_PATH, 'utf-8'));
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/context.mjs:142
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 9050e6ee0f |
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
fs.writeFileSync(UPDATE_CACHE_PATH, JSON.stringify(cache));
```
### MEDIUM · DATA_EXFIL_JS_NETWORK · scripts/context.mjs:161
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | e49964eab4 |
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
const res = await fetch(`${UPDATE_HOST}/api/version`, { signal: AbortSignal.timeout(FETCH_TIMEOUT_MS) });
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/context.mjs:193
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 9fb92fae50 |
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
const raw = JSON.parse(fs.readFileSync(path.join(cwd, '.impeccable', name), 'utf-8'));
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/critique-storage.mjs:110
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 36bf711ded |
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
fs.writeFileSync(filePath, `${front}\n${body.trim()}\n`, 'utf-8');
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/critique-storage.mjs:178
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 10764a29c5 |
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
return slice.map((file) => parseFrontmatter(fs.readFileSync(file, 'utf-8')));
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/critique-storage.mjs:195
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 68dac8ac5c |
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
const raw = fs.readFileSync(bodyFile, 'utf-8');
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/detector/cli/main.mjs:63
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 8bc3329c27 |
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
? detectHtml(fp, options) : detectText(fs.readFileSync(fp, 'utf-8'), fp, options);
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/detector/cli/main.mjs:236
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 02ce962e67 |
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
fileFindings = detectText(fs.readFileSync(file, 'utf-8'), file, scanOptions);
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/detector/cli/main.mjs:254
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 1abba0d62e |
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
allFindings.push(...detectText(fs.readFileSync(resolved, 'utf-8'), resolved, scanOptions));
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/detector/design-system.mjs:150
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | a53a35cd1c |
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
return JSON.parse(fs.readFileSync(filePath, 'utf-8'));
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/detector/design-system.mjs:366
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 225bb55a15 |
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
frontmatter = parseFrontmatter(fs.readFileSync(md.path, 'utf-8'));
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/detector/engines/browser/detect-url.mjs:140
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 58a2e2279a |
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
}, () => fs.readFileSync(browserScriptPath, 'utf-8'));
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/detector/engines/static-html/css-cascade.mjs:880
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | d9d709c1eb |
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
}, () => fs.readFileSync(cssPath, 'utf-8'));
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/detector/engines/static-html/detect-html.mjs:113
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 475bbc8880 |
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
}, () => fs.readFileSync(filePath, 'utf-8'));
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/detector/node/file-system.mjs:60
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | d347e383b0 |
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
const content = fs.readFileSync(file, 'utf-8');
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/detector/node/file-system.mjs:131
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 190ee4d096 |
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
const content = fs.readFileSync(configPath, 'utf-8');
```
### MEDIUM · DATA_EXFIL_JS_NETWORK · scripts/detector/node/file-system.mjs:162
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 1932157e65 |
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
const res = await fetch(`http://localhost:${port}/`, { signal: controller.signal, redirect: 'follow' });
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/hook-admin.mjs:139
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | daa09ed7e0 |
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
return { exists: true, malformed: false, raw: JSON.parse(fs.readFileSync(filePath, 'utf-8')) };
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/hook-admin.mjs:191
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 78d31cbd83 |
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
fs.writeFileSync(filePath, JSON.stringify(next, null, 2) + '\n');
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/hook-admin.mjs:209
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 10e2359c52 |
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
fs.writeFileSync(filePath, JSON.stringify(next, null, 2) + '\n');
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/hook-admin.mjs:348
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 0cfefc9ca5 |
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
next = mergeHookManifests(JSON.parse(fs.readFileSync(dest, 'utf-8')), fresh);
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/hook-admin.mjs:363
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 2b7d16aa3a |
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
fs.writeFileSync(dest, serialized);
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/hook-admin.mjs:371
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 6692abccca |
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
return fs.readFileSync(filePath, 'utf-8');
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/hook-admin.mjs:405
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 088f47b02c |
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
parsed = JSON.parse(fs.readFileSync(filePath, 'utf-8'));
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/hook-admin.mjs:454
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 595dfe9032 |
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
parsed = JSON.parse(fs.readFileSync(manifestPath, 'utf-8'));
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/hook-admin.mjs:480
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 67a44c8085 |
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
fs.writeFileSync(manifestPath, `${JSON.stringify(next, null, 2)}\n`);
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/hook-admin.mjs:614
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 040a4471af |
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
fs.writeFileSync(filePath, JSON.stringify(rest, null, 2) + '\n');
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/hook-before-edit.mjs:164
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | a47ef9ead2 |
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
return fs.readFileSync(filePath, 'utf-8');
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/hook-before-edit.mjs:235
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 589e92d371 |
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
return fs.readFileSync(sourcePath, 'utf-8');
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/hook-lib.mjs:108
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 780ae71c49 |
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
return JSON.parse(fs.readFileSync(filePath, 'utf-8'));
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/hook-lib.mjs:453
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 2279c2b6d2 |
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
fs.writeFileSync(target, JSON.stringify(cache));
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/hook-lib.mjs:473
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | a3b6b79c82 |
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
const existing = fs.existsSync(target.path) ? fs.readFileSync(target.path, 'utf-8') : '';
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/hook-lib.mjs:487
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 52917c55f9 |
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
fs.writeFileSync(target.path, updated, 'utf-8');
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/hook-lib.mjs:526
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 91b8a1b8b6 |
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
const body = fs.readFileSync(dotGit, 'utf-8').trim();
```
### LOW · UNDECLARED_NETWORK_DESTINATION · scripts/hook-lib.mjs:920
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 5040ab1e3c |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | unauthorized_tool_use |
| Analyzer | static |
| Evidence check | unavailable |
| Title | Script contacts a destination the documentation never mentions |
Evidence snippet:

```text

```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/hook-lib.mjs:1209
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 8ea06a9b5d |
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
try { content = fs.readFileSync(p, 'utf-8'); } catch { /* unreadable primary */ }
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/hook-lib.mjs:1246
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | bbe71b23f4 |
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
fs.appendFileSync(expanded, line);
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/hook-lib.mjs:1483
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | a8d53095ad |
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
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/lib/impeccable-paths.mjs:67
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 271c7c2c6e |
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
const info = JSON.parse(fs.readFileSync(filePath, 'utf-8'));
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/lib/impeccable-paths.mjs:94
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 3ee8a85e66 |
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
### CRITICAL · COMMAND_INJECTION_JS_CHILD_PROCESS · scripts/lib/is-generated.mjs:16
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | c2559b3ee1 |
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
### CRITICAL · COMMAND_INJECTION_JS_CHILD_PROCESS · scripts/lib/is-generated.mjs:44
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 360b22b7c4 |
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
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/live-accept.mjs:260
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 4b92bbad84 |
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
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/live-accept.mjs:378
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 2c3ec8d5a3 |
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
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/live-accept.mjs:759
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 2db5bad200 |
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
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/live-accept.mjs:782
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | f33bb2c11a |
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
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/live-commit-manual-edits.mjs:245
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | dfa8d8add2 |
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
try { content = fs.readFileSync(absolute, 'utf-8'); } catch { return null; }
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/live-commit-manual-edits.mjs:331
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | b2c2e1e4ea |
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
try { lines = fs.readFileSync(path.resolve(cwd, relative), 'utf-8').split('\n'); } catch { return false; }
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/live-commit-manual-edits.mjs:369
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 6fad035932 |
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
try { lines = fs.readFileSync(absolute, 'utf-8').split('\n'); } catch { return []; }
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/live-commit-manual-edits.mjs:381
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | fc3d38251b |
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
try { lines = fs.readFileSync(path.resolve(cwd, target.file), 'utf-8').split('\n'); } catch { return false; }
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/live-commit-manual-edits.mjs:582
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | ad02b11f00 |
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
content: fs.readFileSync(absolute, 'utf-8'),
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/live-commit-manual-edits.mjs:649
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | b69d2f5b6e |
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
try { content = fs.readFileSync(absolute, 'utf-8'); } catch { continue; }
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/live-commit-manual-edits.mjs:686
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | bcc337d5bb |
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
fs.writeFileSync(absolute, before.content, 'utf-8');
```
### MEDIUM · DATA_EXFIL_JS_NETWORK · scripts/live-complete.mjs:60
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 36e6ab6f3c |
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
### CRITICAL · COMMAND_INJECTION_JS_CHILD_PROCESS · scripts/live-copy-edit-agent.mjs:10
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 18787ec966 |
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
import { spawn, spawnSync } from 'node:child_process';
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/live-copy-edit-agent.mjs:129
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 8d0622c97b |
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
const output = fs.existsSync(resultPath) ? fs.readFileSync(resultPath, 'utf-8') : '';
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/live-copy-edit-agent.mjs:133
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 999e6939cc |
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
const tail = fs.existsSync(logPath) ? fs.readFileSync(logPath, 'utf-8').slice(-1200) : output.slice(-1200);
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/live-copy-edit-agent.mjs:148
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 72d2b8e140 |
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
try { content = fs.readFileSync(file, 'utf-8'); } catch (err) {
```
### CRITICAL · COMMAND_INJECTION_JS_CHILD_PROCESS · scripts/live-copy-edit-agent.mjs:169
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | f9cc263f9a |
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
const check = spawnSync(process.execPath, ['--check', file], { cwd, encoding: 'utf-8' });
```
### CRITICAL · COMMAND_INJECTION_JS_CHILD_PROCESS · scripts/live-copy-edit-agent.mjs:253
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 167b9f0c4e |
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
const validation = spawnSync(script, {
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/live-copy-edit-agent.mjs:284
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | ae779d8eb1 |
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
const pkg = JSON.parse(fs.readFileSync(pkgPath, 'utf-8'));
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/live-copy-edit-agent.mjs:406
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 9323c6c378 |
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
fs.writeFileSync(absolute, content, 'utf-8');
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/live-copy-edit-agent.mjs:507
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | a668e63604 |
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
if (mirrorOutputPath) fs.writeFileSync(mirrorOutputPath, output);
```
### CRITICAL · COMMAND_INJECTION_JS_CHILD_PROCESS · scripts/live-copy-edit-agent.mjs:552
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 60c51a7afa |
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
const result = spawnSync(command, ['--version'], { stdio: 'ignore' });
```
### CRITICAL · COMMAND_INJECTION_JS_CHILD_PROCESS · scripts/live-copy-edit-agent.mjs:661
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 2d204610cc |
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
result = spawnSync('claude', [
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/live-inject.mjs:91
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 89af42d243 |
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
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/live-inject.mjs:111
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 319f9bf419 |
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
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/live-inject.mjs:126
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 4de9a9ac64 |
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
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/live-inject.mjs:130
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 6a462ddd3f |
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
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/live-inject.mjs:159
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | d3f5ca945b |
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
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/live-inject.mjs:166
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 25220bf2b3 |
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
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/live-inject.mjs:180
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 7be7f83f88 |
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
const existing = fs.existsSync(target.path) ? fs.readFileSync(target.path, 'utf-8') : '';
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/live-inject.mjs:198
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 3e4642bdfe |
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
fs.writeFileSync(target.path, updated, 'utf-8');
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/live-inject.mjs:225
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 7d6a4d5353 |
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
const body = fs.readFileSync(dotGit, 'utf-8').trim();
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/live-insert.mjs:174
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 416f20fdf9 |
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
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/live-insert.mjs:252
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 246fd8d338 |
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
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/live-manual-edit-evidence.mjs:171
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 83a304e29e |
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
const content = fs.readFileSync(file, 'utf-8');
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/live-manual-edit-evidence.mjs:256
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 151c8e682f |
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
try { content = fs.readFileSync(file, 'utf-8'); } catch { return; }
```
### CRITICAL · COMMAND_INJECTION_JS_CHILD_PROCESS · scripts/live-poll.mjs:12
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 69a5581a3d |
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
### MEDIUM · DATA_EXFIL_JS_NETWORK · scripts/live-poll.mjs:113
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | d36e608d1f |
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
### MEDIUM · DATA_EXFIL_JS_NETWORK · scripts/live-poll.mjs:126
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | ba66f8b799 |
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
const res = await fetch(`${base}/status?token=${token}`);
```
### MEDIUM · DATA_EXFIL_JS_NETWORK · scripts/live-poll.mjs:165
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 9d9c68dbe1 |
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
const res = await fetch(`${base}/poll?token=${token}&timeout=${slice}&leaseMs=${DEFAULT_EVENT_LEASE_MS}`);
```
### CRITICAL · COMMAND_INJECTION_JS_CHILD_PROCESS · scripts/live-server.mjs:18
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | c269d185d3 |
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
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/live-server.mjs:314
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 8521409096 |
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
fs.appendFileSync(filePath, JSON.stringify(entry) + '\n');
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/live-server.mjs:353
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 0caf014da8 |
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
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/live-server.mjs:442
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 02fccff770 |
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
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/live-server.mjs:491
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 7f3800b3a6 |
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
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/live-server.mjs:560
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | efeee91ca5 |
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
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/live-server.mjs:579
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 65228f8c6a |
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
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/live-server.mjs:587
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 5a55634618 |
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
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/live-server.mjs:607
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | b6f62e5487 |
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
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/live-server.mjs:796
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | d3409e85b8 |
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
const manifest = JSON.parse(fs.readFileSync(full, 'utf-8'));
```
### MEDIUM · DATA_EXFIL_JS_NETWORK · scripts/live-server.mjs:1026
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 37564e21a7 |
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
### MEDIUM · DATA_EXFIL_JS_NETWORK · scripts/live-status.mjs:17
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 03e523ca90 |
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
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/live-wrap.mjs:130
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 0006f60db4 |
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
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/live-wrap.mjs:344
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 0601abe85e |
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
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/live-wrap.mjs:686
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | a6dad54cbb |
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
| Review ID | cf23d30af3 |
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
### CRITICAL · COMMAND_INJECTION_JS_CHILD_PROCESS · scripts/live.mjs:208
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 1d0459c98a |
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
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/live/browser-script-parts.mjs:28
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 56f7bb534c |
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
export function readLiveBrowserScriptParts(parts, readFile = (filePath) => fs.readFileSync(filePath, 'utf-8')) {
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/live/manual-apply.mjs:329
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 5507cf05f9 |
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
fs.writeFileSync(evidencePath, JSON.stringify(batch, null, 2) + '\n', 'utf-8');
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/live/manual-apply.mjs:703
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 860ab5d152 |
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
content: fs.existsSync(absolute) ? fs.readFileSync(absolute, 'utf-8') : '',
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/live/manual-apply.mjs:720
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 79be679b88 |
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
return JSON.parse(fs.readFileSync(file, 'utf-8'));
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/live/manual-apply.mjs:741
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 06a27532f4 |
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
content: exists ? fs.readFileSync(absolute, 'utf-8') : '',
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/live/manual-apply.mjs:746
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | b6319d0e7b |
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
fs.writeFileSync(`${file}.tmp`, JSON.stringify(transaction, null, 2) + '\n', 'utf-8');
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/live/manual-apply.mjs:798
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 29057cb7d2 |
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
fs.writeFileSync(absolute, item.content || '', 'utf-8');
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/live/manual-apply.mjs:862
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 309d09298f |
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
fs.writeFileSync(absolute, before.content, 'utf-8');
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/live/manual-edits-buffer.mjs:35
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | c5b7d9dc8b |
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
const raw = fs.readFileSync(filePath, 'utf-8');
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/live/manual-edits-buffer.mjs:53
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 708469ed7e |
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
fs.writeFileSync(filePath, JSON.stringify({ version: BUFFER_VERSION, entries: buffer.entries }, null, 2));
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/live/session-store.mjs:50
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 27888cfabd |
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
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/live/session-store.mjs:134
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | a4800fab0d |
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
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/live/session-store.mjs:288
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 951e740345 |
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
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/live/svelte-component.mjs:37
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | dc9c3cf8fb |
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
fs.writeFileSync(file, `export { mount, unmount } from 'svelte';\n`, 'utf-8');
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/live/svelte-component.mjs:169
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 33857a4748 |
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
fs.writeFileSync(path.join(dir, 'manifest.json'), JSON.stringify(manifest, null, 2) + '\n', 'utf-8');
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/live/svelte-component.mjs:174
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 40a83e978f |
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
fs.writeFileSync(variantFile, buildVariantStub(n, originalWithProps, contract), 'utf-8');
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/live/svelte-component.mjs:219
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | cdd76d6e01 |
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
fs.writeFileSync(path.join(dir, 'manifest.json'), JSON.stringify(manifest, null, 2) + '\n', 'utf-8');
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/live/svelte-component.mjs:224
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 2eabc86a1e |
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
fs.writeFileSync(variantFile, buildInsertVariantStub(n), 'utf-8');
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/live/svelte-component.mjs:256
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 7a850014de |
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
const data = JSON.parse(fs.readFileSync(manifestPath, 'utf-8'));
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/live/svelte-component.mjs:514
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 9c9b6dc016 |
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
const { markup, cssLines } = parseSvelteComponentFile(fs.readFileSync(variantPath, 'utf-8'));
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/live/svelte-component.mjs:535
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | b817644954 |
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
const sourceContent = fs.readFileSync(sourceFile, 'utf-8');
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/live/svelte-component.mjs:562
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 3317caf25d |
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
fs.writeFileSync(sourceFile, newLines.join('\n'), 'utf-8');
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/live/svelte-component.mjs:595
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | dce7339a6f |
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
const sourceContent = fs.readFileSync(sourceFile, 'utf-8');
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/live/svelte-component.mjs:622
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 4c6c48d807 |
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
fs.writeFileSync(sourceFile, newLines.join('\n'), 'utf-8');
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/live/svelte-component.mjs:752
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 653bac7ba0 |
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
return JSON.parse(fs.readFileSync(file, 'utf-8'));
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/live/svelte-component.mjs:764
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 386cb7f310 |
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
fs.writeFileSync(file, JSON.stringify(data, null, 2) + '\n', 'utf-8');
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/live/svelte-component.mjs:795
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 65fd00dd93 |
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
fs.writeFileSync(file, JSON.stringify({ accepts: remaining }, null, 2) + '\n', 'utf-8');
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/live/sveltekit-adapter.mjs:52
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | ba7eeb7b89 |
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
const before = layoutExisted ? fs.readFileSync(layoutAbs, 'utf-8') : defaultSvelteLayout();
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/live/sveltekit-adapter.mjs:54
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 384732a2f5 |
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
fs.writeFileSync(layoutAbs, after, 'utf-8');
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/live/sveltekit-adapter.mjs:72
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | d1afe39a2a |
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
const before = fs.readFileSync(layoutAbs, 'utf-8');
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/live/sveltekit-adapter.mjs:75
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 44f868ca5f |
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
fs.writeFileSync(layoutAbs, after, 'utf-8');
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/live/sveltekit-adapter.mjs:142
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 9a67f15d0c |
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
fs.writeFileSync(file, buildSvelteLiveRootComponent(port), 'utf-8');
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/live/sveltekit-adapter.mjs:239
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 6f1a666ff3 |
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
const pkg = JSON.parse(fs.readFileSync(file, 'utf-8'));
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/live/sveltekit-adapter.mjs:253
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | f62e77a574 |
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
return fs.readFileSync(file, 'utf-8').includes(text);
```
### MEDIUM · BEHAVIOR_BASH_TAINT_FLOW · reference/polish.md:41
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 98180eb8fc |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | data_exfiltration |
| Analyzer | behavioral |
| Evidence check | exact |
| Title | Bash: tainted data flows to dangerous sink |
Evidence snippet:

```text
node .rovodev/skills/impeccable/scripts/critique-storage.mjs latest "$slug"
```
## Other notes

0 metadata-quality / scan-coverage rows: .
