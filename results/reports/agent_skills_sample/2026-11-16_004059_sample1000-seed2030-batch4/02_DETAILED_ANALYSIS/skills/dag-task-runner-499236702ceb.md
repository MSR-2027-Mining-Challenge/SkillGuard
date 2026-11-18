# Skill `dag-task-runner-499236702ceb`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | ArdenoStudio/dinaya |
| SKILL.md path | apple-ultra-skills/dag-task-runner/SKILL.md |
| Sample stratum | scripts |
| Folder complete in GitSkills | False |
| Coverage | complete: every planned configuration produced a COMPLETE scan |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 1 | INFO | exit code 0 |
| SKILL.md only \| behavioral | COMPLETE | 1 | INFO | exit code 0 |
| Full folder \| default | COMPLETE | 5 | LOW | exit code 0 |
| Full folder \| behavioral | COMPLETE | 5 | LOW | exit code 0 |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### LOW · SUPPLY_CHAIN_UNPINNED_DEPENDENCY · scripts/package.json:20
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 3ca4ad1d77 |
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
"@cursor/sdk": "^1.0.9"
```
### LOW · SUPPLY_CHAIN_UNPINNED_DEPENDENCY · scripts/package.json:23
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 7080eecf90 |
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
"@types/node": "^25.6.0"
```
### LOW · SUPPLY_CHAIN_UNPINNED_DEPENDENCY · scripts/package.json:24
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | e629bc4178 |
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
"tsx": "^4.21.0"
```
### LOW · SUPPLY_CHAIN_UNPINNED_DEPENDENCY · scripts/package.json:25
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | f6fce48e19 |
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
"typescript": "^6.0.3"
```
## Other notes

4 metadata-quality / scan-coverage rows: MANIFEST_MISSING_LICENSE (4).
