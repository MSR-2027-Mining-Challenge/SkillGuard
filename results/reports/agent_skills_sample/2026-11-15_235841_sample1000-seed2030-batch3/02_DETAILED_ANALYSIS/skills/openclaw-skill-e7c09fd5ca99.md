# Skill `openclaw-skill-e7c09fd5ca99`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | agntdev/agentmeme.ai |
| SKILL.md path | openclaw-skill/SKILL.md |
| Sample stratum | scripts |
| Folder complete in GitSkills | False |
| Coverage | complete: every planned configuration produced a COMPLETE scan |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 1 | INFO | exit code 0 |
| SKILL.md only \| behavioral | COMPLETE | 1 | INFO | exit code 0 |
| Full folder \| default | COMPLETE | 17 | MEDIUM | exit code 0 |
| Full folder \| behavioral | COMPLETE | 17 | MEDIUM | exit code 0 |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### MEDIUM · DATA_EXFIL_JS_NETWORK · scripts/check-leaderboard.ts:10
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | d8f0d15fdc |
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
const res = await fetch(`${RACE_API}/api/leaderboard?limit=20`);
```
### MEDIUM · DATA_EXFIL_JS_NETWORK · scripts/close-orders.ts:4
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | da6e2a5d61 |
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
const res = await fetch(`${RACE_API}/api/contracts`);
```
### MEDIUM · DATA_EXFIL_JS_NETWORK · scripts/close-orders.ts:27
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 74ac1b223b |
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
const res = await fetch(`${RACE_API}/api/contracts/${contractId}/close-all-orders`, { method: "POST" });
```
### MEDIUM · FILE_MAGIC_MISMATCH · scripts/get-balance.ts:
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | c567763c43 |
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
### MEDIUM · FILE_MAGIC_MISMATCH · scripts/get-orderbook.ts:
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | b4a7966d73 |
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
### MEDIUM · DATA_EXFIL_JS_NETWORK · scripts/helpers.ts:58
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 2d9471a4bd |
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
const res = await fetch(`${TONCENTER}/api/v2/getAddressBalance?address=${encodeURIComponent(address)}`);
```
### MEDIUM · DATA_EXFIL_JS_NETWORK · scripts/helpers.ts:65
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 6d121b17a8 |
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
const res = await fetch(`${TONCENTER}/api/v2/getAddressInformation?address=${encodeURIComponent(address)}`);
```
### MEDIUM · DATA_EXFIL_JS_NETWORK · scripts/helpers.ts:80
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 9c4c548521 |
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
### MEDIUM · DATA_EXFIL_JS_NETWORK · scripts/helpers.ts:121
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 0c871a41ed |
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
const res = await fetch(`${RACE_API}/api/tokens`);
```
### MEDIUM · DATA_EXFIL_JS_NETWORK · scripts/helpers.ts:157
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | b7b6675cbb |
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
const res = await fetch(`${DEX_API}/orders/book?${params}`);
```
### MEDIUM · DATA_EXFIL_JS_NETWORK · scripts/helpers.ts:184
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 85ebff99b8 |
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
const res = await fetch(`${DEX_API}/orders?${params}`);
```
### MEDIUM · DATA_EXFIL_JS_NETWORK · scripts/helpers.ts:200
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | b055d78351 |
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
const res = await fetch(`${DEX_API}/coins?limit=200`);
```
### MEDIUM · DATA_EXFIL_JS_NETWORK · scripts/helpers.ts:221
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | b1e1539e39 |
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
const res = await fetch(`${DEX_API}/vaults?${params}`);
```
### MEDIUM · FILE_MAGIC_MISMATCH · scripts/list-orders.ts:
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 81f7d4615c |
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
### MEDIUM · DATA_EXFIL_JS_NETWORK · scripts/withdraw.ts:4
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | b08542d92f |
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
const res = await fetch(`${RACE_API}/api/contracts`);
```
### MEDIUM · DATA_EXFIL_JS_NETWORK · scripts/withdraw.ts:31
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 66f6716ae8 |
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
const res = await fetch(endpoint, { method: "POST" });
```
## Other notes

4 metadata-quality / scan-coverage rows: MANIFEST_MISSING_LICENSE (4).
