# Skill `opensea-swaps-1de502b10011`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | Pieverse-Eng/purrfect-skills |
| SKILL.md path | opensea/vendor/opensea-swaps/SKILL.md |
| Sample stratum | scripts |
| Folder complete in GitSkills | True |
| Coverage | complete: every planned configuration produced a COMPLETE scan |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 3 | LOW | exit code 0 |
| SKILL.md only \| behavioral | COMPLETE | 3 | LOW | exit code 0 |
| Full folder \| default | COMPLETE | 3 | LOW | exit code 0 |
| Full folder \| behavioral | COMPLETE | 3 | LOW | exit code 0 |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### LOW · SUPPLY_CHAIN_UNPINNED_DEPENDENCY · SKILL.md:
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 5b9aeb2e14 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | SKILL.md only \| default; SKILL.md only \| behavioral; Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | supply_chain_attack |
| Analyzer | static |
| Evidence check | unavailable |
| Title | Unpinned dependency |
Evidence snippet:

```text
node >= 18.0.0
```
## Other notes

0 metadata-quality / scan-coverage rows: .
