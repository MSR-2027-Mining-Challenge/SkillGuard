# Skill `minimap-92360e59ce0c`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | rore/bear-cli |
| SKILL.md path | tools/minimap/SKILL.md |
| Sample stratum | scripts |
| Folder complete in GitSkills | False |
| Coverage | complete: every planned configuration produced a COMPLETE scan |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 1 | INFO | exit code 0 |
| SKILL.md only \| behavioral | COMPLETE | 1 | INFO | exit code 0 |
| Full folder \| default | COMPLETE | 11 | LOW | exit code 0 |
| Full folder \| behavioral | COMPLETE | 11 | LOW | exit code 0 |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### LOW · DATA_EXFIL_JS_FS_ACCESS · server.js:171
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | a944e6fef3 |
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
file = await fs.readFile(filePath, "utf8");
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · src/roadmap.js:815
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 031dd4cd68 |
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
rawConfig = await fs.readFile(configPath, "utf8");
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · src/roadmap.js:921
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | eaa026b1ab |
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
const templateText = await fs.readFile(templatePath, "utf8");
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · src/roadmap.js:922
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 4bf8bbb8f1 |
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
await fs.writeFile(targetPath, templateText, "utf8");
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · src/roadmap.js:965
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 20bd048240 |
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
return await fs.readFile(filePath, "utf8");
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · src/roadmap.js:997
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 70e0e9ae7a |
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
const text = await fs.readFile(entry.filePath, "utf8");
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · src/roadmap.js:1131
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | a96596da08 |
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
await fs.writeFile(item.filePath, payload.rawText, "utf8");
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · src/roadmap.js:1174
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | ca32b0bf4a |
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
await fs.writeFile(item.filePath, serialized, "utf8");
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · src/roadmap.js:1191
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 29c6ca9803 |
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
await fs.writeFile(scopePath, nextText.replace(/\n/g, eol), "utf8");
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · src/roadmap.js:1240
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | d4a6534702 |
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
await fs.writeFile(boardPath, serialized, "utf8");
```
## Other notes

4 metadata-quality / scan-coverage rows: MANIFEST_MISSING_LICENSE (4).
