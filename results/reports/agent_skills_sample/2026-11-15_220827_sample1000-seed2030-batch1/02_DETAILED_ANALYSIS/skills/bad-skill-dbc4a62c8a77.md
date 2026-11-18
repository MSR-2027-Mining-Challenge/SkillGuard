# Skill `bad-skill-dbc4a62c8a77`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | pdugan20/claudelint |
| SKILL.md path | tests/fixtures/projects/invalid-all-categories/.claude/skills/bad-skill/SKILL.md |
| Sample stratum | scripts |
| Folder complete in GitSkills | True |
| Coverage | complete: every planned configuration produced a COMPLETE scan |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 3 | LOW | exit code 0 |
| SKILL.md only \| behavioral | COMPLETE | 3 | LOW | exit code 0 |
| Full folder \| default | COMPLETE | 4 | MEDIUM | exit code 0 |
| Full folder \| behavioral | COMPLETE | 4 | MEDIUM | exit code 0 |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### MEDIUM · CORRELATED_MANIFEST_CAPABILITY_MISMATCH · bad-skill.sh:9
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 699ad8d449 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | unauthorized_tool_use |
| Analyzer | correlation |
| Evidence check | unavailable |
| Title | Implementation exceeds declared skill capabilities |
Evidence snippet:

```text

```
## Other notes

12 metadata-quality / scan-coverage rows: SOCIAL_ENG_VAGUE_DESCRIPTION (4), MANIFEST_INVALID_NAME (4), MANIFEST_MISSING_LICENSE (4).
