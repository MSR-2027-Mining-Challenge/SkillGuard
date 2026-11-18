# Skill `vllm-compare-reqs-b58e203bc21d`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | opendatahub-io/ai-helpers |
| SKILL.md path | helpers/skills/vllm-compare-reqs/SKILL.md |
| Sample stratum | scripts |
| Folder complete in GitSkills | True |
| Coverage | complete: every planned configuration produced a COMPLETE scan |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 1 | INFO | exit code 0 |
| SKILL.md only \| behavioral | COMPLETE | 1 | INFO | exit code 0 |
| Full folder \| default | COMPLETE | 4 | MEDIUM | exit code 0 |
| Full folder \| behavioral | COMPLETE | 4 | MEDIUM | exit code 0 |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### MEDIUM · ALLOWED_TOOLS_NETWORK_USAGE · SKILL.md:
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | d1b206df50 |
| Provisional label |  |
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
### MEDIUM · ALLOWED_TOOLS_READ_VIOLATION · SKILL.md:
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 8c280caab3 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | unauthorized_tool_use |
| Analyzer | static |
| Evidence check | unavailable |
| Title | Code reads files but Read tool not in allowed-tools |
Evidence snippet:

```text

```
### MEDIUM · TOOL_ABUSE_UNDECLARED_NETWORK · SKILL.md:
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 8a66ddb3ff |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | unauthorized_tool_use |
| Analyzer | static |
| Evidence check | unavailable |
| Title | Undeclared network usage |
Evidence snippet:

```text

```
## Other notes

4 metadata-quality / scan-coverage rows: MANIFEST_MISSING_LICENSE (4).
