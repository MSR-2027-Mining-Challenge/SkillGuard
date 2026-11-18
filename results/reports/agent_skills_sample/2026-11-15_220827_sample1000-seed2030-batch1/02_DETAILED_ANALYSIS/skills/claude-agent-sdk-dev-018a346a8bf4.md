# Skill `claude-agent-sdk-dev-018a346a8bf4`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | Airmomo/skills |
| SKILL.md path | claude-agent-sdk-dev/SKILL.md |
| Sample stratum | scripts |
| Folder complete in GitSkills | True |
| Coverage | complete: every planned configuration produced a COMPLETE scan |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 1 | INFO | exit code 0 |
| SKILL.md only \| behavioral | COMPLETE | 1 | INFO | exit code 0 |
| Full folder \| default | COMPLETE | 4 | LOW | exit code 0 |
| Full folder \| behavioral | COMPLETE | 4 | LOW | exit code 0 |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### LOW · SUPPLY_CHAIN_UNPINNED_DEPENDENCY · examples/minimal-typescript/package.json:10
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | ec55d442e3 |
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
"@anthropic-ai/claude-agent-sdk": "^0.1.0"
```
### LOW · SUPPLY_CHAIN_UNPINNED_DEPENDENCY · examples/minimal-typescript/package.json:13
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | cf2d623bf1 |
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
"tsx": "^4.19.0"
```
### LOW · SUPPLY_CHAIN_UNPINNED_DEPENDENCY · examples/minimal-typescript/package.json:14
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | e95f70c8b0 |
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
"typescript": "^5.5.0"
```
## Other notes

4 metadata-quality / scan-coverage rows: MANIFEST_MISSING_LICENSE (4).
