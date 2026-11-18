# Skill `launchd-cron-installer-04a39183afa5`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | 0xAxiom/axiom-public |
| SKILL.md path | agent-skills/skills/launchd-cron-installer/SKILL.md |
| Sample stratum | scripts |
| Folder complete in GitSkills | True |
| Coverage | no_complete_scan: Cisco ran, but no configuration produced a COMPLETE scan |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | PARTIAL | 3 | HIGH | Cisco reported an analyzer failure (skill_loader: SkillLoadError:MISSING_REQUIRED_MANIFEST_FIELD) |
| SKILL.md only \| behavioral | PARTIAL | 3 | HIGH | Cisco reported an analyzer failure (skill_loader: SkillLoadError:MISSING_REQUIRED_MANIFEST_FIELD) |
| Full folder \| default | PARTIAL | 4 | HIGH | Cisco reported an analyzer failure (skill_loader: SkillLoadError:MISSING_REQUIRED_MANIFEST_FIELD) |
| Full folder \| behavioral | PARTIAL | 4 | HIGH | Cisco reported an analyzer failure (skill_loader: SkillLoadError:MISSING_REQUIRED_MANIFEST_FIELD) |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### HIGH · ACTIVE_OS_PERSISTENCE_DIRECTIVE · SKILL.md:3
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 3cf782af7d |
| Provisional label |  |
| Final (human) label |  |
| Configurations | SKILL.md only \| default; SKILL.md only \| behavioral; Full folder \| default; Full folder \| behavioral |
| Scan outcomes | partial |
| Cisco category | malware |
| Analyzer | static |
| Evidence check | mismatch |
| Title | Active instruction establishes operating-system persistence |
Evidence snippet:

```text
[active operating-system persistence directive]
```
### HIGH · ACTIVE_OS_PERSISTENCE_DIRECTIVE · SKILL.md:69
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | d2aca02fcd |
| Provisional label |  |
| Final (human) label |  |
| Configurations | SKILL.md only \| default; SKILL.md only \| behavioral; Full folder \| default; Full folder \| behavioral |
| Scan outcomes | partial |
| Cisco category | malware |
| Analyzer | static |
| Evidence check | mismatch |
| Title | Active instruction establishes operating-system persistence |
Evidence snippet:

```text
[active operating-system persistence directive]
```
### LOW · UNDECLARED_NETWORK_DESTINATION · scripts/cron-to-plist.js:149
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 8ec02c7998 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | partial |
| Cisco category | unauthorized_tool_use |
| Analyzer | static |
| Evidence check | unavailable |
| Title | Script contacts a destination the documentation never mentions |
Evidence snippet:

```text

```
## Other notes

4 metadata-quality / scan-coverage rows: SKILL_LOAD_FALLBACK_USED (4).
