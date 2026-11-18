# Skill `auto-memory-f16b6134d1b3`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | dvcrn/openclaw-skills-marketplace |
| SKILL.md path | plugins/0xautonomys--permanent-memory/skills/auto-memory/SKILL.md |
| Sample stratum | scripts |
| Folder complete in GitSkills | False |
| Coverage | complete: every planned configuration produced a COMPLETE scan |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 1 | INFO | exit code 0 |
| SKILL.md only \| behavioral | COMPLETE | 1 | INFO | exit code 0 |
| Full folder \| default | COMPLETE | 2 | LOW | exit code 0 |
| Full folder \| behavioral | COMPLETE | 9 | MEDIUM | exit code 0 |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### LOW · UNDECLARED_NETWORK_DESTINATION · scripts/_lib.sh:36
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | a7dba0fad0 |
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
### MEDIUM · BEHAVIOR_BASH_TAINT_FLOW · scripts/automemory-recall-chain.sh:154
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 0df81a4fe9 |
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
EXPERIENCE=$(curl -sS --fail "$GATEWAY_URL" 2>/dev/null || true)
```
### MEDIUM · BEHAVIOR_BASH_TAINT_FLOW · scripts/automemory-recall-chain.sh:161
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | b37680077d |
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
EXPERIENCE=$(curl -sS --fail "$GATEWAY_URL" 2>/dev/null \
```
### MEDIUM · BEHAVIOR_BASH_TAINT_FLOW · scripts/automemory-recall-chain.sh:164
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 1df2e573e5 |
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
if [[ -z "$EXPERIENCE" ]] && command -v perl &>/dev/null; then
```
### MEDIUM · BEHAVIOR_BASH_TAINT_FLOW · scripts/automemory-recall-chain.sh:165
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | e50604d1e7 |
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
EXPERIENCE=$(curl -sS --fail "$GATEWAY_URL" 2>/dev/null \
```
### MEDIUM · BEHAVIOR_BASH_TAINT_FLOW · scripts/automemory-save-memory.sh:126
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 24b3b2121f |
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
CID=$("$SCRIPT_DIR/automemory-upload.sh" "$TMPFILE" --json --compress)
```
### MEDIUM · BEHAVIOR_BASH_TAINT_FLOW · scripts/automemory-upload.sh:89
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | dff97c89f6 |
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
RESPONSE=$(curl -sS -w "\n%{http_code}" -X POST "$AD_API_BASE/uploads/file/$UPLOAD_ID/chunk" \
```
### MEDIUM · BEHAVIOR_BASH_TAINT_FLOW · scripts/automemory-upload.sh:103
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 088cd9d72b |
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
RESPONSE=$(curl -sS -w "\n%{http_code}" -X POST "$AD_API_BASE/uploads/$UPLOAD_ID/complete" \
```
## Other notes

4 metadata-quality / scan-coverage rows: MANIFEST_MISSING_LICENSE (4).
