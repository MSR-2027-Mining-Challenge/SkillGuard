# Skill `mermaid-studio-d9030faf4ffd`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | DevOficinaBrasil/backend-promotor |
| SKILL.md path | .claude/skills/mermaid-studio/SKILL.md |
| Sample stratum | scripts |
| Folder complete in GitSkills | True |
| Coverage | complete: every planned configuration produced a COMPLETE scan |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 0 | SAFE | exit code 0 |
| SKILL.md only \| behavioral | COMPLETE | 0 | SAFE | exit code 0 |
| Full folder \| default | COMPLETE | 10 | CRITICAL | exit code 0 |
| Full folder \| behavioral | COMPLETE | 10 | CRITICAL | exit code 0 |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### LOW · HIDDEN_DATA_FILE · .skill-meta.json:
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | befbbadd3b |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | obfuscation |
| Analyzer | static |
| Evidence check | unavailable |
| Title | Hidden data file detected |
Evidence snippet:

```text

```
### CRITICAL · COMMAND_INJECTION_JS_CHILD_PROCESS · scripts/batch.mjs:21
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | baa32c8348 |
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
import { execSync } from "child_process";
```
### CRITICAL · COMMAND_INJECTION_JS_CHILD_PROCESS · scripts/batch.mjs:126
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | fa23cbb29a |
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
execSync(cmd, {
```
### CRITICAL · COMMAND_INJECTION_JS_CHILD_PROCESS · scripts/render.mjs:17
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 3084e6bb46 |
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
import { execSync } from "child_process";
```
### CRITICAL · COMMAND_INJECTION_JS_CHILD_PROCESS · scripts/render.mjs:150
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 4ae371bde0 |
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
execSync(`${shellQuote(p)} --version`, { stdio: "pipe", timeout: 10000 });
```
### CRITICAL · COMMAND_INJECTION_JS_CHILD_PROCESS · scripts/render.mjs:157
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | d71f4edccb |
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
execSync("npx mmdc --version", { stdio: "pipe", timeout: 15000 });
```
### CRITICAL · COMMAND_INJECTION_JS_CHILD_PROCESS · scripts/render.mjs:247
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 7bc9995b73 |
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
execSync(cmd, { stdio: "pipe", timeout: 60000 });
```
### MEDIUM · DATA_EXFIL_JS_NETWORK · scripts/render.mjs:320
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 0c3da69c7b |
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
`{ name: '${name}', loader: () => fetch('${ICON_PACK_URLS[name]}').then(r => r.json()) }`
```
### LOW · UNDECLARED_NETWORK_DESTINATION · scripts/render.mjs:348
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | c222c44f9a |
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
### CRITICAL · COMMAND_INJECTION_JS_FUNCTION_CONSTRUCTOR · scripts/render.mjs:398
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 49ce006c18 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | command_injection |
| Analyzer | static |
| Evidence check | exact |
| Title | Dynamic code execution via Function constructor or string-based setTimeout/setInterval |
Evidence snippet:

```text
await page.waitForFunction("window.__mermaidRendered === true", { timeout: 15000 });
```
## Other notes

0 metadata-quality / scan-coverage rows: .
