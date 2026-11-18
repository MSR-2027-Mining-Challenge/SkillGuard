# Skill `hifi-math-tts-bebf863dcf05`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | b-vitamins/dotfiles |
| SKILL.md path | codex/skills/hifi-math-tts/SKILL.md |
| Sample stratum | scripts |
| Folder complete in GitSkills | True |
| Coverage | complete: every planned configuration produced a COMPLETE scan |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 1 | INFO | exit code 0 |
| SKILL.md only \| behavioral | COMPLETE | 1 | INFO | exit code 0 |
| Full folder \| default | COMPLETE | 3 | LOW | exit code 0 |
| Full folder \| behavioral | COMPLETE | 3 | LOW | exit code 0 |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### LOW · FILE_MAGIC_MISMATCH · assets/acceptance-review-prompt-template.md:
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 0f76fb7f02 |
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
### LOW · FILE_MAGIC_MISMATCH · assets/line-by-line-audit-prompt-template.md:
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | d803ae3745 |
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
