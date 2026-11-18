# Skill `adk-skill-4aa83b5bc710`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | miticojo/adk-skill |
| SKILL.md path | adk-skill/SKILL.md |
| Sample stratum | supporting_no_scripts |
| Folder complete in GitSkills | True |
| Coverage | complete: every planned configuration produced a COMPLETE scan |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 0 | SAFE | exit code 0 |
| SKILL.md only \| behavioral | COMPLETE | 0 | SAFE | exit code 0 |
| Full folder \| default | COMPLETE | 0 | SAFE | exit code 0 |
| Full folder \| behavioral | COMPLETE | 2 | HIGH | exit code 0 |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### HIGH · MDBLOCK_PYTHON_EVAL_EXEC · references/tools-reference.md:11
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 06e3f1fd2e |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | command_injection |
| Analyzer | behavioral |
| Evidence check | mismatch |
| Title | Python code block uses eval/exec |
Evidence snippet:

```text
return str(eval(expression))
```
### HIGH · MDBLOCK_PYTHON_EVAL_EXEC · references/tools-reference.md:103
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 2cbbb89d79 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | command_injection |
| Analyzer | behavioral |
| Evidence check | mismatch |
| Title | Python code block uses eval/exec |
Evidence snippet:

```text
retrieval_tool = VertexAiRagRetrieval(
```
## Other notes

0 metadata-quality / scan-coverage rows: .
