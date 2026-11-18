# Skill `camoufox-deploy-18b42d5f19d8`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | modbender/skill-library-mcp |
| SKILL.md path | data/camoufox-deploy/SKILL.md |
| Sample stratum | scripts |
| Folder complete in GitSkills | False |
| Coverage | complete: every planned configuration produced a COMPLETE scan |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 5 | HIGH | exit code 0 |
| SKILL.md only \| behavioral | COMPLETE | 5 | HIGH | exit code 0 |
| Full folder \| default | COMPLETE | 10 | CRITICAL | exit code 0 |
| Full folder \| behavioral | COMPLETE | 10 | CRITICAL | exit code 0 |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### HIGH · PIPELINE_TAINT_FLOW · SKILL.md:1
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 434a6035aa |
| Provisional label |  |
| Final (human) label |  |
| Configurations | SKILL.md only \| default; SKILL.md only \| behavioral; Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | data_exfiltration |
| Analyzer | pipeline |
| Evidence check | mismatch |
| Title | Dangerous data flow in command pipeline |
Evidence snippet:

```text
curl -LsSf https://astral.sh/uv/install.sh | sh
```
### HIGH · PIPELINE_TAINT_FLOW · SKILL.md:2
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 99d24c061f |
| Provisional label |  |
| Final (human) label |  |
| Configurations | SKILL.md only \| default; SKILL.md only \| behavioral; Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | data_exfiltration |
| Analyzer | pipeline |
| Evidence check | mismatch |
| Title | Dangerous data flow in command pipeline |
Evidence snippet:

```text
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```
### MEDIUM · CORRELATED_NETWORK_EXECUTION_FLOW · SKILL.md:50
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 30f697e58f |
| Provisional label |  |
| Final (human) label |  |
| Configurations | SKILL.md only \| default; SKILL.md only \| behavioral; Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | command_injection |
| Analyzer | correlation |
| Evidence check | unavailable |
| Title | Network-derived content reaches code execution |
Evidence snippet:

```text

```
### MEDIUM · CORRELATED_NETWORK_EXECUTION_FLOW · SKILL.md:156
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 9c7238486f |
| Provisional label |  |
| Final (human) label |  |
| Configurations | SKILL.md only \| default; SKILL.md only \| behavioral; Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | command_injection |
| Analyzer | correlation |
| Evidence check | unavailable |
| Title | Network-derived content reaches code execution |
Evidence snippet:

```text

```
### HIGH · PIPELINE_TAINT_FLOW · README.md:2
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 5048d9d09f |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | data_exfiltration |
| Analyzer | pipeline |
| Evidence check | mismatch |
| Title | Dangerous data flow in command pipeline |
Evidence snippet:

```text
curl -LsSf https://astral.sh/uv/install.sh | sh
```
### HIGH · PIPELINE_TAINT_FLOW · README.md:3
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 65ca21f331 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | data_exfiltration |
| Analyzer | pipeline |
| Evidence check | mismatch |
| Title | Dangerous data flow in command pipeline |
Evidence snippet:

```text
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```
### MEDIUM · COMPOUND_FETCH_EXECUTE · README.md:20
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 6087fa7c84 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | command_injection |
| Analyzer | pipeline |
| Evidence check | exact |
| Title | Remote fetch followed by execution |
Evidence snippet:

```text
# 安装 uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# 安装 camoufox
uv pip install camoufox --system

# 下载 camoufox 浏览器
python3 -c "from camoufox.sync_api import Camoufox; Camoufox()"

```
### CRITICAL · COMPOUND_FETCH_EXECUTE · scripts/install.sh:66
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 0cbe3a9e8d |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | command_injection |
| Analyzer | pipeline |
| Evidence check | mismatch |
| Title | Remote fetch followed by execution |
Evidence snippet:

```text
#!/bin/bash
#
# Camoufox + Agent-Browser 一键安装脚本
# 
# 这个脚本自动完成：
# 1. 安装 uv
# 2. 用 uv 安装 camoufox
# 3. 下载 camoufox 浏览器二进制
# 4. 安装 agent-browser npm 包
# 5. 修改 agent-browser 源码（自动检测 firefox/camoufox）
# 6. 重新编译 Rust CLI
# 7. 替换系统版本
#

set -e  # 遇到错误立即退出

# 颜色定义
RED='\033[0;31m'
GREEN='\
```
### HIGH · CORRELATED_NETWORK_EXECUTION_FLOW · scripts/install.sh:66
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | d6444144c3 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | command_injection |
| Analyzer | correlation |
| Evidence check | unavailable |
| Title | Network-derived content reaches code execution |
Evidence snippet:

```text

```
## Other notes

4 metadata-quality / scan-coverage rows: MANIFEST_MISSING_LICENSE (4).
