# Skill `opus-video-13ec794b5de7`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | Birdywen/genspark-agent |
| SKILL.md path | skills/opus-video/SKILL.md |
| Sample stratum | supporting_no_scripts |
| Folder complete in GitSkills | False |
| Coverage | complete: every planned configuration produced a COMPLETE scan |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 1 | INFO | exit code 0 |
| SKILL.md only \| behavioral | COMPLETE | 9 | HIGH | exit code 0 |
| Full folder \| default | COMPLETE | 1 | INFO | exit code 0 |
| Full folder \| behavioral | COMPLETE | 20 | HIGH | exit code 0 |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### HIGH · BEHAVIOR_BASH_TAINT_FLOW · SKILL.md:348
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | a02fd58cfd |
| Provisional label |  |
| Final (human) label |  |
| Configurations | SKILL.md only \| behavioral; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | data_exfiltration |
| Analyzer | behavioral |
| Evidence check | ambiguous |
| Title | Bash: network input flows to execution |
Evidence snippet:

```text
T=$(echo $RESP | python3 -c "import sys,json;d=json.load(sys.stdin);print(d[\"data\"][\"token\"])")
```
### HIGH · BEHAVIOR_BASH_TAINT_FLOW · SKILL.md:349
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | eb51ad917e |
| Provisional label |  |
| Final (human) label |  |
| Configurations | SKILL.md only \| behavioral; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | data_exfiltration |
| Analyzer | behavioral |
| Evidence check | ambiguous |
| Title | Bash: network input flows to execution |
Evidence snippet:

```text
O=$(echo $RESP | python3 -c "import sys,json;d=json.load(sys.stdin);print(d[\"data\"][\"orgId\"])")
```
### MEDIUM · BEHAVIOR_BASH_TAINT_FLOW · SKILL.md:352
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 71449a7ae9 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | SKILL.md only \| behavioral; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | data_exfiltration |
| Analyzer | behavioral |
| Evidence check | mismatch |
| Title | Bash: network input flows to execution |
Evidence snippet:

```text
curl -s -X POST https://api.opus.pro/api/generative-jobs -H "Authorization: Bearer $T" -H "X-OPUS-ORG-ID: $O" -H "X-OPUS-USER-ID: $O" -H "Content-Type: application/json" -H "Origin: https://clip.opus.pro" -d "{\"jobType\":\"youtube-title\",\"text\":\"$TEXT\"}"
```
### MEDIUM · BEHAVIOR_BASH_TAINT_FLOW · SKILL.md:355
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | d98141ece9 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | SKILL.md only \| behavioral; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | data_exfiltration |
| Analyzer | behavioral |
| Evidence check | mismatch |
| Title | Bash: network input flows to execution |
Evidence snippet:

```text
curl -s -X POST https://api.opus.pro/api/generative-jobs -H "Authorization: Bearer $T" -H "X-OPUS-ORG-ID: $O" -H "X-OPUS-USER-ID: $O" -H "Content-Type: application/json" -H "Origin: https://clip.opus.pro" -d "{\"jobType\":\"youtube-description\",\"text\":\"$TEXT\"}"
```
### MEDIUM · BEHAVIOR_BASH_TAINT_FLOW · SKILL.md:358
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 8c93edd551 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | SKILL.md only \| behavioral; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | data_exfiltration |
| Analyzer | behavioral |
| Evidence check | mismatch |
| Title | Bash: network input flows to execution |
Evidence snippet:

```text
curl -s -X POST https://api.opus.pro/api/generative-jobs -H "Authorization: Bearer $T" -H "X-OPUS-ORG-ID: $O" -H "X-OPUS-USER-ID: $O" -H "Content-Type: application/json" -H "Origin: https://clip.opus.pro" -d "{\"jobType\":\"youtube-hashtag\",\"description\":\"$TEXT\"}"
```
### HIGH · BEHAVIOR_BASH_TAINT_FLOW · SKILL.md:366
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | a02fd58cfd |
| Provisional label |  |
| Final (human) label |  |
| Configurations | SKILL.md only \| behavioral; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | data_exfiltration |
| Analyzer | behavioral |
| Evidence check | ambiguous |
| Title | Bash: network input flows to execution |
Evidence snippet:

