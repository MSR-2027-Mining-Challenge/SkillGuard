# Skill `kafka-event-driven-866d18f7c6c2`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | Psqasim/personal-ai-employee |
| SKILL.md path | .claude/skills/kafka-event-driven/SKILL.md |
| Sample stratum | scripts |
| Folder complete in GitSkills | True |
| Coverage | complete: every planned configuration produced a COMPLETE scan |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 7 | MEDIUM | exit code 0 |
| SKILL.md only \| behavioral | COMPLETE | 7 | MEDIUM | exit code 0 |
| Full folder \| default | COMPLETE | 7 | MEDIUM | exit code 0 |
| Full folder \| behavioral | COMPLETE | 7 | MEDIUM | exit code 0 |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### MEDIUM · YARA_autonomy_abuse_generic · SKILL.md:178
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 42f5b7e7de |
| Provisional label |  |
| Final (human) label |  |
| Configurations | SKILL.md only \| default; SKILL.md only \| behavioral; Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | autonomy_abuse |
| Analyzer | static |
| Evidence check | mismatch |
| Title | AUTONOMY ABUSE detected by YARA |
Evidence snippet:

```text
props.put("retries", Integer.MAX_VALUE); // Retry indefinitely
```
### MEDIUM · YARA_autonomy_abuse_generic · SKILL.md:277
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 831f07d2da |
| Provisional label |  |
| Final (human) label |  |
| Configurations | SKILL.md only \| default; SKILL.md only \| behavioral; Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | autonomy_abuse |
| Analyzer | static |
| Evidence check | mismatch |
| Title | AUTONOMY ABUSE detected by YARA |
Evidence snippet:

```text
## Error Handling Patterns
```
### MEDIUM · YARA_autonomy_abuse_generic · SKILL.md:279
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 4c0ebd1f3f |
| Provisional label |  |
| Final (human) label |  |
| Configurations | SKILL.md only \| default; SKILL.md only \| behavioral; Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | autonomy_abuse |
| Analyzer | static |
| Evidence check | mismatch |
| Title | AUTONOMY ABUSE detected by YARA |
Evidence snippet:

```text
### Producer Error Handling
```
### MEDIUM · YARA_autonomy_abuse_generic · SKILL.md:299
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | d12fbdf52d |
| Provisional label |  |
| Final (human) label |  |
| Configurations | SKILL.md only \| default; SKILL.md only \| behavioral; Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | autonomy_abuse |
| Analyzer | static |
| Evidence check | mismatch |
| Title | AUTONOMY ABUSE detected by YARA |
Evidence snippet:

```text
### Consumer Error Handling
```
### MEDIUM · YARA_autonomy_abuse_generic · SKILL.md:398
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 278481d9bd |
| Provisional label |  |
| Final (human) label |  |
| Configurations | SKILL.md only \| default; SKILL.md only \| behavioral; Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | autonomy_abuse |
| Analyzer | static |
| Evidence check | mismatch |
| Title | AUTONOMY ABUSE detected by YARA |
Evidence snippet:

```text
4. **Auto-commit without error handling** - Can lead to message loss
```
### MEDIUM · YARA_autonomy_abuse_generic · SKILL.md:446
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | cb3482c70a |
| Provisional label |  |
| Final (human) label |  |
| Configurations | SKILL.md only \| default; SKILL.md only \| behavioral; Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | autonomy_abuse |
| Analyzer | static |
| Evidence check | mismatch |
| Title | AUTONOMY ABUSE detected by YARA |
Evidence snippet:

```text
- `simple_producer.java` - Basic producer with error handling
```
## Other notes

4 metadata-quality / scan-coverage rows: MANIFEST_MISSING_LICENSE (4).
