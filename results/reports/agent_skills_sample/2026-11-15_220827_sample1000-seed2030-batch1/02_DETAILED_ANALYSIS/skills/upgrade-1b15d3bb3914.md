# Skill `upgrade-1b15d3bb3914`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | ianphil/genesis-frontier |
| SKILL.md path | .github/skills/upgrade/SKILL.md |
| Sample stratum | scripts |
| Folder complete in GitSkills | True |
| Coverage | complete: every planned configuration produced a COMPLETE scan |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 1 | INFO | exit code 0 |
| SKILL.md only \| behavioral | COMPLETE | 1 | INFO | exit code 0 |
| Full folder \| default | COMPLETE | 17 | CRITICAL | exit code 0 |
| Full folder \| behavioral | COMPLETE | 17 | CRITICAL | exit code 0 |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### CRITICAL · COMMAND_INJECTION_JS_CHILD_PROCESS · upgrade.js:15
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 1194466c62 |
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
const { execSync } = require("child_process");
```
### CRITICAL · COMMAND_INJECTION_JS_CHILD_PROCESS · upgrade.js:22
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | c574250121 |
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
const raw = execSync(`gh api ${apiPath}`, {
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · upgrade.js:82
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | dff2745e01 |
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
return JSON.parse(fs.readFileSync(p, "utf8"));
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · upgrade.js:87
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | f95f10ebc0 |
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
fs.writeFileSync(p, JSON.stringify(registry, null, 2) + "\n", "utf8");
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · upgrade.js:321
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | b74d94f020 |
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
fs.writeFileSync(localPath, content);
```
### CRITICAL · COMMAND_INJECTION_JS_CHILD_PROCESS · upgrade.js:330
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | d3b1517ef5 |
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
execSync("npm install --production", {
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · upgrade.test.js:14
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 411fdc7a58 |
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
fs.writeFileSync(
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · upgrade.test.js:22
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 22ed00c116 |
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
fs.writeFileSync(path.join(full, "index.js"), "// stub", "utf8");
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · upgrade.test.js:29
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 81355b4836 |
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
fs.readFileSync(path.join(root, ".github", "registry.json"), "utf8")
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · upgrade.test.js:564
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 314bd52d0d |
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
fs.writeFileSync(path.join(ghDir, "registry.json"), "{}", "utf8");
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · upgrade.test.js:572
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | acc6842663 |
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
fs.writeFileSync(path.join(root, "registry.json"), "{}", "utf8");
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · upgrade.test.js:589
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | ca4d0c5a33 |
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
fs.writeFileSync(path.join(ghDir, "registry.json"), "{}", "utf8");
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · upgrade.test.js:590
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 632c5b144d |
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
fs.writeFileSync(path.join(root, "registry.json"), "{}", "utf8");
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · upgrade.test.js:621
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 2d20c39f24 |
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
fs.writeFileSync(
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · upgrade.test.js:629
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 2847c78e7c |
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
fs.writeFileSync(path.join(full, "index.js"), "// stub", "utf8");
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · upgrade.test.js:636
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 03870d9ab5 |
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
fs.readFileSync(path.join(root, "registry.json"), "utf8")
```
## Other notes

4 metadata-quality / scan-coverage rows: MANIFEST_MISSING_LICENSE (4).
