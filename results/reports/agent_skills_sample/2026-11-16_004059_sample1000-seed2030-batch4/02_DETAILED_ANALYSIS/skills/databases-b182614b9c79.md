# Skill `databases-b182614b9c79`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | Biyocon/CustomAgents |
| SKILL.md path | .vscode/archive/upstream-skills/skills/databases/SKILL.md |
| Sample stratum | scripts |
| Folder complete in GitSkills | False |
| Coverage | complete: every planned configuration produced a COMPLETE scan |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 0 | SAFE | exit code 0 |
| SKILL.md only \| behavioral | COMPLETE | 0 | SAFE | exit code 0 |
| Full folder \| default | COMPLETE | 7 | LOW | exit code 0 |
| Full folder \| behavioral | COMPLETE | 7 | LOW | exit code 0 |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### LOW · SUPPLY_CHAIN_UNPINNED_DEPENDENCY · scripts/requirements.txt:7
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | ba4d63472f |
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
| Review ID | 455b2dcbce |
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
| Review ID | 0b0da32fbe |
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
| Review ID | bccdb88fe5 |
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
pytest>=7.0.0
```
### LOW · SUPPLY_CHAIN_UNPINNED_DEPENDENCY · scripts/tests/requirements.txt:2
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 88c1e8f53e |
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
pytest-cov>=4.0.0
```
### LOW · SUPPLY_CHAIN_UNPINNED_DEPENDENCY · scripts/tests/requirements.txt:3
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 3b3d116f58 |
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
pytest-mock>=3.10.0
```
### LOW · SUPPLY_CHAIN_UNPINNED_DEPENDENCY · scripts/tests/requirements.txt:4
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | a880945eef |
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
mongomock>=4.1.0
```
## Other notes

0 metadata-quality / scan-coverage rows: .
