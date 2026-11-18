# Skill `k8s-hpa-cost-tuning-94bfc9f65d18`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | microlinkhq/skills |
| SKILL.md path | k8s-hpa-cost-tuning/SKILL.md |
| Sample stratum | scripts |
| Folder complete in GitSkills | True |
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
### MEDIUM · DATA_EXFIL_JS_NETWORK · scripts/audit-metrics.mjs:169
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 6594c52da2 |
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
const res = await fetch(url, {
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/audit-metrics.mjs:433
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 17316060c7 |
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
await fs.writeFile(args.out, JSON.stringify(output, null, args.pretty ? 2 : 0))
```
### MEDIUM · DATA_EXFIL_JS_NETWORK · scripts/incident-metrics.mjs:189
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | cc878e0618 |
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
const res = await fetch(url, {
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/incident-metrics.mjs:411
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | f788e3f338 |
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
await fs.writeFile(args.out, JSON.stringify(output, null, args.pretty ? 2 : 0))
```
## Other notes

4 metadata-quality / scan-coverage rows: MANIFEST_MISSING_LICENSE (4).
