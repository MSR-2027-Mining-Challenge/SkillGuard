# Skill `lxc-setup-dcc11cf17ae2`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | ssrjkk/claude-skills |
| SKILL.md path | .claude/skills/devops/lxc-setup/SKILL.md |
| Sample stratum | supporting_no_scripts |
| Folder complete in GitSkills | True |
| Coverage | complete: every planned configuration produced a COMPLETE scan |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 1 | INFO | exit code 0 |
| SKILL.md only \| behavioral | COMPLETE | 1 | INFO | exit code 0 |
| Full folder \| default | COMPLETE | 1 | INFO | exit code 0 |
| Full folder \| behavioral | COMPLETE | 1 | INFO | exit code 0 |
| SKILL.md only \| behavioral+llm | COMPLETE | 2 | LOW | exit code 0 |
| SKILL.md only \| behavioral+meta | COMPLETE | 1 | INFO | exit code 0 |
| SKILL.md only \| behavioral+llm+meta | COMPLETE | 2 | LOW | exit code 0 |
| Full folder \| behavioral+llm | COMPLETE | 2 | LOW | exit code 0 |
| Full folder \| behavioral+meta | COMPLETE | 1 | INFO | exit code 0 |
| Full folder \| behavioral+llm+meta | COMPLETE | 2 | LOW | exit code 0 |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### LOW · LLM_POLICY_VIOLATION · :
|  | value |
|---|---|
| Validation | Scanner alert, not in the review queue |
| Review ID |  |
| Provisional label |  |
| Final (human) label |  |
| Configurations | SKILL.md only \| behavioral+llm; SKILL.md only \| behavioral+llm+meta; Full folder \| behavioral+llm+meta |
| Scan outcomes | complete |
| Cisco category | policy_violation |
| Analyzer | llm |
| Evidence check | unavailable |
| Title | Missing license specification in manifest |
Evidence snippet:

```text
YAML Manifest Details [evidence_id=SRC:bd43a7da36c1cfe1]: - name: lxc-setup - description: Setup with LXC. installation. - license: Not specified - compatibility: Not specified - allowed-tools: Not specified - additional metadata: {'category': 'devops', 'tags': ['lxc', 'setup', 'devops', 'container'], 'models': ['gpt-4', 'claude-3'], 'version': '1.0'}
```
### LOW · LLM_PROMPT_INJECTION · SKILL.md:
|  | value |
|---|---|
| Validation | Scanner alert, not in the review queue |
| Review ID |  |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| behavioral+llm |
| Scan outcomes | complete |
| Cisco category | prompt_injection |
| Analyzer | llm |
| Evidence check | unavailable |
| Title | Potential prompt injection in skill description |
Evidence snippet:

```text
Setup with LXC. installation.
```
## Other notes

10 metadata-quality / scan-coverage rows: MANIFEST_MISSING_LICENSE (10).
