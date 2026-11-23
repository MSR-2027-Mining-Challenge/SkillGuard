# Skill `review-l10n-22be0b42ed0e`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | a-ghorbani/pocketpal-dev-team |
| SKILL.md path | skills/review-l10n/SKILL.md |
| Sample stratum | scripts |
| Folder complete in GitSkills | True |
| Coverage | complete: every planned configuration produced a COMPLETE scan |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 1 | INFO | exit code 0 |
| SKILL.md only \| behavioral | COMPLETE | 1 | INFO | exit code 0 |
| Full folder \| default | COMPLETE | 2 | MEDIUM | exit code 0 |
| Full folder \| behavioral | COMPLETE | 2 | MEDIUM | exit code 0 |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### MEDIUM · DATA_EXFIL_JS_NETWORK · scripts/apply-plan.mjs:114
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | fb34843fb4 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | data_exfiltration |
| Analyzer | static |
| Evidence check | exact |
| Title | Outbound network request primitives in JavaScript/TypeScript |
Evidence snippet:

```text
const res = await fetch(url, {
```
## Other notes

4 metadata-quality / scan-coverage rows: MANIFEST_MISSING_LICENSE (4).
