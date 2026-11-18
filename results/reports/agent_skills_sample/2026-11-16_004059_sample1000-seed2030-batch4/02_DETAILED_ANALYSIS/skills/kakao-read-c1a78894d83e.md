# Skill `kakao-read-c1a78894d83e`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | hivgb1-ai/do-better-workspace-v2 |
| SKILL.md path | .claude/skills/kakao-read/SKILL.md |
| Sample stratum | scripts |
| Folder complete in GitSkills | True |
| Coverage | complete: every planned configuration produced a COMPLETE scan |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 1 | INFO | exit code 0 |
| SKILL.md only \| behavioral | COMPLETE | 1 | INFO | exit code 0 |
| Full folder \| default | COMPLETE | 15 | CRITICAL | exit code 0 |
| Full folder \| behavioral | COMPLETE | 15 | CRITICAL | exit code 0 |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### MEDIUM · ALLOWED_TOOLS_NETWORK_USAGE · SKILL.md:
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 1ec88382f1 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | unauthorized_tool_use |
| Analyzer | static |
| Evidence check | unavailable |
| Title | Code makes network requests |
Evidence snippet:

```text

```
### MEDIUM · ALLOWED_TOOLS_WRITE_VIOLATION · SKILL.md:
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 2200c437da |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | policy_violation |
| Analyzer | static |
| Evidence check | unavailable |
| Title | Skill declares no Write tool but bundled scripts write files |
Evidence snippet:

```text

```
### MEDIUM · TOOL_ABUSE_UNDECLARED_NETWORK · SKILL.md:
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | bd6d6535e2 |
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
### LOW · ALLOWED_TOOLS_GLOB_VIOLATION · SKILL.md:
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 3226998f74 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | unauthorized_tool_use |
| Analyzer | static |
| Evidence check | unavailable |
| Title | Code uses glob/file patterns but Glob tool not in allowed-tools |
Evidence snippet:

```text

```
### LOW · ALLOWED_TOOLS_GREP_VIOLATION · SKILL.md:
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 818d06b492 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | unauthorized_tool_use |
| Analyzer | static |
| Evidence check | unavailable |
| Title | Code uses search/grep patterns but Grep tool not in allowed-tools |
Evidence snippet:

```text

```
### CRITICAL · YARA_sql_injection_generic · scripts/kakao_read.py:434
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | e247f20961 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | command_injection |
| Analyzer | static |
| Evidence check | exact |
| Title | INJECTION ATTACK detected by YARA |
Evidence snippet:

```text
COALESCE(u.displayName, u.nickName, CAST(m.authorId AS TEXT)) AS sender,
```
### CRITICAL · YARA_sql_injection_generic · scripts/kakao_read.py:467
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | c851c90039 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | command_injection |
| Analyzer | static |
| Evidence check | exact |
| Title | INJECTION ATTACK detected by YARA |
Evidence snippet:

```text
COALESCE(u.displayName, u.nickName, CAST(m.authorId AS TEXT)),
```
### MEDIUM · DATA_EXFIL_NETWORK_REQUESTS · scripts/kakao_read.py:495
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 7081f09d50 |
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
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
```
### MEDIUM · DATA_EXFIL_NETWORK_REQUESTS · scripts/kakao_read.py:496
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | b786beae2f |
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
data = urllib.request.urlopen(req, timeout=30).read()
```
### CRITICAL · YARA_sql_injection_generic · scripts/kakao_read.py:510
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | f072355490 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | command_injection |
| Analyzer | static |
| Evidence check | exact |
| Title | INJECTION ATTACK detected by YARA |
Evidence snippet:

```text
COALESCE(u.displayName, u.nickName, CAST(m.authorId AS TEXT)), m.message
```
### CRITICAL · YARA_sql_injection_generic · scripts/kakao_read.py:546
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 25e6e994a7 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | command_injection |
| Analyzer | static |
| Evidence check | exact |
| Title | INJECTION ATTACK detected by YARA |
Evidence snippet:

```text
"COALESCE(u2.displayName, u2.nickName, CAST(m2.authorId AS TEXT)) AS nm "
```
### CRITICAL · YARA_sql_injection_generic · scripts/kakao_read.py:599
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | ae2af8ccbf |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | command_injection |
| Analyzer | static |
| Evidence check | exact |
| Title | INJECTION ATTACK detected by YARA |
Evidence snippet:

```text
COALESCE(u.displayName, u.nickName, CAST(m.authorId AS TEXT)) AS sender,
```
### MEDIUM · DATA_EXFIL_NETWORK_REQUESTS · scripts/win/kakao_win.py:402
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | ded9a783ac |
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
req = urllib.request.Request(PROCDUMP_URL, headers={"User-Agent": "Mozilla/5.0"})
```
### MEDIUM · DATA_EXFIL_NETWORK_REQUESTS · scripts/win/kakao_win.py:403
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 031ff52cd8 |
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
with urllib.request.urlopen(req, timeout=60) as r:
```
## Other notes

4 metadata-quality / scan-coverage rows: MANIFEST_MISSING_LICENSE (4).
