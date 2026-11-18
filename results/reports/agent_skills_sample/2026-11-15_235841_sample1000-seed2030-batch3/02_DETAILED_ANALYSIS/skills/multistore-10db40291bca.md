# Skill `multistore-10db40291bca`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | modc2/mod |
| SKILL.md path | mod/orbit/multistore/skill.md |
| Sample stratum | scripts |
| Folder complete in GitSkills | True |
| Coverage | complete: every planned configuration produced a COMPLETE scan |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 1 | INFO | exit code 0 |
| SKILL.md only \| behavioral | COMPLETE | 1 | INFO | exit code 0 |
| Full folder \| default | COMPLETE | 15 | MEDIUM | exit code 0 |
| Full folder \| behavioral | COMPLETE | 15 | MEDIUM | exit code 0 |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### LOW · SUPPLY_CHAIN_UNPINNED_DEPENDENCY · app/package.json:12
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 95cacc93cc |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | supply_chain_attack |
| Analyzer | static |
| Evidence check | exact |
| Title | Unpinned dependency |
Evidence snippet:

```text
"react": "^18.3.1"
```
### LOW · SUPPLY_CHAIN_UNPINNED_DEPENDENCY · app/package.json:13
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 396aaa9b40 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | supply_chain_attack |
| Analyzer | static |
| Evidence check | exact |
| Title | Unpinned dependency |
Evidence snippet:

```text
"react-dom": "^18.3.1"
```
### LOW · SUPPLY_CHAIN_UNPINNED_DEPENDENCY · app/package.json:16
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 99a294c61b |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | supply_chain_attack |
| Analyzer | static |
| Evidence check | exact |
| Title | Unpinned dependency |
Evidence snippet:

```text
"typescript": "^5.5.4"
```
### LOW · SUPPLY_CHAIN_UNPINNED_DEPENDENCY · app/package.json:17
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 7261996eab |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | supply_chain_attack |
| Analyzer | static |
| Evidence check | exact |
| Title | Unpinned dependency |
Evidence snippet:

```text
"@types/node": "^20.14.10"
```
### LOW · SUPPLY_CHAIN_UNPINNED_DEPENDENCY · app/package.json:18
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 6f01dfa335 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | supply_chain_attack |
| Analyzer | static |
| Evidence check | exact |
| Title | Unpinned dependency |
Evidence snippet:

```text
"@types/react": "^18.3.3"
```
### LOW · SUPPLY_CHAIN_UNPINNED_DEPENDENCY · app/package.json:19
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 20fb20bd20 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | supply_chain_attack |
| Analyzer | static |
| Evidence check | exact |
| Title | Unpinned dependency |
Evidence snippet:

```text
"@types/react-dom": "^18.3.0"
```
### MEDIUM · DATA_EXFIL_JS_NETWORK · app/src/lib/api.ts:56
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | dc0dfb0c6a |
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
status: () => fetch(`${BASE}/status`).then((r) => json<Status>(r)),
```
### MEDIUM · DATA_EXFIL_JS_NETWORK · app/src/lib/api.ts:57
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 9dbf368c66 |
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
backends: () => fetch(`${BASE}/backends`).then((r) => json<BackendsResp>(r)),
```
### MEDIUM · DATA_EXFIL_JS_NETWORK · app/src/lib/api.ts:58
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | fb3a3f8de4 |
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
health: () => fetch(`${BASE}/health`).then((r) => json<Record<string, unknown>>(r)),
```
### MEDIUM · DATA_EXFIL_JS_NETWORK · app/src/lib/api.ts:67
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 95850f26b4 |
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
return fetch(`${BASE}/list${qs ? `?${qs}` : ""}`).then((r) => json<ListResp>(r));
```
### MEDIUM · DATA_EXFIL_JS_NETWORK · app/src/lib/api.ts:75
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 90aedc35c7 |
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
return fetch(`${BASE}/put`, {
```
### MEDIUM · DATA_EXFIL_JS_NETWORK · app/src/lib/api.ts:86
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | f615bc4d61 |
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
return fetch(`${BASE}/pin`, {
```
### MEDIUM · DATA_EXFIL_JS_NETWORK · app/src/lib/api.ts:93
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | ca7c4f2128 |
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
fetch(`${BASE}/rm?cid=${encodeURIComponent(cid)}&backend=${backend}`, {
```
### MEDIUM · DATA_EXFIL_JS_NETWORK · app/src/lib/api.ts:101
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 29020d14e9 |
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
return fetch(`${BASE}/replicate`, {
```
## Other notes

4 metadata-quality / scan-coverage rows: MANIFEST_MISSING_LICENSE (4).
