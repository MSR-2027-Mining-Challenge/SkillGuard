# Skill `iikit-08-taskstoissues-61cce4592036`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | JaviMontano/jm-adk |
| SKILL.md path | sdd-metodologia/.claude/skills/iikit-08-taskstoissues/SKILL.md |
| Sample stratum | scripts |
| Folder complete in GitSkills | False |
| Coverage | complete: every planned configuration produced a COMPLETE scan |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 0 | SAFE | exit code 0 |
| SKILL.md only \| behavioral | COMPLETE | 0 | SAFE | exit code 0 |
| Full folder \| default | COMPLETE | 35 | CRITICAL | exit code 0 |
| Full folder \| behavioral | COMPLETE | 38 | CRITICAL | exit code 0 |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/dashboard/src/analyze.js:165
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 955d532608 |
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
const analysisContent = fs.readFileSync(analysisPath, 'utf-8');
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/dashboard/src/analyze.js:166
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 3ef63ab6d4 |
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
const specContent = fs.existsSync(specPath) ? fs.readFileSync(specPath, 'utf-8') : '';
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/dashboard/src/bugs.js:68
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 2ea865b841 |
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
const bugsContent = fs.readFileSync(bugsPath, 'utf-8');
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/dashboard/src/bugs.js:72
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 9f0f381cf9 |
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
const tasksContent = fs.existsSync(tasksPath) ? fs.readFileSync(tasksPath, 'utf-8') : '';
```
### CRITICAL · COMMAND_INJECTION_JS_CHILD_PROCESS · scripts/dashboard/src/bugs.js:136
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 33155339a7 |
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
const { execSync } = require('child_process');
```
### CRITICAL · COMMAND_INJECTION_JS_CHILD_PROCESS · scripts/dashboard/src/bugs.js:137
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 5ec82fe5f1 |
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
repoUrl = execSync('git remote get-url origin', {
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/dashboard/src/generate-dashboard.js:36
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 9c5580dffb |
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
const specContent = fs.readFileSync(specPath, 'utf-8');
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/dashboard/src/generate-dashboard.js:37
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 2abfeda149 |
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
const tasksContent = fs.existsSync(tasksPath) ? fs.readFileSync(tasksPath, 'utf-8') : '';
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/dashboard/src/generate-dashboard.js:99
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | aeef149fa6 |
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
const specContent = fs.existsSync(specPath) ? fs.readFileSync(specPath, 'utf-8') : '';
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/dashboard/src/generate-dashboard.js:100
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 07705529e3 |
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
const tasksContent = fs.existsSync(tasksPath) ? fs.readFileSync(tasksPath, 'utf-8') : '';
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/dashboard/src/generate-dashboard.js:109
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 227d7d86c3 |
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
const allFeatureContent = featureFiles.map(f => fs.readFileSync(f, 'utf-8')).join('\n');
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/dashboard/src/generate-dashboard.js:114
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | f58c33ad7c |
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
const context = JSON.parse(fs.readFileSync(contextPath, 'utf-8'));
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/dashboard/src/generate-dashboard.js:195
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 0bfa1d4dc8 |
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
fs.writeFileSync(tmpPath, content, 'utf-8');
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/dashboard/src/generate-dashboard.js:212
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 5c58a4d221 |
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
_cachedTemplate = fs.readFileSync(templatePath, 'utf-8');
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/dashboard/src/parser.js:111
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | a391038ad2 |
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
const content = fs.readFileSync(path.join(checklistDir, file), 'utf-8');
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/dashboard/src/parser.js:146
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | ee894e9623 |
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
const content = fs.readFileSync(path.join(checklistDir, file), 'utf-8');
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/dashboard/src/parser.js:224
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 1bc855f6a7 |
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
const content = fs.readFileSync(constitutionPath, 'utf-8').toLowerCase();
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/dashboard/src/parser.js:271
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 3a52a3fa7a |
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
const content = fs.readFileSync(premisePath, 'utf-8');
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/dashboard/src/parser.js:288
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 1abefa3a6e |
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
const content = fs.readFileSync(constitutionPath, 'utf-8');
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/dashboard/src/parser.js:883
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 4c2fa9fe46 |
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
const content = fs.readFileSync(tesslPath, 'utf-8');
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/dashboard/src/pipeline.js:34
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 9a569afaeb |
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
const specContent = specExists ? fs.readFileSync(specPath, 'utf-8') : '';
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/dashboard/src/pipeline.js:37
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | ca8a283297 |
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
const planContent = planExists ? fs.readFileSync(planPath, 'utf-8') : '';
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/dashboard/src/pipeline.js:40
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 33fab62303 |
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
const tasksContent = tasksExists ? fs.readFileSync(tasksPath, 'utf-8') : '';
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/dashboard/src/pipeline.js:49
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 5f54a4ce07 |
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
const constitutionContent = constitutionExists ? fs.readFileSync(constitutionPath, 'utf-8') : '';
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/dashboard/src/pipeline.js:55
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 086992651c |
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
checklistContent = clFiles.map(f => fs.readFileSync(path.join(checklistDir, f), 'utf-8')).join('\n');
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/dashboard/src/pipeline.js:59
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 8349547521 |
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
const analysisContent = analysisExists ? fs.readFileSync(analysisPath, 'utf-8') : '';
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/dashboard/src/pipeline.js:66
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 9a65eb2623 |
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
const ctx = JSON.parse(fs.readFileSync(contextPath, 'utf-8'));
```
### CRITICAL · COMMAND_INJECTION_JS_CHILD_PROCESS · scripts/dashboard/src/planview.js:5
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 859fbd014a |
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
const childProcess = require('child_process');
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/dashboard/src/planview.js:40
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 5f72de0245 |
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
const planContent = fs.readFileSync(planPath, 'utf-8');
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/dashboard/src/planview.js:49
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | ff85543a72 |
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
const researchContent = fs.readFileSync(researchPath, 'utf-8');
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/dashboard/src/storymap.js:22
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | f22136276b |
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
const content = fs.readFileSync(specPath, 'utf-8');
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/dashboard/src/testify.js:137
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 5ad694e1a4 |
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
const specContent = fs.existsSync(specPath) ? fs.readFileSync(specPath, 'utf-8') : '';
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/dashboard/src/testify.js:145
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 2fa36f73c0 |
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
const featureContents = featureFiles.map(f => fs.readFileSync(f, 'utf-8'));
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/dashboard/src/testify.js:152
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | dc8b9a8f96 |
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
const tasksContent = fs.existsSync(tasksPath) ? fs.readFileSync(tasksPath, 'utf-8') : '';
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/dashboard/src/testify.js:174
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 9288ed92eb |
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
const context = JSON.parse(fs.readFileSync(contextPath, 'utf-8'));
```
### MEDIUM · BEHAVIOR_BASH_TAINT_FLOW · scripts/bash/check-prerequisites.sh:404
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 84919c753f |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | data_exfiltration |
| Analyzer | behavioral |
| Evidence check | exact |
| Title | Bash: tainted data flows to dangerous sink |
Evidence snippet:

```text
NEXT_STEP_JSON=$(bash "$SCRIPT_DIR/next-step.sh" --phase status --json --project-root "$REPO_ROOT" 2>/dev/null) || NEXT_STEP_JSON='{}'
```
### MEDIUM · BEHAVIOR_BASH_TAINT_FLOW · scripts/bash/common.sh:572
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | d57c1f617e |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | data_exfiltration |
| Analyzer | behavioral |
| Evidence check | exact |
| Title | Bash: sensitive data flows to execution sink |
Evidence snippet:

```text
if echo "$content" | grep -qi "python\|pytest"; then
```
### MEDIUM · BEHAVIOR_BASH_TAINT_FLOW · scripts/bash/common.sh:575
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 4227997deb |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | data_exfiltration |
| Analyzer | behavioral |
| Evidence check | exact |
| Title | Bash: sensitive data flows to execution sink |
Evidence snippet:

```text
if echo "$content" | grep -qi "javascript\|typescript\|node\.js\|jest\|vitest"; then
```
## Other notes

0 metadata-quality / scan-coverage rows: .
