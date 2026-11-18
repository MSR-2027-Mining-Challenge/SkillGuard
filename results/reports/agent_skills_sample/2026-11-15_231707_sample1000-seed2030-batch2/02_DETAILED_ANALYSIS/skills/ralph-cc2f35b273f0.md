# Skill `ralph-cc2f35b273f0`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | jai/greenhouse-raycast-extension |
| SKILL.md path | .claude/skills/ralph/SKILL.md |
| Sample stratum | scripts |
| Folder complete in GitSkills | True |
| Coverage | no_complete_scan: Cisco ran, but no configuration produced a COMPLETE scan |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | PARTIAL | 1 | INFO | Cisco reported an analyzer failure (skill_loader: SkillLoadError:MALFORMED_YAML_FRONTMATTER) |
| SKILL.md only \| behavioral | PARTIAL | 3 | MEDIUM | Cisco reported an analyzer failure (skill_loader: SkillLoadError:MALFORMED_YAML_FRONTMATTER) |
| Full folder \| default | PARTIAL | 1 | INFO | Cisco reported an analyzer failure (skill_loader: SkillLoadError:MALFORMED_YAML_FRONTMATTER) |
| Full folder \| behavioral | PARTIAL | 5 | MEDIUM | Cisco reported an analyzer failure (skill_loader: SkillLoadError:MALFORMED_YAML_FRONTMATTER) |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### MEDIUM · BEHAVIOR_BASH_TAINT_FLOW · SKILL.md:346
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | b8c2d2f475 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | SKILL.md only \| behavioral; Full folder \| behavioral |
| Scan outcomes | partial |
| Cisco category | data_exfiltration |
| Analyzer | behavioral |
| Evidence check | mismatch |
| Title | Bash: tainted data flows to dangerous sink |
Evidence snippet:

```text
git push origin "$CURRENT_BRANCH" 2>/dev/null || \
```
### MEDIUM · BEHAVIOR_BASH_TAINT_FLOW · SKILL.md:347
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | e4f3beae78 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | SKILL.md only \| behavioral; Full folder \| behavioral |
| Scan outcomes | partial |
| Cisco category | data_exfiltration |
| Analyzer | behavioral |
| Evidence check | mismatch |
| Title | Bash: tainted data flows to dangerous sink |
Evidence snippet:

```text
git push -u origin "$CURRENT_BRANCH"
```
### MEDIUM · BEHAVIOR_BASH_TAINT_FLOW · templates/loop.sh:63
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | dbc4a16e94 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| behavioral |
| Scan outcomes | partial |
| Cisco category | data_exfiltration |
| Analyzer | behavioral |
| Evidence check | exact |
| Title | Bash: tainted data flows to dangerous sink |
Evidence snippet:

```text
git push origin "$CURRENT_BRANCH" || {
```
### MEDIUM · BEHAVIOR_BASH_TAINT_FLOW · templates/loop.sh:65
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 2d1f03bcf1 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| behavioral |
| Scan outcomes | partial |
| Cisco category | data_exfiltration |
| Analyzer | behavioral |
| Evidence check | exact |
| Title | Bash: tainted data flows to dangerous sink |
Evidence snippet:

```text
git push -u origin "$CURRENT_BRANCH"
```
## Other notes

4 metadata-quality / scan-coverage rows: SKILL_LOAD_FALLBACK_USED (4).
