# Skill `implementing-canary-tokens-for-netw-07811ef04df1`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | YomMongkolphanna/SECURITY_BRAIN |
| SKILL.md path | security_brain/brain/ai_agent/skills/anthropic/implementing-canary-tokens-for-network-intrusion/SKILL.md |
| Sample stratum | skill_md_only |
| Folder complete in GitSkills | True |
| Coverage | complete: every planned configuration produced a COMPLETE scan |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 2 | LOW | exit code 0 |
| SKILL.md only \| behavioral | COMPLETE | 6 | MEDIUM | exit code 0 |
| Full folder \| default | COMPLETE | 2 | LOW | exit code 0 |
| Full folder \| behavioral | COMPLETE | 6 | MEDIUM | exit code 0 |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### MEDIUM · MDBLOCK_PYTHON_HTTP_POST · SKILL.md:65
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 4db3b678fe |
| Provisional label |  |
| Final (human) label |  |
| Configurations | SKILL.md only \| behavioral; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | data_exfiltration |
| Analyzer | behavioral |
| Evidence check | ambiguous |
| Title | Python code block sends HTTP POST request |
Evidence snippet:

```text
response = requests.post("https://canarytokens.org/generate", data={
```
### MEDIUM · MDBLOCK_PYTHON_HTTP_POST · SKILL.md:91
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | abaceb29fa |
| Provisional label |  |
| Final (human) label |  |
| Configurations | SKILL.md only \| behavioral; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | data_exfiltration |
| Analyzer | behavioral |
| Evidence check | ambiguous |
| Title | Python code block sends HTTP POST request |
Evidence snippet:

```text
response = requests.post("https://canarytokens.org/generate", data={
```
### MEDIUM · MDBLOCK_PYTHON_HTTP_POST · SKILL.md:117
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | d5d985c302 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | SKILL.md only \| behavioral; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | data_exfiltration |
| Analyzer | behavioral |
| Evidence check | ambiguous |
| Title | Python code block sends HTTP POST request |
Evidence snippet:

```text
response = requests.post("https://canarytokens.org/generate", data={
```
### MEDIUM · MDBLOCK_PYTHON_HTTP_POST · SKILL.md:165
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 2e545c9f3f |
| Provisional label |  |
| Final (human) label |  |
| Configurations | SKILL.md only \| behavioral; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | data_exfiltration |
| Analyzer | behavioral |
| Evidence check | mismatch |
| Title | Python code block sends HTTP POST request |
Evidence snippet:

```text
requests.post(webhook_url, json=payload, timeout=10)
```
## Other notes

8 metadata-quality / scan-coverage rows: SOCIAL_ENG_VAGUE_DESCRIPTION (4), MANIFEST_MISSING_LICENSE (4).
