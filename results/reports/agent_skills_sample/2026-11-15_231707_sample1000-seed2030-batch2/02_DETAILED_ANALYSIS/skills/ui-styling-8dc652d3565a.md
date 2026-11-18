# Skill `ui-styling-8dc652d3565a`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | hontauadrian/sfx-app-empty-test |
| SKILL.md path | .overstory/claude-profiles/builder/skills/ui-styling/SKILL.md |
| Sample stratum | scripts |
| Folder complete in GitSkills | False |
| Coverage | complete: every planned configuration produced a COMPLETE scan |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 1 | INFO | exit code 0 |
| SKILL.md only \| behavioral | COMPLETE | 1 | INFO | exit code 0 |
| Full folder \| default | COMPLETE | 7 | LOW | exit code 0 |
| Full folder \| behavioral | COMPLETE | 7 | LOW | exit code 0 |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### LOW · SUPPLY_CHAIN_UNPINNED_DEPENDENCY · scripts/requirements.txt:7
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 28c7a04180 |
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
pytest>=8.0.0
```
### LOW · SUPPLY_CHAIN_UNPINNED_DEPENDENCY · scripts/requirements.txt:8
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 7b13a5190f |
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
pytest-cov>=4.1.0
```
### LOW · SUPPLY_CHAIN_UNPINNED_DEPENDENCY · scripts/requirements.txt:9
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 40864310fb |
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
pytest-mock>=3.12.0
```
### LOW · SUPPLY_CHAIN_UNPINNED_DEPENDENCY · scripts/tests/requirements.txt:1
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 509b64aa8a |
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
pytest>=7.4.0
```
### LOW · SUPPLY_CHAIN_UNPINNED_DEPENDENCY · scripts/tests/requirements.txt:2
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 7068c9b9e0 |
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
pytest-cov>=4.1.0
```
### LOW · SUPPLY_CHAIN_UNPINNED_DEPENDENCY · scripts/tests/requirements.txt:3
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 0e57d9bfea |
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
pytest-mock>=3.11.1
```
## Other notes

4 metadata-quality / scan-coverage rows: MANIFEST_INVALID_NAME (4).
