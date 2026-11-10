# Skill `youtube-content-7162d1c45997`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | theheavenlyd3mon/hermes-profiles |
| SKILL.md path | profiles/educate/skills/media/youtube-content/SKILL.md |
| Sample stratum | scripts |
| Folder complete in GitSkills | True |
| Coverage | partially_complete: some configurations are COMPLETE, others are partial, contract-only or failed |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 2 | HIGH | exit code 0 |
| SKILL.md only \| behavioral | COMPLETE | 3 | HIGH | exit code 0 |
| Full folder \| default | COMPLETE | 2 | HIGH | exit code 0 |
| Full folder \| behavioral | COMPLETE | 4 | HIGH | exit code 0 |
| SKILL.md only \| behavioral+llm | COMPLETE | 6 | HIGH | exit code 0 |
| SKILL.md only \| behavioral+meta | PARTIAL | 3 | HIGH | Meta-Analyzer degraded: \[{'code': 'META_BATCH_PARSE_FAILED', 'message': 'Meta-analysis response was malformed (Ollama Meta did not classify every expected index exactly once); this batch was retained unchanged.', 'first_index': 0, 'last_index': 2, 'finding_count': 3, 'failure_diagnostic': {'outer_error_code': 'META_BATCH_PARSE_FAILED', 'inner_error_code': 'META_CONTRACT_RESPONSE', 'request_sha256': 'a3908d0dbea8e6019deef48183337fa732dd6a97d1fcfa4ffa30e6f9454dc82e', 'response_sha256': 'cd8f66985d6e767f3d5a8481b9613529e1afd91a44824364ba57ceb5aef8c7b7', 'repair_attempted': 1, 'repair_succeeded': 0, 'repair_request_sha256': 'be58a99cdb7a947ef05a3488182a80123e370aa3963a7e1a9c51eb925af0a33a', 'repair_response_sha256': '64f197a72fb54de83bb241c08741cab848e1fae18776076098c510aa97ef9519', 'repair_error_code': 'META_CONTRACT_RESPONSE'}}\] |
| SKILL.md only \| behavioral+llm+meta | COMPLETE | 7 | HIGH | exit code 0 |
| Full folder \| behavioral+llm | PARTIAL | 6 | HIGH | Cisco reported an analyzer failure (llm_analyzer: litellm.Timeout: OllamaException - litellm.Timeout: Connection timed out. Timeout passed=120.0, time taken=120.006 seconds); the LLM analyzer could not review the skill (LLM_ANALYSIS_FAILED) |
| Full folder \| behavioral+meta | COMPLETE | 5 | CRITICAL | exit code 0 |
| Full folder \| behavioral+llm+meta | PARTIAL | 6 | HIGH | Cisco reported an analyzer failure (llm_analyzer: litellm.Timeout: OllamaException - litellm.Timeout: Connection timed out. Timeout passed=120.0, time taken=120.008 seconds); the LLM analyzer could not review the skill (LLM_ANALYSIS_FAILED); Meta-Analyzer degraded: \[{'code': 'META_BATCH_PARSE_FAILED', 'message': 'Meta-analysis response was malformed (Ollama Meta did not classify every expected index exactly once); this batch was retained unchanged.', 'first_index': 0, 'last_index': 5, 'finding_count': 6, 'failure_diagnostic': {'outer_error_code': 'META_BATCH_PARSE_FAILED', 'inner_error_code': 'META_CONTRACT_RESPONSE', 'request_sha256': '35197c0b8a581dc2599184663ee8f3eba29cfe00e1b9b74f9feb8ceab55e6b10', 'response_sha256': 'c7b10504221496477cc48247f87613bf5301c598a90b9a1ceb5383d3ffd5759f', 'repair_attempted': 1, 'repair_succeeded': 0, 'repair_request_sha256': 'ad929a574cbf187cc1848e1bb4d42f2781962dcf05420b8d6473613e401843c3', 'repair_response_sha256': '5ff7db48ee814adfe04583ebcb9408607631b00287dc974bc686cdf0e9a5b29f', 'repair_error_code': 'META_CONTRACT_RESPONSE'}}\] |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### HIGH · ACTIVE_DYNAMIC_EXECUTION · SKILL.md:169
|  | value |
|---|---|
| Validation | Scanner alert, not in the review queue |
| Review ID |  |
| Provisional label |  |
| Final (human) label |  |
| Configurations | SKILL.md only \| default; SKILL.md only \| behavioral; Full folder \| default; Full folder \| behavioral; SKILL.md only \| behavioral+llm; SKILL.md only \| behavioral+meta; SKILL.md only \| behavioral+llm+meta; Full folder \| behavioral+llm; Full folder \| behavioral+meta; Full folder \| behavioral+llm+meta |
| Scan outcomes | complete; partial |
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
| Validation | Scanner alert, not in the review queue |
| Review ID |  |
| Provisional label |  |
| Final (human) label |  |
| Configurations | SKILL.md only \| behavioral; Full folder \| behavioral; SKILL.md only \| behavioral+llm; SKILL.md only \| behavioral+meta; SKILL.md only \| behavioral+llm+meta; Full folder \| behavioral+llm; Full folder \| behavioral+meta; Full folder \| behavioral+llm+meta |
| Scan outcomes | complete; partial |
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
| Validation | Scanner alert, not in the review queue |
| Review ID |  |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| behavioral; Full folder \| behavioral+llm; Full folder \| behavioral+meta; Full folder \| behavioral+llm+meta |
| Scan outcomes | complete; partial |
| Cisco category | command_injection |
| Analyzer | behavioral |
| Evidence check | mismatch |
| Title | Python code block executes shell commands |
Evidence snippet:

```text
r = subprocess.run(['curl', '-s', '-L', '--max-time', '30',
```
### HIGH · LLM_COMMAND_INJECTION · SKILL.md:
|  | value |
|---|---|
| Validation | Scanner alert, not in the review queue |
| Review ID |  |
| Provisional label |  |
| Final (human) label |  |
| Configurations | SKILL.md only \| behavioral+llm; SKILL.md only \| behavioral+llm+meta |
| Scan outcomes | complete |
| Cisco category | command_injection |
| Analyzer | llm |
| Evidence check | unavailable |
| Title | Direct command injection via subprocess.run in batch extraction |
Evidence snippet:

```text
The skill's batch extraction pipeline uses `subprocess.run` to run yt-dlp with `--dump-single-json` on user-provided URLs, creating a potential command injection vector if the URL input is untrusted.
```
### MEDIUM · META_DETECTED_UNAUTHORIZED_TOOL_USE · :
|  | value |
|---|---|
| Validation | Scanner alert, not in the review queue |
| Review ID |  |
| Provisional label |  |
| Final (human) label |  |
| Configurations | SKILL.md only \| behavioral+llm+meta |
| Scan outcomes | complete |
| Cisco category | unauthorized_tool_use |
| Analyzer | meta |
| Evidence check | unavailable |
| Title | Cron job rate limiting bypass |
Evidence snippet:

```text

```
### CRITICAL · META_DETECTED_PROMPT_INJECTION · :
|  | value |
|---|---|
| Validation | Scanner alert, not in the review queue |
| Review ID |  |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| behavioral+meta |
| Scan outcomes | complete |
| Cisco category | prompt_injection |
| Analyzer | meta |
| Evidence check | unavailable |
| Title | Command injection via subprocess.run |
Evidence snippet:

```text

```
## Other notes

16 metadata-quality / scan-coverage rows: MANIFEST_MISSING_LICENSE (10), LLM_CONTEXT_BUDGET_EXCEEDED (4), LLM_ANALYSIS_FAILED (2).
