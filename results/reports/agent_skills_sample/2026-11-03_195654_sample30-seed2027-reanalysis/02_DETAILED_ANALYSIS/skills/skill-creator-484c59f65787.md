# Skill `skill-creator-484c59f65787`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | niekbeckers/skills |
| SKILL.md path | skills/skill-creator/SKILL.md |
| Sample stratum | scripts |
| Folder complete in GitSkills | True |
| Coverage | complete: every planned configuration produced a COMPLETE scan |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 1 | INFO | exit code 0 |
| SKILL.md only \| behavioral | COMPLETE | 1 | INFO | exit code 0 |
| Full folder \| default | COMPLETE | 3 | CRITICAL | exit code 0 |
| Full folder \| behavioral | COMPLETE | 3 | CRITICAL | exit code 0 |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### CRITICAL · COMMAND_INJECTION_OS_SYSTEM · eval-viewer/generate_review.py:390
|  | value |
|---|---|
| Validation | Provisional label (AI-assisted, not independent human review) |
| Review ID | f0f315b409 |
| Provisional label | scanner_parser_issue |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | command_injection |
| Analyzer | static |
| Evidence check | exact |
| Title | Shell command execution with string formatting (potential injection) |
Evidence snippet:

```text
result = subprocess.run(
```
### MEDIUM · FILE_MAGIC_MISMATCH · scripts/__init__.py:
|  | value |
|---|---|
| Validation | Provisional label (AI-assisted, not independent human review) |
| Review ID | 39cb711dfc |
| Provisional label | scanner_parser_issue |
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
