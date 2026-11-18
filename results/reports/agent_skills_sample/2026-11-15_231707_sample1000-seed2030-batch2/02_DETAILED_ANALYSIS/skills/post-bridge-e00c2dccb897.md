# Skill `post-bridge-e00c2dccb897`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | post-bridge-hq/agent-mode |
| SKILL.md path | skills/post-bridge/SKILL.md |
| Sample stratum | scripts |
| Folder complete in GitSkills | True |
| Coverage | complete: every planned configuration produced a COMPLETE scan |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 1 | INFO | exit code 0 |
| SKILL.md only \| behavioral | COMPLETE | 1 | INFO | exit code 0 |
| Full folder \| default | COMPLETE | 7 | MEDIUM | exit code 0 |
| Full folder \| behavioral | COMPLETE | 7 | MEDIUM | exit code 0 |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/post-bridge.js:27
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 730a284621 |
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
return JSON.parse(fs.readFileSync(LOCAL_CONFIG, "utf8")).apiKey;
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/post-bridge.js:33
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 612ee52a94 |
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
return JSON.parse(fs.readFileSync(CONFIG_FILE, "utf8")).apiKey;
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/post-bridge.js:43
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 29b1aeb6dd |
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
fs.writeFileSync(file, JSON.stringify({ apiKey: key }, null, 2));
```
### MEDIUM · DATA_EXFIL_JS_NETWORK · scripts/post-bridge.js:64
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 60ad6c1668 |
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
const res = await fetch(url, options);
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/post-bridge.js:119
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | efa9401679 |
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
const fileBuffer = fs.readFileSync(file);
```
### MEDIUM · DATA_EXFIL_JS_NETWORK · scripts/post-bridge.js:120
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 998b6bf327 |
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
const uploadRes = await fetch(createRes.upload_url, {
```
## Other notes

4 metadata-quality / scan-coverage rows: MANIFEST_MISSING_LICENSE (4).
