# Skill `data-store-7495a41da383`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | runxhq/runx |
| SKILL.md path | skills/data-store/SKILL.md |
| Sample stratum | scripts |
| Folder complete in GitSkills | True |
| Coverage | complete: every planned configuration produced a COMPLETE scan |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 1 | INFO | exit code 0 |
| SKILL.md only \| behavioral | COMPLETE | 1 | INFO | exit code 0 |
| Full folder \| default | COMPLETE | 11 | CRITICAL | exit code 0 |
| Full folder \| behavioral | COMPLETE | 11 | CRITICAL | exit code 0 |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### LOW · DATA_EXFIL_JS_FS_ACCESS · tools/data/local/run.mjs:29
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | f7ef13d107 |
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
? fs.readFileSync(process.env.RUNX_INPUTS_PATH, "utf8")
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · tools/data/local/run.mjs:267
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | d0973e9b32 |
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
const parsed = JSON.parse(fs.readFileSync(file, "utf8"));
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · tools/data/local/run.mjs:279
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 85c350c63b |
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
fs.writeFileSync(tmp, `${JSON.stringify(store, null, 2)}\n`);
```
### CRITICAL · COMMAND_INJECTION_JS_CHILD_PROCESS · tools/data/redis/run.mjs:3
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | b8a1a3846e |
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
### LOW · DATA_EXFIL_JS_FS_ACCESS · tools/data/redis/run.mjs:29
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 7b52d96ff4 |
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
? fs.readFileSync(process.env.RUNX_INPUTS_PATH, "utf8")
```
### CRITICAL · COMMAND_INJECTION_JS_CHILD_PROCESS · tools/data/redis/run.mjs:381
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 818754d754 |
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
const result = spawnSync(REDIS_CLI_BIN, ["-u", redisUrl(rawInputs), "--raw", ...args], {
```
### CRITICAL · COMMAND_INJECTION_JS_CHILD_PROCESS · tools/data/sqlite/run.mjs:4
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 65a5ff6c7a |
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
### LOW · DATA_EXFIL_JS_FS_ACCESS · tools/data/sqlite/run.mjs:30
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 05015cb904 |
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
? fs.readFileSync(process.env.RUNX_INPUTS_PATH, "utf8")
```
### CRITICAL · COMMAND_INJECTION_JS_CHILD_PROCESS · tools/data/sqlite/run.mjs:602
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 49a0405f44 |
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
const result = spawnSync(SQLITE_BIN, ["-cmd", ".timeout 5000", database], {
```
### CRITICAL · COMMAND_INJECTION_JS_CHILD_PROCESS · tools/data/sqlite/run.mjs:616
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 47f1273d04 |
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
const result = spawnSync(SQLITE_BIN, ["-cmd", ".timeout 5000", "-json", database], {
```
## Other notes

4 metadata-quality / scan-coverage rows: MANIFEST_MISSING_LICENSE (4).
