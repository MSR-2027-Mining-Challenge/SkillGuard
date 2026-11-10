# Skill `set-reminder-7652ed9105a8`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | Will-Barnard-WB/Personal-Knowledge-Bot |
| SKILL.md path | .claude/skills/set-reminder/SKILL.md |
| Sample stratum | scripts |
| Folder complete in GitSkills | True |
| Coverage | complete: every planned configuration produced a COMPLETE scan |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 1 | INFO | exit code 0 |
| SKILL.md only \| behavioral | COMPLETE | 1 | INFO | exit code 0 |
| Full folder \| default | COMPLETE | 6 | HIGH | exit code 0 |
| Full folder \| behavioral | COMPLETE | 6 | HIGH | exit code 0 |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### HIGH · ALLOWED_TOOLS_BASH_VIOLATION · SKILL.md:
|  | value |
|---|---|
| Validation | Provisional label (AI-assisted, not independent human review) |
| Review ID | e37db01d42 |
| Provisional label | scanner_parser_issue |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | unauthorized_tool_use |
| Analyzer | static |
| Evidence check | unavailable |
| Title | Code executes bash but Bash tool not in allowed-tools |
Evidence snippet:

```text

```
### MEDIUM · ALLOWED_TOOLS_NETWORK_USAGE · SKILL.md:
|  | value |
|---|---|
| Validation | Provisional label (AI-assisted, not independent human review) |
| Review ID | 78fa761fe9 |
| Provisional label | uncertain |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | unauthorized_tool_use |
| Analyzer | static |
| Evidence check | unavailable |
| Title | Code makes network requests |
Evidence snippet:

```text

```
### LOW · ALLOWED_TOOLS_GREP_VIOLATION · SKILL.md:
|  | value |
|---|---|
| Validation | Provisional label (AI-assisted, not independent human review) |
| Review ID | 65f210f2dd |
| Provisional label | scanner_parser_issue |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | unauthorized_tool_use |
| Analyzer | static |
| Evidence check | unavailable |
| Title | Code uses search/grep patterns but Grep tool not in allowed-tools |
Evidence snippet:

```text

```
### MEDIUM · DATA_EXFIL_NETWORK_REQUESTS · scripts/set_reminder.py:38
|  | value |
|---|---|
| Validation | Provisional label (AI-assisted, not independent human review) |
| Review ID | 0d820447dc |
| Provisional label | intentional |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | data_exfiltration |
| Analyzer | static |
| Evidence check | exact |
| Title | Outbound network request primitives that can transmit data externally |
Evidence snippet:

```text
req  = urllib.request.Request(
```
### MEDIUM · DATA_EXFIL_NETWORK_REQUESTS · scripts/set_reminder.py:41
|  | value |
|---|---|
| Validation | Provisional label (AI-assisted, not independent human review) |
| Review ID | 180a203e99 |
| Provisional label | intentional |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | data_exfiltration |
| Analyzer | static |
| Evidence check | exact |
| Title | Outbound network request primitives that can transmit data externally |
Evidence snippet:

```text
urllib.request.urlopen(req, timeout=10)
```
## Other notes

4 metadata-quality / scan-coverage rows: MANIFEST_MISSING_LICENSE (4).
