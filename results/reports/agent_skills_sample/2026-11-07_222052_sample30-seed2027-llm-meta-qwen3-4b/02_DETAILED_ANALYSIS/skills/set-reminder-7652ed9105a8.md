# Skill `set-reminder-7652ed9105a8`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | Will-Barnard-WB/Personal-Knowledge-Bot |
| SKILL.md path | .claude/skills/set-reminder/SKILL.md |
| Sample stratum | scripts |
| Folder complete in GitSkills | True |
| Coverage | partially_complete: some configurations are COMPLETE, others are partial, contract-only or failed |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 1 | INFO | exit code 0 |
| SKILL.md only \| behavioral | COMPLETE | 1 | INFO | exit code 0 |
| Full folder \| default | COMPLETE | 6 | HIGH | exit code 0 |
| Full folder \| behavioral | COMPLETE | 6 | HIGH | exit code 0 |
| SKILL.md only \| behavioral+llm | COMPLETE | 2 | LOW | exit code 0 |
| SKILL.md only \| behavioral+meta | COMPLETE | 1 | INFO | exit code 0 |
| SKILL.md only \| behavioral+llm+meta | PARTIAL | 2 | LOW | Meta-Analyzer degraded: \[{'code': 'META_BATCH_PARSE_FAILED', 'message': 'Meta-analysis response was malformed (NONE_SUPPORTED conflicts with a substantive Meta delta); this batch was retained unchanged.', 'first_index': 0, 'last_index': 1, 'finding_count': 2, 'failure_diagnostic': {'outer_error_code': 'META_BATCH_PARSE_FAILED', 'inner_error_code': 'META_CONTRACT_DELTA_CONSISTENCY', 'request_sha256': '9ffc7605ff96d7ec7ca96dc690f6b3694aaa980f586aad686826fc64382ff492', 'response_sha256': '107ffb6ea401d4c852a44ea691ff297e1c0fd1d61010cbcca7593d4fdbd1087c', 'repair_attempted': 1, 'repair_succeeded': 0, 'repair_request_sha256': '228821f0d2a0bc95979efb931b6622f197bb5bf273b05c8f12fae46ce4fd2e0b', 'repair_response_sha256': 'b0302f60bdb2ac39a0f80ca6b2ace0ee063913ef31ed436a824a5164cb7fe641', 'repair_error_code': 'META_CONTRACT_RESPONSE'}}\] |
| Full folder \| behavioral+llm | COMPLETE | 9 | HIGH | exit code 0 |
| Full folder \| behavioral+meta | PARTIAL | 6 | HIGH | Meta-Analyzer degraded: \[{'code': 'META_BATCH_PARSE_FAILED', 'message': 'Meta-analysis response was malformed (Ollama Meta did not classify every expected index exactly once); this batch was retained unchanged.', 'first_index': 0, 'last_index': 5, 'finding_count': 6, 'failure_diagnostic': {'outer_error_code': 'META_BATCH_PARSE_FAILED', 'inner_error_code': 'META_CONTRACT_RESPONSE', 'request_sha256': '137e5182646a7c82407ce0564daa9c875dfe64da979516e15548a9f3d1c66da6', 'response_sha256': '3db0431250235f176a5d7c4502774b47870a7f3b4329455975ca5b2d60983553', 'repair_attempted': 1, 'repair_succeeded': 0, 'repair_request_sha256': '1d44adc017c55c81ecb5460e0b55e3f1dd22cff1bb6b4ad10f895b8ab8149649', 'repair_response_sha256': '7bb4e6a943dfb78033643dc271ca80b1f40d368cdd0ecbcfe36d8c6920cd819d', 'repair_error_code': 'META_CONTRACT_RESPONSE'}}\] |
| Full folder \| behavioral+llm+meta | PARTIAL | 9 | HIGH | Meta-Analyzer degraded: \[{'code': 'META_BATCH_PARSE_FAILED', 'message': 'Meta-analysis response was malformed (Ollama Meta did not classify every expected index exactly once); this batch was retained unchanged.', 'first_index': 0, 'last_index': 8, 'finding_count': 9, 'failure_diagnostic': {'outer_error_code': 'META_BATCH_PARSE_FAILED', 'inner_error_code': 'META_CONTRACT_RESPONSE', 'request_sha256': '902c3e5fc6677955ec94c5c4792318f2ef4e539d5e6b32da2d56730f23081cf8', 'response_sha256': '4076b88ddead9e011ce52982aa3fb28ece9304b063a577c96751ed66efa07d72', 'repair_attempted': 1, 'repair_succeeded': 0, 'repair_request_sha256': '49a44efc271cba08bda63cbbd804ac306c638da9c4fba46b7dc04e256d5e8dc5', 'repair_response_sha256': '203c8d9c00c887c1bc5bec4d466074f548457891ecb35cd5e105829ee3b993d6', 'repair_error_code': 'META_CONTRACT_RESPONSE'}}\] |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### HIGH · ALLOWED_TOOLS_BASH_VIOLATION · SKILL.md:
|  | value |
|---|---|
| Validation | Scanner alert, not in the review queue |
| Review ID |  |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral; Full folder \| behavioral+llm; Full folder \| behavioral+meta; Full folder \| behavioral+llm+meta |
| Scan outcomes | complete; partial |
| Cisco category | unauthorized_tool_use |
| Analyzer | static |
| Evidence check | unavailable |
| Title | Code executes bash but Bash tool not in allowed-tools |
Evidence snippet:

