# Skill `skill-01e8f31dd5aa`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | daedalus/mcp-cryptography |
| SKILL.md path | SKILL.md |
| Sample stratum | scripts |
| Folder complete in GitSkills | False |
| Coverage | no_complete_scan: Cisco ran, but no configuration produced a COMPLETE scan |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | PARTIAL | 1 | INFO | Cisco reported an analyzer failure (skill_loader: SkillLoadError:MISSING_REQUIRED_MANIFEST_FIELD) |
| SKILL.md only \| behavioral | PARTIAL | 1 | INFO | Cisco reported an analyzer failure (skill_loader: SkillLoadError:MISSING_REQUIRED_MANIFEST_FIELD) |
| Full folder \| default | PARTIAL | 17 | CRITICAL | Cisco reported an analyzer failure (skill_loader: SkillLoadError:MISSING_REQUIRED_MANIFEST_FIELD) |
| Full folder \| behavioral | PARTIAL | 17 | CRITICAL | Cisco reported an analyzer failure (skill_loader: SkillLoadError:MISSING_REQUIRED_MANIFEST_FIELD) |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### MEDIUM · FILE_MAGIC_MISMATCH · .bumpversion.cfg:
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | ea137f49ea |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | partial |
| Cisco category | obfuscation |
| Analyzer | static |
| Evidence check | unavailable |
| Title | File extension does not match actual content type |
Evidence snippet:

```text

```
### LOW · HIDDEN_DATA_FILE · .bumpversion.cfg:
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 99ceb99b74 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | partial |
| Cisco category | obfuscation |
| Analyzer | static |
| Evidence check | unavailable |
| Title | Hidden data file detected |
Evidence snippet:

```text

```
### LOW · HIDDEN_DATA_FILE · .pre-commit-config.yaml:
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | f934c8ed6e |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | partial |
| Cisco category | obfuscation |
| Analyzer | static |
| Evidence check | unavailable |
| Title | Hidden data file detected |
Evidence snippet:

```text

```
### LOW · SUPPLY_CHAIN_UNPINNED_DEPENDENCY · pyproject.toml:2
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 55ca56a18b |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | partial |
| Cisco category | supply_chain_attack |
| Analyzer | static |
| Evidence check | ambiguous |
| Title | Unpinned dependency |
Evidence snippet:

```text
hatch
```
### LOW · SUPPLY_CHAIN_UNPINNED_DEPENDENCY · pyproject.toml:6
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | be287bf128 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | partial |
| Cisco category | supply_chain_attack |
| Analyzer | static |
| Evidence check | exact |
| Title | Unpinned dependency |
Evidence snippet:

```text
cryptography
```
### LOW · SUPPLY_CHAIN_UNPINNED_DEPENDENCY · pyproject.toml:15
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | e0e3054bbf |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | partial |
| Cisco category | supply_chain_attack |
| Analyzer | static |
| Evidence check | exact |
| Title | Unpinned dependency |
Evidence snippet:

```text
fastmcp
```
### LOW · SUPPLY_CHAIN_UNPINNED_DEPENDENCY · pyproject.toml:19
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 739ea371d7 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | partial |
| Cisco category | supply_chain_attack |
| Analyzer | static |
| Evidence check | ambiguous |
| Title | Unpinned dependency |
Evidence snippet:

```text
ruff
```
### LOW · SUPPLY_CHAIN_UNPINNED_DEPENDENCY · pyproject.toml:20
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 7174cbdcac |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | partial |
| Cisco category | supply_chain_attack |
| Analyzer | static |
| Evidence check | ambiguous |
| Title | Unpinned dependency |
Evidence snippet:

```text
mypy
```
### LOW · SUPPLY_CHAIN_UNPINNED_DEPENDENCY · pyproject.toml:22
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | ae0dcf5b0d |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | partial |
| Cisco category | supply_chain_attack |
| Analyzer | static |
| Evidence check | exact |
| Title | Unpinned dependency |
Evidence snippet:

```text
pip-api
```
### LOW · SUPPLY_CHAIN_UNPINNED_DEPENDENCY · pyproject.toml:25
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | a4291f5c52 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | partial |
| Cisco category | supply_chain_attack |
| Analyzer | static |
| Evidence check | exact |
| Title | Unpinned dependency |
Evidence snippet:

```text
pytest
```
### LOW · SUPPLY_CHAIN_UNPINNED_DEPENDENCY · pyproject.toml:26
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | f1cfb16850 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | partial |
| Cisco category | supply_chain_attack |
| Analyzer | static |
| Evidence check | exact |
| Title | Unpinned dependency |
Evidence snippet:

```text
pytest-cov
```
### LOW · SUPPLY_CHAIN_UNPINNED_DEPENDENCY · pyproject.toml:27
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 60959babb8 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | partial |
| Cisco category | supply_chain_attack |
| Analyzer | static |
| Evidence check | exact |
| Title | Unpinned dependency |
Evidence snippet:

```text
pytest-mock
```
### LOW · SUPPLY_CHAIN_UNPINNED_DEPENDENCY · pyproject.toml:28
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | a91f7cf8dd |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | partial |
| Cisco category | supply_chain_attack |
| Analyzer | static |
| Evidence check | exact |
| Title | Unpinned dependency |
Evidence snippet:

```text
pytest-asyncio
```
### LOW · SUPPLY_CHAIN_UNPINNED_DEPENDENCY · pyproject.toml:29
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 5ebf2afcd5 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | partial |
| Cisco category | supply_chain_attack |
| Analyzer | static |
| Evidence check | exact |
| Title | Unpinned dependency |
Evidence snippet:

```text
hypothesis
```
### LOW · SUPPLY_CHAIN_UNPINNED_DEPENDENCY · pyproject.toml:35
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 652555d8e7 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | partial |
| Cisco category | supply_chain_attack |
| Analyzer | static |
| Evidence check | exact |
| Title | Unpinned dependency |
Evidence snippet:

```text
mcp-cryptography[dev,test,lint]
```
### CRITICAL · YARA_credential_harvesting_generic · tests/test_mcp.py:50
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 26b838adcd |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | partial |
| Cisco category | hardcoded_secrets |
| Analyzer | static |
| Evidence check | exact |
| Title | CREDENTIAL HARVESTING detected by YARA |
Evidence snippet:

```text
assert "-----BEGIN PRIVATE KEY-----[REDACTED]
