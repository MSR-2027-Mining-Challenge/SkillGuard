# Skill `linkedin-job-scraper-217ba2f48a2e`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | robomotionio/robomotion-skills |
| SKILL.md path | robomotion-gtm-skills/skills/linkedin-job-scraper/SKILL.md |
| Sample stratum | scripts |
| Folder complete in GitSkills | False |
| Coverage | complete: every planned configuration produced a COMPLETE scan |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 1 | INFO | exit code 0 |
| SKILL.md only \| behavioral | COMPLETE | 1 | INFO | exit code 0 |
| Full folder \| default | COMPLETE | 9 | HIGH | exit code 0 |
| Full folder \| behavioral | COMPLETE | 9 | HIGH | exit code 0 |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### MEDIUM · TOOL_ABUSE_UNDECLARED_NETWORK · SKILL.md:
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 47bfc25c92 |
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
### LOW · UNDECLARED_NETWORK_DESTINATION · scripts/linkedin_jobs.py:26
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 0c7f4a06f7 |
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
### LOW · UNDECLARED_NETWORK_DESTINATION · scripts/linkedin_jobs.py:48
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | c1e7ae64b8 |
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
### MEDIUM · DATA_EXFIL_NETWORK_REQUESTS · scripts/linkedin_jobs.py:51
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 13e7efd31f |
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
req = urllib.request.Request(url, data=data, method="POST",
```
### HIGH · CORRELATED_SENSITIVE_NETWORK_FLOW · scripts/linkedin_jobs.py:55
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 94d820c6d5 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | data_exfiltration |
| Analyzer | correlation |
| Evidence check | unavailable |
| Title | Sensitive source reaches a network sink |
Evidence snippet:

```text

```
### MEDIUM · DATA_EXFIL_NETWORK_REQUESTS · scripts/linkedin_jobs.py:55
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 2f673f4200 |
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
with urllib.request.urlopen(req, timeout=120) as r:
```
### MEDIUM · DATA_EXFIL_NETWORK_REQUESTS · scripts/linkedin_jobs.py:83
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 44910095a2 |
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
req = urllib.request.Request(DDG, data=data, headers={"User-Agent": UA})
```
### MEDIUM · DATA_EXFIL_NETWORK_REQUESTS · scripts/linkedin_jobs.py:86
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 85199edf4f |
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
with urllib.request.urlopen(req, timeout=30) as r:
```
## Other notes

4 metadata-quality / scan-coverage rows: MANIFEST_MISSING_LICENSE (4).
