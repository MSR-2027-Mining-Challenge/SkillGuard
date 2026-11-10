# Skill `youtube-content-7162d1c45997`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | theheavenlyd3mon/hermes-profiles |
| SKILL.md path | profiles/educate/skills/media/youtube-content/SKILL.md |
| Sample stratum | scripts |
| Folder complete in GitSkills | True |
| Coverage | complete: every planned configuration produced a COMPLETE scan |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 2 | HIGH | exit code 0 |
| SKILL.md only \| behavioral | COMPLETE | 3 | HIGH | exit code 0 |
| Full folder \| default | COMPLETE | 2 | HIGH | exit code 0 |
| Full folder \| behavioral | COMPLETE | 4 | HIGH | exit code 0 |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### HIGH · ACTIVE_DYNAMIC_EXECUTION · SKILL.md:169
|  | value |
|---|---|
| Validation | Provisional label (AI-assisted, not independent human review) |
| Review ID | 9cbcff225f |
| Provisional label | intentional |
| Final (human) label |  |
| Configurations | SKILL.md only \| default; SKILL.md only \| behavioral; Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | command_injection |
| Analyzer | static |
| Evidence check | exact |
| Title | Active instruction invokes dynamic code or process execution |
Evidence snippet:

```text
r = subprocess.run([
```
### MEDIUM · MDBLOCK_PYTHON_SUBPROCESS · SKILL.md:162
|  | value |
|---|---|
| Validation | Provisional label (AI-assisted, not independent human review) |
| Review ID | d1c1fe72fc |
| Provisional label | intentional |
| Final (human) label |  |
| Configurations | SKILL.md only \| behavioral; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | command_injection |
| Analyzer | behavioral |
| Evidence check | mismatch |
| Title | Python code block executes shell commands |
Evidence snippet:

```text
r = subprocess.run([
```
### MEDIUM · MDBLOCK_PYTHON_SUBPROCESS · references/ytdlp-quirks.md:69
|  | value |
|---|---|
| Validation | Provisional label (AI-assisted, not independent human review) |
| Review ID | 018ac4e2f1 |
| Provisional label | intentional |
| Final (human) label |  |
| Configurations | Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | command_injection |
| Analyzer | behavioral |
| Evidence check | mismatch |
| Title | Python code block executes shell commands |
Evidence snippet:

```text
r = subprocess.run(['curl', '-s', '-L', '--max-time', '30',
```
## Other notes

4 metadata-quality / scan-coverage rows: MANIFEST_MISSING_LICENSE (4).