```text
T=$(echo $RESP | python3 -c "import sys,json;d=json.load(sys.stdin);print(d[\"data\"][\"token\"])")
```
### HIGH · BEHAVIOR_BASH_TAINT_FLOW · SKILL.md:367
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | eb51ad917e |
| Provisional label |  |
| Final (human) label |  |
| Configurations | SKILL.md only \| behavioral; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | data_exfiltration |
| Analyzer | behavioral |
| Evidence check | ambiguous |
| Title | Bash: network input flows to execution |
Evidence snippet:

```text
O=$(echo $RESP | python3 -c "import sys,json;d=json.load(sys.stdin);print(d[\"data\"][\"orgId\"])")
```
### MEDIUM · BEHAVIOR_BASH_TAINT_FLOW · SKILL.md:368
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 3b225e16c8 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | SKILL.md only \| behavioral; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | data_exfiltration |
| Analyzer | behavioral |
| Evidence check | mismatch |
| Title | Bash: network input flows to execution |
Evidence snippet:

```text
curl -s "https://api.opus.pro/api/generative-jobs/JOB_ID" -H "Authorization: Bearer $T" -H "X-OPUS-ORG-ID: $O" -H "X-OPUS-USER-ID: $O" -H "Origin: https://clip.opus.pro"
```
### MEDIUM · BEHAVIOR_BASH_TAINT_FLOW · CAPTIONS_API.md:302
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 36400b8e65 |
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
STATUS=$(curl -s "https://api.opus.pro/api/clip-projects/$PROJECT_ID" \
```
### MEDIUM · BEHAVIOR_BASH_TAINT_FLOW · CAPTIONS_API.md:304
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | c937919ab8 |
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
STAGE=$(echo $STATUS | python3 -c "import sys,json; print(json.load(sys.stdin)['stage'])")
```
### MEDIUM · BEHAVIOR_BASH_TAINT_FLOW · CAPTIONS_API.md:316
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 5876962c62 |
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
SRT_URL=$(echo $STATUS | python3 -c "import sys,json; print(json.load(sys.stdin)['transcriptSrtUrl'])")
```
### MEDIUM · BEHAVIOR_BASH_TAINT_FLOW · CAPTIONS_API.md:317
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 19ab24849a |
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
TXT_URL=$(echo $STATUS | python3 -c "import sys,json; print(json.load(sys.stdin)['transcriptTxtUrl'])")
```
### MEDIUM · BEHAVIOR_BASH_TAINT_FLOW · CAPTIONS_API.md:678
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 0ee3bbcc51 |
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
STATUS=$(echo $RESULT | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['status'])")
```
### MEDIUM · BEHAVIOR_BASH_TAINT_FLOW · CAPTIONS_API.md:690
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 2bf0ae3e0f |
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
STAGE=$(echo $RESULT | python3 -c "import sys,json; print(json.load(sys.stdin)['stage'])")
```
### MEDIUM · BEHAVIOR_BASH_TAINT_FLOW · CAPTIONS_API.md:707
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 337877e86d |
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
SCRIPT=$(echo $SCRIPT_RESULT | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['result']['scriptContent'])")
```
### MEDIUM · BEHAVIOR_BASH_TAINT_FLOW · CAPTIONS_API.md:721
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 4c522e58b3 |
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
DURATION=$(echo $SOURCE | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['durationMs'])")
```
### MEDIUM · BEHAVIOR_BASH_TAINT_FLOW · CAPTIONS_API.md:722
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 367a951165 |
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
TITLE=$(echo $SOURCE | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['title'])")
```
### MEDIUM · BEHAVIOR_BASH_TAINT_FLOW · CAPTIONS_API.md:738
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | be60f3311f |
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
SRT_URL=$(echo $CAPTION_RESULT | python3 -c "import sys,json; print(json.load(sys.stdin)['transcriptSrtUrl'])")
```
### MEDIUM · BEHAVIOR_BASH_TAINT_FLOW · CAPTIONS_API.md:744
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 8512cfce3e |
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
THUMB_URLS=$(echo $THUMB_RESULT | python3 -c "import sys,json; urls=json.load(sys.stdin)['data']['result']['generatedThumbnailUris']; [print(u) for u in urls]")
```
## Other notes

4 metadata-quality / scan-coverage rows: MANIFEST_MISSING_LICENSE (4).
