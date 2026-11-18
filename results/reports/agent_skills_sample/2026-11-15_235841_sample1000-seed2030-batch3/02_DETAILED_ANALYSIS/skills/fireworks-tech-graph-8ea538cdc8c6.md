# Skill `fireworks-tech-graph-8ea538cdc8c6`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | canyouio/NetDevOps-Platforms |
| SKILL.md path | .agents/skills/fireworks-tech-graph/SKILL.md |
| Sample stratum | scripts |
| Folder complete in GitSkills | False |
| Coverage | complete: every planned configuration produced a COMPLETE scan |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 1 | INFO | exit code 0 |
| SKILL.md only \| behavioral | COMPLETE | 1 | INFO | exit code 0 |
| Full folder \| default | COMPLETE | 1 | INFO | exit code 0 |
| Full folder \| behavioral | COMPLETE | 6 | MEDIUM | exit code 0 |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### MEDIUM · BEHAVIOR_BASH_TAINT_FLOW · scripts/generate-diagram.sh:148
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 8f16c834f5 |
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
if python3 -c "import cairosvg; cairosvg.svg2png(url='${SVG_FILE}', write_to='${PNG_FILE}', scale=${SCALE})" 2>/dev/null; then
```
### MEDIUM · BEHAVIOR_BASH_TAINT_FLOW · scripts/test-all-styles.sh:100
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 44eb375f7e |
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
if python3 "${SKILL_DIR}/scripts/generate-from-template.py" "$TEMPLATE_TYPE" "$SVG_FILE" "$(cat "$FIXTURE")" > /dev/null 2>&1 \
```
### MEDIUM · BEHAVIOR_BASH_TAINT_FLOW · scripts/test-all-styles.sh:101
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | eaed6d366f |
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
&& "${SKILL_DIR}/scripts/validate-svg.sh" "$SVG_FILE" > /dev/null 2>&1; then
```
### MEDIUM · BEHAVIOR_BASH_TAINT_FLOW · scripts/test-all-styles.sh:105
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | c760fb0921 |
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
&& python3 -c "import cairosvg; cairosvg.svg2png(url='${SVG_FILE}', write_to='${PNG_FILE}', scale=2)" 2>/dev/null; then
```
### MEDIUM · BEHAVIOR_BASH_TAINT_FLOW · scripts/test-all-styles.sh:122
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 17d141961f |
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
"${SKILL_DIR}/scripts/validate-svg.sh" "$SVG_FILE" 2>&1 | grep -E "✗|Error" | sed 's/^/    /' || true
```
## Other notes

4 metadata-quality / scan-coverage rows: MANIFEST_MISSING_LICENSE (4).
