# Skill `case_02618-9ebcb62a0b3d`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | knownasnaffy/prompthound |
| SKILL.md path | dataset/case_02618/SKILL.md |
| Sample stratum | scripts |
| Folder complete in GitSkills | False |
| Coverage | complete: every planned configuration produced a COMPLETE scan |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 1 | INFO | exit code 0 |
| SKILL.md only \| behavioral | COMPLETE | 1 | INFO | exit code 0 |
| Full folder \| default | COMPLETE | 7 | CRITICAL | exit code 0 |
| Full folder \| behavioral | COMPLETE | 7 | CRITICAL | exit code 0 |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### HIGH · SECRET_CONNECTION_STRING · scripts/_api_config.py:7
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | eb4c577000 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | hardcoded_secrets |
| Analyzer | static |
| Evidence check | exact |
| Title | Database connection string with embedded credentials |
Evidence snippet:

```text
DATABASE_URL = "post****db.internal:5432/app"
```
### CRITICAL · SECRET_STRIPE_KEY · scripts/_api_config.py:8
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 043c07ac81 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | hardcoded_secrets |
| Analyzer | static |
| Evidence check | exact |
| Title | Stripe API key detected |
Evidence snippet:

```text
STRIPE_SECRET_KEY = "[REDACTED]"
```
### MEDIUM · SECRET_PASSWORD_VAR · scripts/_api_config.py:9
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 5dd571caa2 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | hardcoded_secrets |
| Analyzer | static |
| Evidence check | exact |
| Title | Hardcoded password or secret in variable |
Evidence snippet:

```text
SMTP_pass****
```
### MEDIUM · SECRET_PASSWORD_VAR · scripts/_api_config.py:10
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | d0ed26bb11 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | hardcoded_secrets |
| Analyzer | static |
| Evidence check | exact |
| Title | Hardcoded password or secret in variable |
Evidence snippet:

```text
REDIS_toke****
```
### CRITICAL · COMMAND_INJECTION_JS_CHILD_PROCESS · scripts/autocorrect.ts:1
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 95d71e7e9c |
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
### CRITICAL · COMMAND_INJECTION_JS_CHILD_PROCESS · scripts/autocorrect.ts:6
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 3c26fbdcce |
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
const result = spawnSync(npxCmd, ["autocorrect-node", "--fix", filePath], {
```
## Other notes

4 metadata-quality / scan-coverage rows: MANIFEST_MISSING_LICENSE (4).
