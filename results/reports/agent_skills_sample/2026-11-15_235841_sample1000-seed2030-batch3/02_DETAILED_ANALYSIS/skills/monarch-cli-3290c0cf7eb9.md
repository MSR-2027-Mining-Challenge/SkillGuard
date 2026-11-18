# Skill `monarch-cli-3290c0cf7eb9`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | adbertram/cli-tools |
| SKILL.md path | _repo/skills/monarch-cli/SKILL.md |
| Sample stratum | scripts |
| Folder complete in GitSkills | True |
| Coverage | complete: every planned configuration produced a COMPLETE scan |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 1 | INFO | exit code 0 |
| SKILL.md only \| behavioral | COMPLETE | 1 | INFO | exit code 0 |
| Full folder \| default | COMPLETE | 6 | MEDIUM | exit code 0 |
| Full folder \| behavioral | COMPLETE | 6 | MEDIUM | exit code 0 |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### MEDIUM · FILE_MAGIC_MISMATCH · scripts/apply-approved-updates.sh:
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | d0bbc1746b |
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
### MEDIUM · FILE_MAGIC_MISMATCH · scripts/build-output.sh:
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 35e9a642c2 |
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
### MEDIUM · FILE_MAGIC_MISMATCH · scripts/build-rule-command.sh:
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 1d8a181e93 |
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
### MEDIUM · FILE_MAGIC_MISMATCH · scripts/classify-venmo.sh:
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | f9aff093e6 |
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
### MEDIUM · FILE_MAGIC_MISMATCH · scripts/prepare-review.sh:
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | d50df84b7a |
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
