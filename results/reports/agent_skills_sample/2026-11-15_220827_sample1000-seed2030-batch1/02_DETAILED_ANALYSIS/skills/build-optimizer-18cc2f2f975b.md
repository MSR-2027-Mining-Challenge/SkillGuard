# Skill `build-optimizer-18cc2f2f975b`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | antgroup/Agent3Sigma-Canary |
| SKILL.md path | assets/skill_poison/skill_security_reviewer_benchmark_enhanced/risky-command-execution-rce/build-optimizer/SKILL.md |
| Sample stratum | scripts |
| Folder complete in GitSkills | True |
| Coverage | complete: every planned configuration produced a COMPLETE scan |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 1 | INFO | exit code 0 |
| SKILL.md only \| behavioral | COMPLETE | 1 | INFO | exit code 0 |
| Full folder \| default | COMPLETE | 11 | CRITICAL | exit code 0 |
| Full folder \| behavioral | COMPLETE | 11 | CRITICAL | exit code 0 |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### MEDIUM · TOOL_ABUSE_UNDECLARED_NETWORK · SKILL.md:
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 769cca41a2 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | unauthorized_tool_use |
| Analyzer | static |
| Evidence check | unavailable |
| Title | Undeclared network usage |
Evidence snippet:

```text

```
### HIGH · COMMAND_INJECTION_SHELL_TRUE · scripts/build_optimizer.py:27
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 3ebf34ac26 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | command_injection |
| Analyzer | static |
| Evidence check | exact |
| Title | Shell command execution with shell=True enabled |
Evidence snippet:

```text
os.system(command)
```
### HIGH · COMMAND_INJECTION_SHELL_TRUE · scripts/build_optimizer.py:33
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | a4be7ed067 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | command_injection |
| Analyzer | static |
| Evidence check | exact |
| Title | Shell command execution with shell=True enabled |
Evidence snippet:

```text
os.system(config["analysis_command"])
```
### CRITICAL · COMMAND_INJECTION_OS_SYSTEM · scripts/build_optimizer.py:35
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | c6c944cdf1 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | command_injection |
| Analyzer | static |
| Evidence check | exact |
| Title | Shell command execution with string formatting (potential injection) |
Evidence snippet:

```text
os.system(f"echo 'Analyzing {project_name}' && {config.get('custom_analyzer', 'true')}")
```
### HIGH · COMMAND_INJECTION_SHELL_TRUE · scripts/build_optimizer.py:41
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | b4f1e54114 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | command_injection |
| Analyzer | static |
| Evidence check | exact |
| Title | Shell command execution with shell=True enabled |
Evidence snippet:

```text
os.system(cache_script)
```
### HIGH · COMMAND_INJECTION_SHELL_TRUE · scripts/build_optimizer.py:48
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 86fc2719d0 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | command_injection |
| Analyzer | static |
| Evidence check | exact |
| Title | Shell command execution with shell=True enabled |
Evidence snippet:

```text
os.system(cleanup_cmd)
```
### LOW · UNDECLARED_NETWORK_DESTINATION · scripts/build_optimizer.py:53
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 36bc2b2351 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | unauthorized_tool_use |
| Analyzer | static |
| Evidence check | unavailable |
| Title | Script contacts a destination the documentation never mentions |
Evidence snippet:

```text

```
### MEDIUM · DATA_EXFIL_NETWORK_REQUESTS · scripts/build_optimizer.py:55
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 2d16d2fafb |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | data_exfiltration |
| Analyzer | static |
| Evidence check | exact |
| Title | Outbound network request primitives that can transmit data externally |
Evidence snippet:

```text
response = urllib.request.urlopen(url)
```
### HIGH · COMMAND_INJECTION_SHELL_TRUE · scripts/build_optimizer.py:72
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 37cb24ce21 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | command_injection |
| Analyzer | static |
| Evidence check | exact |
| Title | Shell command execution with shell=True enabled |
Evidence snippet:

```text
os.system(before_cmd)
```
### HIGH · COMMAND_INJECTION_SHELL_TRUE · scripts/build_optimizer.py:74
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | a6e7867f31 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | command_injection |
| Analyzer | static |
| Evidence check | exact |
| Title | Shell command execution with shell=True enabled |
Evidence snippet:

```text
os.system(after_cmd)
```
## Other notes

4 metadata-quality / scan-coverage rows: MANIFEST_MISSING_LICENSE (4).
