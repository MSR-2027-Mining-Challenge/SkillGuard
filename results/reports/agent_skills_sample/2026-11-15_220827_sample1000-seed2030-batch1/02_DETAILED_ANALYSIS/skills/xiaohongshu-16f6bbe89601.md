# Skill `xiaohongshu-16f6bbe89601`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | Demerzels-lab/elsamultiskillagent |
| SKILL.md path | public/skills/heiheimaoya/xiaohongshu/SKILL.md |
| Sample stratum | scripts |
| Folder complete in GitSkills | False |
| Coverage | no_complete_scan: Cisco ran, but no configuration produced a COMPLETE scan |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | PARTIAL | 1 | INFO | Cisco reported an analyzer failure (skill_loader: SkillLoadError:MISSING_REQUIRED_MANIFEST_FIELD) |
| SKILL.md only \| behavioral | PARTIAL | 1 | INFO | Cisco reported an analyzer failure (skill_loader: SkillLoadError:MISSING_REQUIRED_MANIFEST_FIELD) |
| Full folder \| default | PARTIAL | 5 | HIGH | Cisco reported an analyzer failure (skill_loader: SkillLoadError:MISSING_REQUIRED_MANIFEST_FIELD) |
| Full folder \| behavioral | PARTIAL | 5 | HIGH | Cisco reported an analyzer failure (skill_loader: SkillLoadError:MISSING_REQUIRED_MANIFEST_FIELD) |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### LOW · UNDECLARED_NETWORK_DESTINATION · scripts/render_xhs_v2.py:317
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | c15b5f1d28 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | partial |
| Cisco category | unauthorized_tool_use |
| Analyzer | static |
| Evidence check | unavailable |
| Title | Script contacts a destination the documentation never mentions |
Evidence snippet:

```text

```
### LOW · UNDECLARED_NETWORK_DESTINATION · scripts/sign_server.py:65
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 3321eed709 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | partial |
| Cisco category | unauthorized_tool_use |
| Analyzer | static |
| Evidence check | unavailable |
| Title | Script contacts a destination the documentation never mentions |
Evidence snippet:

```text

```
### HIGH · RESOURCE_ABUSE_INFINITE_LOOP · scripts/sign_server.py:151
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 5fa02177ac |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | partial |
| Cisco category | resource_abuse |
| Analyzer | static |
| Evidence check | exact |
| Title | Infinite loop without clear exit condition |
Evidence snippet:

```text
while True:
```
### LOW · UNDECLARED_NETWORK_DESTINATION · workflow.py:73
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 3473b4bfed |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | partial |
| Cisco category | unauthorized_tool_use |
| Analyzer | static |
| Evidence check | unavailable |
| Title | Script contacts a destination the documentation never mentions |
Evidence snippet:

```text

```
## Other notes

4 metadata-quality / scan-coverage rows: SKILL_LOAD_FALLBACK_USED (4).
