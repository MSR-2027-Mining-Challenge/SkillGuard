# Skill `social-publisher-e348b66f0637`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | ewtwd/openclaw-skills |
| SKILL.md path | skills/social-publisher/SKILL.md |
| Sample stratum | scripts |
| Folder complete in GitSkills | False |
| Coverage | no_complete_scan: Cisco ran, but no configuration produced a COMPLETE scan |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | PARTIAL | 1 | INFO | Cisco reported an analyzer failure (skill_loader: SkillLoadError:MALFORMED_YAML_FRONTMATTER) |
| SKILL.md only \| behavioral | PARTIAL | 1 | INFO | Cisco reported an analyzer failure (skill_loader: SkillLoadError:MALFORMED_YAML_FRONTMATTER) |
| Full folder \| default | PARTIAL | 17 | MEDIUM | Cisco reported an analyzer failure (skill_loader: SkillLoadError:MALFORMED_YAML_FRONTMATTER) |
| Full folder \| behavioral | PARTIAL | 17 | MEDIUM | Cisco reported an analyzer failure (skill_loader: SkillLoadError:MALFORMED_YAML_FRONTMATTER) |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### MEDIUM · DATA_EXFIL_JS_NETWORK · scripts/social-publisher.mjs:55
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | d377ffdc0e |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | partial |
| Cisco category | data_exfiltration |
| Analyzer | static |
| Evidence check | exact |
| Title | Outbound network request primitives in JavaScript/TypeScript |
Evidence snippet:

```text
const resp = await fetch(versionUrl);
```
### LOW · UNDECLARED_NETWORK_DESTINATION · scripts/social-publisher.mjs:422
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 15f30e6fa0 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | partial |
| Cisco category | unauthorized_tool_use |
| Analyzer | static |
| Evidence check | unavailable |
| Title | Script contacts a destination the documentation never mentions |
Evidence snippet:

```text

```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/task-manager.mjs:52
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | ab8a650a01 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | partial |
| Cisco category | data_exfiltration |
| Analyzer | static |
| Evidence check | exact |
| Title | Node.js filesystem access candidate for sensitive-flow correlation |
Evidence snippet:

```text
fs.writeFileSync(taskPath, JSON.stringify(taskData, null, 2));
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/task-manager.mjs:82
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 684515cedc |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | partial |
| Cisco category | data_exfiltration |
| Analyzer | static |
| Evidence check | exact |
| Title | Node.js filesystem access candidate for sensitive-flow correlation |
Evidence snippet:

```text
const taskData = JSON.parse(fs.readFileSync(taskPath, 'utf8'));
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/task-manager.mjs:91
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 6c8086b381 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | partial |
| Cisco category | data_exfiltration |
| Analyzer | static |
| Evidence check | exact |
| Title | Node.js filesystem access candidate for sensitive-flow correlation |
Evidence snippet:

```text
fs.writeFileSync(taskPath, JSON.stringify(taskData, null, 2));
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/task-manager.mjs:125
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | cf4630e5ee |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | partial |
| Cisco category | data_exfiltration |
| Analyzer | static |
| Evidence check | exact |
| Title | Node.js filesystem access candidate for sensitive-flow correlation |
Evidence snippet:

```text
const taskData = JSON.parse(fs.readFileSync(taskPath, 'utf8'));
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/task-manager.mjs:138
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 1c97166420 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | partial |
| Cisco category | data_exfiltration |
| Analyzer | static |
| Evidence check | exact |
| Title | Node.js filesystem access candidate for sensitive-flow correlation |
Evidence snippet:

```text
fs.writeFileSync(taskPath, JSON.stringify(taskData, null, 2));
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/task-manager.mjs:164
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | af452bfaf1 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | partial |
| Cisco category | data_exfiltration |
| Analyzer | static |
| Evidence check | exact |
| Title | Node.js filesystem access candidate for sensitive-flow correlation |
Evidence snippet:

```text
return JSON.parse(fs.readFileSync(taskPath, 'utf8'));
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/task-manager.mjs:232
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | a151c9fe15 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | partial |
| Cisco category | data_exfiltration |
| Analyzer | static |
| Evidence check | exact |
| Title | Node.js filesystem access candidate for sensitive-flow correlation |
Evidence snippet:

```text
const taskData = JSON.parse(fs.readFileSync(taskPath, 'utf8'));
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/task-manager.mjs:234
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 92d6c4211a |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | partial |
| Cisco category | data_exfiltration |
| Analyzer | static |
| Evidence check | exact |
| Title | Node.js filesystem access candidate for sensitive-flow correlation |
Evidence snippet:

```text
fs.writeFileSync(taskPath, JSON.stringify(taskData, null, 2));
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/task-manager.mjs:254
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | cd21d1fee9 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | partial |
| Cisco category | data_exfiltration |
| Analyzer | static |
| Evidence check | exact |
| Title | Node.js filesystem access candidate for sensitive-flow correlation |
Evidence snippet:

```text
const taskData = JSON.parse(fs.readFileSync(taskPath, 'utf8'));
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/task-manager.mjs:257
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | f772dbbf6f |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | partial |
| Cisco category | data_exfiltration |
| Analyzer | static |
| Evidence check | exact |
| Title | Node.js filesystem access candidate for sensitive-flow correlation |
Evidence snippet:

```text
fs.writeFileSync(taskPath, JSON.stringify(taskData, null, 2));
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/task-manager.mjs:278
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | de75718f62 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | partial |
| Cisco category | data_exfiltration |
| Analyzer | static |
| Evidence check | exact |
| Title | Node.js filesystem access candidate for sensitive-flow correlation |
Evidence snippet:

```text
return JSON.parse(fs.readFileSync(taskPath, 'utf8'));
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/task-manager.mjs:316
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 091833aefa |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | partial |
| Cisco category | data_exfiltration |
| Analyzer | static |
| Evidence check | exact |
| Title | Node.js filesystem access candidate for sensitive-flow correlation |
Evidence snippet:

```text
tasks.push(JSON.parse(fs.readFileSync(taskPath, 'utf8')));
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/task-manager.mjs:338
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 3a75f0afe8 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | partial |
| Cisco category | data_exfiltration |
| Analyzer | static |
| Evidence check | exact |
| Title | Node.js filesystem access candidate for sensitive-flow correlation |
Evidence snippet:

```text
const taskData = JSON.parse(fs.readFileSync(taskPath, 'utf8'));
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/weibo-interactor.mjs:329
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 3188a14625 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | partial |
| Cisco category | data_exfiltration |
| Analyzer | static |
| Evidence check | exact |
| Title | Node.js filesystem access candidate for sensitive-flow correlation |
Evidence snippet:

```text
return JSON.parse(fs.readFileSync(contextPath, 'utf8'));
```
## Other notes

4 metadata-quality / scan-coverage rows: SKILL_LOAD_FALLBACK_USED (4).
