# Skill `backend-f79082cdb7b0`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | GuilhermeInoe/Tcc |
| SKILL.md path | backend/skill.md |
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
### LOW · FILE_MAGIC_MISMATCH · README.md:
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 994cef4713 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | obfuscation |
| Analyzer | static |
| Evidence check | unavailable |
| Title | File extension does not match actual content type |
Evidence snippet:

```text

```
### LOW · SUPPLY_CHAIN_UNPINNED_DEPENDENCY · requirements.txt:1
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 60fe23110c |
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
fastapi>=0.110.0
```
### LOW · SUPPLY_CHAIN_UNPINNED_DEPENDENCY · requirements.txt:2
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 4676f7f564 |
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
uvicorn>=0.28.0
```
### LOW · SUPPLY_CHAIN_UNPINNED_DEPENDENCY · requirements.txt:3
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 30f1bd4d54 |
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
pydantic>=2.6.0
```
### LOW · SUPPLY_CHAIN_UNPINNED_DEPENDENCY · requirements.txt:4
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | b67f677277 |
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
python-dotenv>=1.0.1
```
### LOW · SUPPLY_CHAIN_UNPINNED_DEPENDENCY · requirements.txt:5
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 265a31218b |
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
google-genai>=0.3.0
```
## Other notes

4 metadata-quality / scan-coverage rows: MANIFEST_MISSING_LICENSE (4).
