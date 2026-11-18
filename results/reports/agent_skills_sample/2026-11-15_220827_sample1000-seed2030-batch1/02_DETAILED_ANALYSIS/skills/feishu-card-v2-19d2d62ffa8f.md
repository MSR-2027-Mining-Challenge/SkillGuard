# Skill `feishu-card-v2-19d2d62ffa8f`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | GeorgeDoors888/GB-Power-Market-JJ |
| SKILL.md path | openclaw-skills/skills/afk101/feishu-card-v2/SKILL.md |
| Sample stratum | scripts |
| Folder complete in GitSkills | False |
| Coverage | complete: every planned configuration produced a COMPLETE scan |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 1 | INFO | exit code 0 |
| SKILL.md only \| behavioral | COMPLETE | 1 | INFO | exit code 0 |
| Full folder \| default | COMPLETE | 5 | MEDIUM | exit code 0 |
| Full folder \| behavioral | COMPLETE | 5 | MEDIUM | exit code 0 |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### MEDIUM · DATA_EXFIL_JS_NETWORK · index.ts:154
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 6dc391f71e |
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
const res = await fetch("https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal", {
```
### LOW · UNDECLARED_NETWORK_DESTINATION · index.ts:154
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 5bbbc96f7d |
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
### MEDIUM · DATA_EXFIL_JS_NETWORK · index.ts:183
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 3949d5a197 |
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
### MEDIUM · DATA_EXFIL_JS_NETWORK · index.ts:212
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | e61afc767f |
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
