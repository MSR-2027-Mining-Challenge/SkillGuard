# Skill `prompt_to_production-48e1d61795e7`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | ivanleomk/aie-workshop-2026-singapore |
| SKILL.md path | .agent/skills/prompt_to_production/SKILL.md |
| Sample stratum | scripts |
| Folder complete in GitSkills | True |
| Coverage | complete: every planned configuration produced a COMPLETE scan |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 2 | INFO | exit code 0 |
| SKILL.md only \| behavioral | COMPLETE | 2 | INFO | exit code 0 |
| Full folder \| default | COMPLETE | 16 | CRITICAL | exit code 0 |
| Full folder \| behavioral | COMPLETE | 16 | CRITICAL | exit code 0 |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### MEDIUM · FILE_MAGIC_MISMATCH · solutions/03-tool-call.ts:
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 3880e168a8 |
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
### CRITICAL · COMMAND_INJECTION_JS_CHILD_PROCESS · solutions/07-coding-agent.ts:5
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 12fea511f6 |
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
import { execSync } from "node:child_process";
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · solutions/07-coding-agent.ts:97
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 277b360db3 |
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
return fs.readFileSync(args.filePath, "utf-8");
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · solutions/07-coding-agent.ts:119
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 80b5533e57 |
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
fs.writeFileSync(args.filePath, args.content, "utf-8");
```
### CRITICAL · COMMAND_INJECTION_JS_CHILD_PROCESS · solutions/07-coding-agent.ts:139
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 49992c505f |
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
const output = execSync(args.command, { encoding: "utf-8", timeout: 15000 });
```
### CRITICAL · COMMAND_INJECTION_JS_CHILD_PROCESS · solutions/08-google-tools.ts:5
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 9db919faeb |
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
import { execSync } from "node:child_process";
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · solutions/08-google-tools.ts:42
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 10cc08a1ce |
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
fs.appendFileSync("08-google-tools.log", JSON.stringify(response, null, 2) + "\n\n", "utf-8");
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · solutions/08-google-tools.ts:105
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | eaa051f6c5 |
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
return fs.readFileSync(args.filePath, "utf-8");
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · solutions/08-google-tools.ts:127
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 40aeae57f5 |
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
fs.writeFileSync(args.filePath, args.content, "utf-8");
```
### CRITICAL · COMMAND_INJECTION_JS_CHILD_PROCESS · solutions/08-google-tools.ts:147
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 674b509933 |
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
const output = execSync(args.command, { encoding: "utf-8", timeout: 15000 });
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · solutions/09-daytona-sdk.ts:67
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 69b94f2ba6 |
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
fs.appendFileSync("09-daytona-sdk.log", JSON.stringify(response, null, 2) + "\n\n", "utf-8");
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · solutions/10-adding-otel.ts:85
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | f1ec81e509 |
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
fs.appendFileSync("10-adding-otel.log", JSON.stringify(response, null, 2) + "\n\n", "utf-8");
```
### CRITICAL · COMMAND_INJECTION_JS_CHILD_PROCESS · solutions/11-tuning-responses.ts:5
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | d8e2dabe15 |
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
import { execSync } from "node:child_process";
```
### LOW · UNDECLARED_NETWORK_DESTINATION · solutions/11-tuning-responses.ts:257
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | b3f172cb6c |
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
## Other notes

8 metadata-quality / scan-coverage rows: MANIFEST_INVALID_NAME (4), MANIFEST_MISSING_LICENSE (4).
