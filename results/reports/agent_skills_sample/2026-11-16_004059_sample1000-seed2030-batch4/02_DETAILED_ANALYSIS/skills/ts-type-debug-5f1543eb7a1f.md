# Skill `ts-type-debug-5f1543eb7a1f`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | yoyooyooo/logix |
| SKILL.md path | .agent/skills/ts-type-debug/SKILL.md |
| Sample stratum | scripts |
| Folder complete in GitSkills | True |
| Coverage | complete: every planned configuration produced a COMPLETE scan |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 1 | INFO | exit code 0 |
| SKILL.md only \| behavioral | COMPLETE | 1 | INFO | exit code 0 |
| Full folder \| default | COMPLETE | 3 | LOW | exit code 0 |
| Full folder \| behavioral | COMPLETE | 3 | LOW | exit code 0 |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### LOW · SUPPLY_CHAIN_UNPINNED_DEPENDENCY · package.json:9
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 53f5506a8e |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | supply_chain_attack |
| Analyzer | static |
| Evidence check | exact |
| Title | Unpinned dependency |
Evidence snippet:

```text
"ts-morph": "^25.0.0"
```
### LOW · SUPPLY_CHAIN_UNPINNED_DEPENDENCY · package.json:10
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 25a7e4a18c |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | supply_chain_attack |
| Analyzer | static |
| Evidence check | exact |
| Title | Unpinned dependency |
Evidence snippet:

```text
"tsx": "^4.19.2"
```
## Other notes

4 metadata-quality / scan-coverage rows: MANIFEST_MISSING_LICENSE (4).
