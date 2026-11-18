# Skill `k8s-check-fix-c4645c57a44a`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | Ascend/agent-skills |
| SKILL.md path | skills/k8s-check-fix/SKILL.md |
| Sample stratum | scripts |
| Folder complete in GitSkills | True |
| Coverage | complete: every planned configuration produced a COMPLETE scan |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 3 | LOW | exit code 0 |
| SKILL.md only \| behavioral | COMPLETE | 3 | LOW | exit code 0 |
| Full folder \| default | COMPLETE | 7 | LOW | exit code 0 |
| Full folder \| behavioral | COMPLETE | 7 | LOW | exit code 0 |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### LOW · SUPPLY_CHAIN_UNPINNED_DEPENDENCY · SKILL.md:
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | e27f7b9a43 |
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
kubectl
```
### LOW · UNDECLARED_NETWORK_DESTINATION · scripts/lib/ preflight.sh:12
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | cc82d0562d |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | unauthorized_tool_use |
| Analyzer | static |
| Evidence check | unavailable |
| Title | Script contacts a destination the documentation never mentions |
Evidence snippet:

```text

```
### LOW · UNDECLARED_NETWORK_DESTINATION · scripts/lib/ preflight.sh:16
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 389b96a8b5 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | unauthorized_tool_use |
| Analyzer | static |
| Evidence check | unavailable |
| Title | Script contacts a destination the documentation never mentions |
Evidence snippet:

```text

```
### LOW · FILE_MAGIC_MISMATCH · templates/deployment_report_template.md:
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | fd707d499a |
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
### LOW · FILE_MAGIC_MISMATCH · templates/pod_autopsy_template.md:
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | f2b6cb5adb |
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
## Other notes

4 metadata-quality / scan-coverage rows: MANIFEST_MISSING_LICENSE (4).
