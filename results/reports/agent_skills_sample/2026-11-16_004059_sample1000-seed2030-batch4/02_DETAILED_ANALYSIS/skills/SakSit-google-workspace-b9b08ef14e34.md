# Skill `SakSit-google-workspace-b9b08ef14e34`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | beer-sakthai/Sak-Family-Agent |
| SKILL.md path | personas/saksit/skills/productivity/SakSit-google-workspace/SKILL.md |
| Sample stratum | scripts |
| Folder complete in GitSkills | True |
| Coverage | complete: every planned configuration produced a COMPLETE scan |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 2 | HIGH | exit code 0 |
| SKILL.md only \| behavioral | COMPLETE | 2 | HIGH | exit code 0 |
| Full folder \| default | COMPLETE | 10 | HIGH | exit code 0 |
| Full folder \| behavioral | COMPLETE | 10 | HIGH | exit code 0 |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### HIGH · ACTIVE_REMOTE_ACQUIRE_EXECUTE · SKILL.md:112
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 1fd00c2984 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | SKILL.md only \| default; SKILL.md only \| behavioral; Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | command_injection |
| Analyzer | static |
| Evidence check | mismatch |
| Title | Active instruction acquires and executes remote content |
Evidence snippet:

```text
If they paste the raw client ID / client secret values instead of a file path, write a valid Desktop OAuth JSON file for them yourself, save it somewhere explicit (for example `~/Downloads/hermes-goog
```
### MEDIUM · TOOL_ABUSE_UNDECLARED_NETWORK · SKILL.md:
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | a483e7fe5b |
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
### LOW · UNDECLARED_NETWORK_DESTINATION · scripts/google_api.py:46
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 1f4c376b43 |
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
### MEDIUM · DATA_EXFIL_ENV_VARS · scripts/google_api.py:90
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 7e92775bc6 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | data_exfiltration |
| Analyzer | static |
| Evidence check | exact |
| Title | Bulk process environment snapshot can expose credentials and tokens |
Evidence snippet:

```text
env = os.environ.copy()
```
### LOW · UNDECLARED_NETWORK_DESTINATION · scripts/google_api.py:825
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | c04168df7d |
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
### MEDIUM · DATA_EXFIL_ENV_VARS · scripts/gws_bridge.py:39
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 7525c3cf2a |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | data_exfiltration |
| Analyzer | static |
| Evidence check | exact |
| Title | Bulk process environment snapshot can expose credentials and tokens |
Evidence snippet:

```text
env = os.environ.copy()
```
### MEDIUM · DATA_EXFIL_NETWORK_REQUESTS · scripts/setup.py:427
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 04d1b03e32 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | data_exfiltration |
| Analyzer | static |
| Evidence check | exact |
| Title | Outbound network request primitives that can transmit data externally |
Evidence snippet:

```text
urllib.request.urlopen(
```
### MEDIUM · DATA_EXFIL_NETWORK_REQUESTS · scripts/setup.py:428
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 36af804dda |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | data_exfiltration |
| Analyzer | static |
| Evidence check | exact |
| Title | Outbound network request primitives that can transmit data externally |
Evidence snippet:

```text
urllib.request.Request(
```
### LOW · UNDECLARED_NETWORK_DESTINATION · scripts/setup.py:429
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | dcd6715a6c |
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
## Other notes

4 metadata-quality / scan-coverage rows: MANIFEST_INVALID_NAME (4).
