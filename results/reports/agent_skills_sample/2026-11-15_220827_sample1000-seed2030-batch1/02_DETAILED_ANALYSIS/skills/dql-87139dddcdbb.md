# Skill `dql-87139dddcdbb`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | GuanceCloud/pipeline-go |
| SKILL.md path | skills/dql/SKILL.md |
| Sample stratum | scripts |
| Folder complete in GitSkills | False |
| Coverage | complete: every planned configuration produced a COMPLETE scan |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 1 | INFO | exit code 0 |
| SKILL.md only \| behavioral | COMPLETE | 1 | INFO | exit code 0 |
| Full folder \| default | COMPLETE | 3 | HIGH | exit code 0 |
| Full folder \| behavioral | COMPLETE | 3 | HIGH | exit code 0 |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### LOW · UNDECLARED_NETWORK_DESTINATION · bin/dqlcheck:6
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | b3e044ee2a |
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
### HIGH · COMPOUND_EXTRACT_EXECUTE · bin/dqlcheck:108
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | ea61455813 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | supply_chain_attack |
| Analyzer | pipeline |
| Evidence check | mismatch |
| Title | Archive extraction followed by execution |
Evidence snippet:

```text
#!/usr/bin/env sh
set -eu

BASE_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
CACHE_ROOT="${DQLCHECK_CACHE_DIR:-$BASE_DIR/.cache}"
REMOTE_ROOT="${DQLCHECK_BASE_URL:-https://static.guance.com/guancedb}"
REMOTE_VERSION_URL="${DQLCHECK_VERSION_URL:-$REMOTE_ROOT/version}"

log() {
  printf '%s\n' "
```
## Other notes

4 metadata-quality / scan-coverage rows: MANIFEST_MISSING_LICENSE (4).
