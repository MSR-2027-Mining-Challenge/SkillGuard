# Skill `motion-graphics-88a76993cbea`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | sansayan01/finance_app_zo |
| SKILL.md path | .claude/skills/motion-graphics/SKILL.md |
| Sample stratum | scripts |
| Folder complete in GitSkills | True |
| Coverage | complete: every planned configuration produced a COMPLETE scan |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 1 | INFO | exit code 0 |
| SKILL.md only \| behavioral | COMPLETE | 1 | INFO | exit code 0 |
| Full folder \| default | COMPLETE | 9 | CRITICAL | exit code 0 |
| Full folder \| behavioral | COMPLETE | 9 | CRITICAL | exit code 0 |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### CRITICAL · COMMAND_INJECTION_JS_CHILD_PROCESS · categories/maps/bake-basemap.mjs:25
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | b6f24ad911 |
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
### LOW · UNDECLARED_NETWORK_DESTINATION · categories/maps/bake-basemap.mjs:106
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 513d937b2e |
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
### LOW · UNDECLARED_NETWORK_DESTINATION · categories/maps/bake-basemap.mjs:107
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 6d2701d8eb |
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
### LOW · UNDECLARED_NETWORK_DESTINATION · categories/maps/bake-basemap.mjs:117
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 387d7709f1 |
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
### MEDIUM · DATA_EXFIL_JS_NETWORK · categories/maps/bake-basemap.mjs:153
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | e81d85b12c |
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
fetch("https://cdn.jsdelivr.net/npm/world-atlas@2.0.2/countries-110m.json").then(function(r){return r.json();}).then(function(w){
```
### CRITICAL · COMMAND_INJECTION_JS_CHILD_PROCESS · categories/maps/bake-basemap.mjs:229
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 5982c0ff70 |
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
const ff = spawnSync(
```
### CRITICAL · COMMAND_INJECTION_JS_CHILD_PROCESS · grounding/locate.mjs:23
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | eccc90e102 |
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
import { execFileSync } from "node:child_process";
```
### MEDIUM · DATA_EXFIL_JS_NETWORK · grounding/locate.mjs:214
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | e3ed9b2907 |
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
const res = await fetch(
```
## Other notes

4 metadata-quality / scan-coverage rows: MANIFEST_MISSING_LICENSE (4).
