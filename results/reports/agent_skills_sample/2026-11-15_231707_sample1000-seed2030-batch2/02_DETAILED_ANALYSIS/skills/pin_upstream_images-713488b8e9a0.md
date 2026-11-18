# Skill `pin_upstream_images-713488b8e9a0`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | multigres/multigres-operator |
| SKILL.md path | tools/skills/pin_upstream_images/SKILL.md |
| Sample stratum | scripts |
| Folder complete in GitSkills | True |
| Coverage | complete: every planned configuration produced a COMPLETE scan |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 2 | INFO | exit code 0 |
| SKILL.md only \| behavioral | COMPLETE | 2 | INFO | exit code 0 |
| Full folder \| default | COMPLETE | 8 | MEDIUM | exit code 0 |
| Full folder \| behavioral | COMPLETE | 8 | MEDIUM | exit code 0 |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### MEDIUM · TOOL_ABUSE_UNDECLARED_NETWORK · SKILL.md:
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | b335111f02 |
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
### MEDIUM · DATA_EXFIL_NETWORK_REQUESTS · scripts/fetch_latest_tags.py:35
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 10481a9a6b |
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
with urllib.request.urlopen(url) as resp:
```
### MEDIUM · DATA_EXFIL_NETWORK_REQUESTS · scripts/fetch_latest_tags.py:41
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | b0359d7a1e |
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
req = urllib.request.Request(url, method="HEAD", headers={
```
### MEDIUM · DATA_EXFIL_NETWORK_REQUESTS · scripts/fetch_latest_tags.py:45
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 5b6f26075b |
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
with urllib.request.urlopen(req) as resp:
```
### MEDIUM · DATA_EXFIL_NETWORK_REQUESTS · scripts/fetch_latest_tags.py:51
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 87d89d6044 |
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
req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
```
### MEDIUM · DATA_EXFIL_NETWORK_REQUESTS · scripts/fetch_latest_tags.py:52
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 61d143c56e |
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
with urllib.request.urlopen(req) as resp:
```
## Other notes

8 metadata-quality / scan-coverage rows: MANIFEST_INVALID_NAME (4), MANIFEST_MISSING_LICENSE (4).
