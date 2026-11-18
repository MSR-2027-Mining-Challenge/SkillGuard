# Skill `05-remote-download-execute-93beb740007e`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | charliechenye/SkillGate |
| SKILL.md path | fixtures/benchmark/05-remote-download-execute/SKILL.md |
| Sample stratum | scripts |
| Folder complete in GitSkills | True |
| Coverage | no_complete_scan: Cisco ran, but no configuration produced a COMPLETE scan |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | PARTIAL | 1 | INFO | Cisco reported an analyzer failure (skill_loader: SkillLoadError:MISSING_REQUIRED_MANIFEST_FIELD) |
| SKILL.md only \| behavioral | PARTIAL | 1 | INFO | Cisco reported an analyzer failure (skill_loader: SkillLoadError:MISSING_REQUIRED_MANIFEST_FIELD) |
| Full folder \| default | PARTIAL | 2 | HIGH | Cisco reported an analyzer failure (skill_loader: SkillLoadError:MISSING_REQUIRED_MANIFEST_FIELD) |
| Full folder \| behavioral | PARTIAL | 2 | HIGH | Cisco reported an analyzer failure (skill_loader: SkillLoadError:MISSING_REQUIRED_MANIFEST_FIELD) |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### HIGH · CORRELATED_NETWORK_EXECUTION_FLOW · scripts/install.sh:2
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 4e6c4ae2c5 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | partial |
| Cisco category | command_injection |
| Analyzer | correlation |
| Evidence check | unavailable |
| Title | Network-derived content reaches code execution |
Evidence snippet:

```text

```
## Other notes

4 metadata-quality / scan-coverage rows: SKILL_LOAD_FALLBACK_USED (4).
