# Skill `fsl-multi-region-architecture-37a3133b9baa`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | BanibrataChatterjee/AwesomeSalesforceSkills |
| SKILL.md path | skills/architect/fsl-multi-region-architecture/SKILL.md |
| Sample stratum | scripts |
| Folder complete in GitSkills | True |
| Coverage | complete: every planned configuration produced a COMPLETE scan |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 2 | LOW | exit code 0 |
| SKILL.md only \| behavioral | COMPLETE | 2 | LOW | exit code 0 |
| Full folder \| default | COMPLETE | 2 | LOW | exit code 0 |
| Full folder \| behavioral | COMPLETE | 2 | LOW | exit code 0 |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### LOW · SUPPLY_CHAIN_UNPINNED_DEPENDENCY · SKILL.md:
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 7ec2cf2ef4 |
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
architect/fsl-optimization-architecture
```
## Other notes

4 metadata-quality / scan-coverage rows: MANIFEST_MISSING_LICENSE (4).
