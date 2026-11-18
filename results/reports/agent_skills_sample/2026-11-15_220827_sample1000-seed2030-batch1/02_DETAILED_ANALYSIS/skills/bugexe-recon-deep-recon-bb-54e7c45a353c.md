# Skill `bugexe-recon-deep-recon-bb-54e7c45a353c`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | conjure-3301/skills |
| SKILL.md path | bugexe-recon-deep-recon-bb/SKILL.md |
| Sample stratum | skill_md_only |
| Folder complete in GitSkills | True |
| Coverage | complete: every planned configuration produced a COMPLETE scan |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 4 | CRITICAL | exit code 0 |
| SKILL.md only \| behavioral | COMPLETE | 4 | CRITICAL | exit code 0 |
| Full folder \| default | COMPLETE | 4 | CRITICAL | exit code 0 |
| Full folder \| behavioral | COMPLETE | 4 | CRITICAL | exit code 0 |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### CRITICAL · COMPOUND_FETCH_EXECUTE · SKILL.md:16
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 7bbf2514d9 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | SKILL.md only \| default; SKILL.md only \| behavioral; Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | command_injection |
| Analyzer | pipeline |
| Evidence check | mismatch |
| Title | Remote fetch followed by execution |
Evidence snippet:

```text
# subfinder — passive multi-source
subfinder -d $DOMAIN -all -recursive -silent -o subs_subfinder.txt &

# Certificate Transparency (crt.sh)
curl -s "https://crt.sh/?q=%25.$DOMAIN&output=json" | \
  python3 -c "import sys,json;[print(x['name_value']) for x in json.load(sys.stdin)]" | \
  sed 's/\*\.
```
### CRITICAL · COMPOUND_FETCH_EXECUTE · SKILL.md:23
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 7821c5a266 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | SKILL.md only \| default; SKILL.md only \| behavioral; Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | command_injection |
| Analyzer | pipeline |
| Evidence check | mismatch |
| Title | Remote fetch followed by execution |
Evidence snippet:

```text
# subfinder — passive multi-source
subfinder -d $DOMAIN -all -recursive -silent -o subs_subfinder.txt &

# Certificate Transparency (crt.sh)
curl -s "https://crt.sh/?q=%25.$DOMAIN&output=json" | \
  python3 -c "import sys,json;[print(x['name_value']) for x in json.load(sys.stdin)]" | \
  sed 's/\*\.
```
## Other notes

8 metadata-quality / scan-coverage rows: MANIFEST_INVALID_NAME (4), MANIFEST_MISSING_LICENSE (4).
