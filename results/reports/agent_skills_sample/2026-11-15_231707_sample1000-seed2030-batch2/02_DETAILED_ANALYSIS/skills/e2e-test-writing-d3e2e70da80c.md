# Skill `e2e-test-writing-d3e2e70da80c`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | fahad0001/opair-ai-sdlc |
| SKILL.md path | .github/skills/e2e-test-writing/SKILL.md |
| Sample stratum | scripts |
| Folder complete in GitSkills | True |
| Coverage | complete: every planned configuration produced a COMPLETE scan |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 1 | INFO | exit code 0 |
| SKILL.md only \| behavioral | COMPLETE | 1 | INFO | exit code 0 |
| Full folder \| default | COMPLETE | 11 | CRITICAL | exit code 0 |
| Full folder \| behavioral | COMPLETE | 11 | CRITICAL | exit code 0 |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/coverage-map.mjs:39
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 67a624beb0 |
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
const text = fs.readFileSync(file, "utf8");
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/coverage-map.mjs:55
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 6957b39be0 |
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
const text = fs.readFileSync(file, "utf8");
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/detect-framework.mjs:21
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 210f387a28 |
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
return JSON.parse(fs.readFileSync(file, "utf8"));
```
### CRITICAL · COMMAND_INJECTION_EVAL · scripts/dom-probe.mjs:39
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | bb9176e95d |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | command_injection |
| Analyzer | static |
| Evidence check | exact |
| Title | Dangerous code execution functions that can execute arbitrary code |
Evidence snippet:

```text
const clean = eval(cleanSource);
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/dom-probe.mjs:72
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 0c34759c1d |
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
fs.writeFileSync(out, rendered, "utf8");
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/health-check.mjs:36
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | de8f5cbede |
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
const lines = fs.readFileSync(file, "utf8").split(/\r?\n/);
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/inspect-e2e-surface.mjs:26
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 0ad9c9a385 |
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
? (JSON.parse(fs.readFileSync(packageJson, "utf8")).scripts ?? {})
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/meaningfulness-audit.mjs:36
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 794b3ef2a8 |
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
const text = fs.readFileSync(file, "utf8");
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/meaningfulness-audit.mjs:80
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 58a381ec97 |
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
const text = fs.readFileSync(file, "utf8");
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/test-report-parser.mjs:27
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | e4afef6df2 |
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
const text = fs.readFileSync(file, "utf8");
```
## Other notes

4 metadata-quality / scan-coverage rows: MANIFEST_MISSING_LICENSE (4).
