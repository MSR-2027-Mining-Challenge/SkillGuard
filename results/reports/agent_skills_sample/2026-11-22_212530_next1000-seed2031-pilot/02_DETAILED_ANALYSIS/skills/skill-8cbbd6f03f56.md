# Skill `skill-8cbbd6f03f56`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | HBConline/orangepi4pro-skill |
| SKILL.md path | SKILL.md |
| Sample stratum | supporting_no_scripts |
| Folder complete in GitSkills | False |
| Coverage | complete: every planned configuration produced a COMPLETE scan |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 3 | CRITICAL | exit code 0 |
| SKILL.md only \| behavioral | COMPLETE | 5 | CRITICAL | exit code 0 |
| Full folder \| default | COMPLETE | 3 | CRITICAL | exit code 0 |
| Full folder \| behavioral | COMPLETE | 5 | CRITICAL | exit code 0 |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### HIGH · ACTIVE_DYNAMIC_EXECUTION · SKILL.md:2287
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | c2dde0fd9f |
| Provisional label |  |
| Final (human) label |  |
| Configurations | SKILL.md only \| default; SKILL.md only \| behavioral; Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | command_injection |
| Analyzer | static |
| Evidence check | exact |
| Title | Active instruction invokes dynamic code or process execution |
Evidence snippet:

```text
result = subprocess.run(['hostname', '-I'], capture_output=True, text=True)
```
### CRITICAL · YARA_command_injection_generic · SKILL.md:2679
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 5984f3d440 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | SKILL.md only \| default; SKILL.md only \| behavioral; Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | command_injection |
| Analyzer | static |
| Evidence check | mismatch |
| Title | INJECTION ATTACK detected by YARA |
Evidence snippet:

```text
sudo dd if=/dev/zero of=/mnt/nvme/swapfile bs=1M count=2048
```
### MEDIUM · MDBLOCK_PYTHON_SUBPROCESS · SKILL.md:2281
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 571f388db8 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | SKILL.md only \| behavioral; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | command_injection |
| Analyzer | behavioral |
| Evidence check | mismatch |
| Title | Python code block executes shell commands |
Evidence snippet:

```text
result = subprocess.run(['hostname', '-I'], capture_output=True, text=True)
```
### MEDIUM · MDBLOCK_PYTHON_SUBPROCESS · SKILL.md:2333
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | d841269823 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | SKILL.md only \| behavioral; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | command_injection |
| Analyzer | behavioral |
| Evidence check | mismatch |
| Title | Python code block executes shell commands |
Evidence snippet:

```text
result = subprocess.run(cmd, cwd=os.path.expanduser("~/ai-sdk/examples/yolov5/build"),
```
## Other notes

4 metadata-quality / scan-coverage rows: MANIFEST_MISSING_LICENSE (4).
