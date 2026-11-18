# Skill `frontend-slides-f614baf0831f`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | punkharb/autoport |
| SKILL.md path | .claude/skills/frontend-slides/SKILL.md |
| Sample stratum | scripts |
| Folder complete in GitSkills | True |
| Coverage | complete: every planned configuration produced a COMPLETE scan |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 1 | INFO | exit code 0 |
| SKILL.md only \| behavioral | COMPLETE | 1 | INFO | exit code 0 |
| Full folder \| default | COMPLETE | 2 | LOW | exit code 0 |
| Full folder \| behavioral | COMPLETE | 3 | MEDIUM | exit code 0 |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### LOW · UNDECLARED_NETWORK_DESTINATION · scripts/export-pdf.sh:105
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 89ce13dab9 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | unauthorized_tool_use |
| Analyzer | static |
| Evidence check | unavailable |
| Title | Script contacts a destination the documentation never mentions |
Evidence snippet:

```text

```
### MEDIUM · BEHAVIOR_BASH_TAINT_FLOW · scripts/export-pdf.sh:389
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | f3b85bba46 |
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
node "$TEMP_SCRIPT" "$SERVE_DIR" "$HTML_FILENAME" "$OUTPUT_PDF" "$SCREENSHOT_DIR" "$VIEWPORT_W" "$VIEWPORT_H" || {
```
## Other notes

4 metadata-quality / scan-coverage rows: MANIFEST_MISSING_LICENSE (4).