```text

```
### MEDIUM · ALLOWED_TOOLS_NETWORK_USAGE · SKILL.md:
|  | value |
|---|---|
| Validation | Scanner alert, not in the review queue |
| Review ID |  |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral; Full folder \| behavioral+llm; Full folder \| behavioral+meta; Full folder \| behavioral+llm+meta |
| Scan outcomes | complete; partial |
| Cisco category | unauthorized_tool_use |
| Analyzer | static |
| Evidence check | unavailable |
| Title | Code makes network requests |
Evidence snippet:

```text

```
### LOW · ALLOWED_TOOLS_GREP_VIOLATION · SKILL.md:
|  | value |
|---|---|
| Validation | Scanner alert, not in the review queue |
| Review ID |  |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral; Full folder \| behavioral+llm; Full folder \| behavioral+meta; Full folder \| behavioral+llm+meta |
| Scan outcomes | complete; partial |
| Cisco category | unauthorized_tool_use |
| Analyzer | static |
| Evidence check | unavailable |
| Title | Code uses search/grep patterns but Grep tool not in allowed-tools |
Evidence snippet:

```text

```
### MEDIUM · DATA_EXFIL_NETWORK_REQUESTS · scripts/set_reminder.py:38
|  | value |
|---|---|
| Validation | Scanner alert, not in the review queue |
| Review ID |  |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral; Full folder \| behavioral+llm; Full folder \| behavioral+meta; Full folder \| behavioral+llm+meta |
| Scan outcomes | complete; partial |
| Cisco category | data_exfiltration |
| Analyzer | static |
| Evidence check | exact |
| Title | Outbound network request primitives that can transmit data externally |
Evidence snippet:

```text
req  = urllib.request.Request(
```
### MEDIUM · DATA_EXFIL_NETWORK_REQUESTS · scripts/set_reminder.py:41
|  | value |
|---|---|
| Validation | Scanner alert, not in the review queue |
| Review ID |  |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral; Full folder \| behavioral+llm; Full folder \| behavioral+meta; Full folder \| behavioral+llm+meta |
| Scan outcomes | complete; partial |
| Cisco category | data_exfiltration |
| Analyzer | static |
| Evidence check | exact |
| Title | Outbound network request primitives that can transmit data externally |
Evidence snippet:

```text
urllib.request.urlopen(req, timeout=10)
```
### LOW · LLM_PROMPT_INJECTION · SKILL.md:
|  | value |
|---|---|
| Validation | Scanner alert, not in the review queue |
| Review ID |  |
| Provisional label |  |
| Final (human) label |  |
| Configurations | SKILL.md only \| behavioral+llm; SKILL.md only \| behavioral+llm+meta |
| Scan outcomes | complete; partial |
| Cisco category | prompt_injection |
| Analyzer | llm |
| Evidence check | unavailable |
| Title | Potential prompt injection via user input parsing |
Evidence snippet:

```text
The skill's workflow requires parsing user input to extract `reminder_text` and `when` fields, which are then passed to a Python script. This creates a potential attack surface where user input could be misinterpreted as malicious commands.
```
### HIGH · LLM_UNAUTHORIZED_TOOL_USE · scripts/set_reminder.py:
|  | value |
|---|---|
| Validation | Scanner alert, not in the review queue |
| Review ID |  |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| behavioral+llm; Full folder \| behavioral+llm+meta |
| Scan outcomes | complete; partial |
| Cisco category | unauthorized_tool_use |
| Analyzer | llm |
| Evidence check | unavailable |
| Title | Unauthorized tool execution via cron |
Evidence snippet:

```text
The script writes a cron entry without user confirmation and deletes itself after execution, bypassing the manifest's `user-invocable: False` constraint
```
### MEDIUM · LLM_DATA_EXFILTRATION · scripts/set_reminder.py:
|  | value |
|---|---|
| Validation | Scanner alert, not in the review queue |
| Review ID |  |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| behavioral+llm; Full folder \| behavioral+llm+meta |
| Scan outcomes | complete; partial |
| Cisco category | data_exfiltration |
| Analyzer | llm |
| Evidence check | unavailable |
| Title | Telegram gateway URL exposure |
Evidence snippet:

```text
The cron script uses `GATEWAY_URL` from the environment, which is not properly secured and could be exposed to unauthorized users
```
## Other notes

10 metadata-quality / scan-coverage rows: MANIFEST_MISSING_LICENSE (10).
