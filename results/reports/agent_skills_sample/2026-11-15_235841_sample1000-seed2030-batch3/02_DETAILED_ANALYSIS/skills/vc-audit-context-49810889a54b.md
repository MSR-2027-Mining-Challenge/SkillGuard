# Skill `vc-audit-context-49810889a54b`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | BabatImReal/affiliate-blog-website- |
| SKILL.md path | .claude/skills/vc-audit-context/SKILL.md |
| Sample stratum | scripts |
| Folder complete in GitSkills | True |
| Coverage | complete: every planned configuration produced a COMPLETE scan |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 2 | INFO | exit code 0 |
| SKILL.md only \| behavioral | COMPLETE | 2 | INFO | exit code 0 |
| Full folder \| default | COMPLETE | 7 | LOW | exit code 0 |
| Full folder \| behavioral | COMPLETE | 7 | LOW | exit code 0 |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/generate-skills-catalog.mjs:46
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | d7d29fa6f4 |
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
const existing = fs.readFileSync(target, "utf8");
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/shared-skill-utils.mjs:15
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 418a0fb0bd |
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
return fs.readFileSync(abs(relPath), "utf8");
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/shared-skill-utils.mjs:169
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | e005de6e66 |
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
fs.writeFileSync(target, `${JSON.stringify(data, null, 2)}\n`);
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/validate-context-discovery.mjs:23
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 7704972597 |
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
return fs.readFileSync(path.join(root, relPath), "utf8");
```
### LOW · DATA_EXFIL_JS_FS_ACCESS · scripts/validate-skill-routing.mjs:26
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | b875022456 |
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
return fs.readFileSync(abs(relPath), "utf8");
```
## Other notes

8 metadata-quality / scan-coverage rows: MANIFEST_INVALID_NAME (4), MANIFEST_MISSING_LICENSE (4).
