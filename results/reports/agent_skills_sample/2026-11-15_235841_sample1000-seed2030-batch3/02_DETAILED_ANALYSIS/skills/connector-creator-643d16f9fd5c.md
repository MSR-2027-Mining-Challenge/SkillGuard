# Skill `connector-creator-643d16f9fd5c`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | narailabs/narai-primitives |
| SKILL.md path | plugins/connector-creator/skills/connector-creator/SKILL.md |
| Sample stratum | scripts |
| Folder complete in GitSkills | False |
| Coverage | complete: every planned configuration produced a COMPLETE scan |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 2 | LOW | exit code 0 |
| SKILL.md only \| behavioral | COMPLETE | 2 | LOW | exit code 0 |
| Full folder \| default | COMPLETE | 7 | LOW | exit code 0 |
| Full folder \| behavioral | COMPLETE | 7 | LOW | exit code 0 |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### LOW · DATA_EXFIL_JS_FS_ACCESS · lib/connector-registry.mjs:19
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | ac7b4fe33e |
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
raw = fs.readFileSync(file, "utf-8");
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · lib/connector-registry.mjs:42
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | c63f18de4f |
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
fs.writeFileSync(file, yaml.dump(parsed, { lineWidth: 120 }));
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · lib/settings-wiring.mjs:21
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 7d76a5f500 |
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
parsed = JSON.parse(fs.readFileSync(settingsPath, "utf-8"));
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · lib/settings-wiring.mjs:44
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 14a9dc5746 |
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
fs.writeFileSync(settingsPath, JSON.stringify(parsed, null, 2) + "\n");
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · lib/settings-wiring.mjs:51
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 3a6c8ecf25 |
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
parsed = JSON.parse(fs.readFileSync(settingsPath, "utf-8"));
```
## Other notes

8 metadata-quality / scan-coverage rows: MANIFEST_DESCRIPTION_TOO_LONG (4), MANIFEST_MISSING_LICENSE (4).
