# Skill `listenhub-7b57a00218af`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | LeoYeAI/openclaw-master-skills |
| SKILL.md path | skills/listenhub/SKILL.md |
| Sample stratum | scripts |
| Folder complete in GitSkills | True |
| Coverage | complete: every planned configuration produced a COMPLETE scan |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 1 | INFO | exit code 0 |
| SKILL.md only \| behavioral | COMPLETE | 1 | INFO | exit code 0 |
| Full folder \| default | COMPLETE | 12 | MEDIUM | exit code 0 |
| Full folder \| behavioral | COMPLETE | 13 | MEDIUM | exit code 0 |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### LOW · UNDECLARED_NETWORK_DESTINATION · scripts/generate-image.sh:55
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 3dc5e26c5c |
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
### LOW · UNDECLARED_NETWORK_DESTINATION · scripts/generate-image.sh:273
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 38cadc11a1 |
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
### MEDIUM · TOOL_ABUSE_SYSTEM_PACKAGE_INSTALL · scripts/generate-image.sh:281
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 609ea0c82a |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | unauthorized_tool_use |
| Analyzer | static |
| Evidence check | exact |
| Title | Attempting to install system packages with elevated privileges |
Evidence snippet:

```text
install_cmd="sudo apt-get update && sudo apt-get install -y ${missing_deps[*]}"
```
### MEDIUM · TOOL_ABUSE_SYSTEM_PACKAGE_INSTALL · scripts/generate-image.sh:283
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 451bb0f2e3 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | unauthorized_tool_use |
| Analyzer | static |
| Evidence check | exact |
| Title | Attempting to install system packages with elevated privileges |
Evidence snippet:

```text
install_cmd="sudo yum install -y ${missing_deps[*]}"
```
### MEDIUM · TOOL_ABUSE_SYSTEM_PACKAGE_INSTALL · scripts/generate-image.sh:285
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 9b886577f1 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | unauthorized_tool_use |
| Analyzer | static |
| Evidence check | exact |
| Title | Attempting to install system packages with elevated privileges |
Evidence snippet:

```text
install_cmd="sudo dnf install -y ${missing_deps[*]}"
```
### MEDIUM · TOOL_ABUSE_SYSTEM_PACKAGE_INSTALL · scripts/generate-image.sh:287
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 843db1c1fe |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | unauthorized_tool_use |
| Analyzer | static |
| Evidence check | exact |
| Title | Attempting to install system packages with elevated privileges |
Evidence snippet:

```text
install_cmd="sudo pacman -S --noconfirm ${missing_deps[*]}"
```
### LOW · UNDECLARED_NETWORK_DESTINATION · scripts/generate-image.sh:302
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | b3385d104f |
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
### LOW · UNDECLARED_NETWORK_DESTINATION · scripts/generate-image.sh:303
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 9b280c9f90 |
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
### LOW · UNDECLARED_NETWORK_DESTINATION · scripts/generate-image.sh:304
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | d6f37ea0f3 |
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
### LOW · UNDECLARED_NETWORK_DESTINATION · scripts/generate-image.sh:574
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 39a6665939 |
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
### LOW · UNDECLARED_NETWORK_DESTINATION · scripts/generate-image.sh:622
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 7da40e1e09 |
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
### MEDIUM · BEHAVIOR_BASH_TAINT_FLOW · scripts/generate-image.sh:445
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 5f2321340d |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | data_exfiltration |
| Analyzer | behavioral |
| Evidence check | exact |
| Title | Bash: tainted data flows to dangerous sink |
Evidence snippet:

```text
ext=$(echo "$ext" | tr '[:upper:]' '[:lower:]')  # Convert to lowercase (bash 3.2 compatible)
```
## Other notes

4 metadata-quality / scan-coverage rows: MANIFEST_MISSING_LICENSE (4).
