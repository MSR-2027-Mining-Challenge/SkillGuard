# Skill `productboard-expert-869f240c2ada`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | borghei/Claude-Skills |
| SKILL.md path | project-management/productboard-expert/SKILL.md |
| Sample stratum | supporting_no_scripts |
| Folder complete in GitSkills | True |
| Coverage | complete: every planned configuration produced a COMPLETE scan |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 0 | SAFE | exit code 0 |
| SKILL.md only \| behavioral | COMPLETE | 0 | SAFE | exit code 0 |
| Full folder \| default | COMPLETE | 0 | SAFE | exit code 0 |
| Full folder \| behavioral | COMPLETE | 1 | MEDIUM | exit code 0 |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### MEDIUM · MDBLOCK_PYTHON_HTTP_POST · examples/wayfinder-productboard-setup.md:205
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 2ee410126a |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | data_exfiltration |
| Analyzer | behavioral |
| Evidence check | mismatch |
| Title | Python code block sends HTTP POST request |
Evidence snippet:

```text
res = requests.post(f"{PB_API}/features", headers=HEADERS, json=body)
```
## Other notes

0 metadata-quality / scan-coverage rows: .
