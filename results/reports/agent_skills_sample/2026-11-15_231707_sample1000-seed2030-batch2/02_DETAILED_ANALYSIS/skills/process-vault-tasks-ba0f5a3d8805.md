# Skill `process-vault-tasks-ba0f5a3d8805`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | saadahmedacademy/Personal-AI-Employee-Hackathon-0 |
| SKILL.md path | .claude/skills/process-vault-tasks/SKILL.md |
| Sample stratum | scripts |
| Folder complete in GitSkills | True |
| Coverage | no_complete_scan: Cisco ran, but no configuration produced a COMPLETE scan |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | PARTIAL | 1 | INFO | Cisco reported an analyzer failure (skill_loader: SkillLoadError:MISSING_REQUIRED_MANIFEST_FIELD) |
| SKILL.md only \| behavioral | PARTIAL | 1 | INFO | Cisco reported an analyzer failure (skill_loader: SkillLoadError:MISSING_REQUIRED_MANIFEST_FIELD) |
| Full folder \| default | PARTIAL | 2 | CRITICAL | Cisco reported an analyzer failure (skill_loader: SkillLoadError:MISSING_REQUIRED_MANIFEST_FIELD) |
| Full folder \| behavioral | PARTIAL | 2 | CRITICAL | Cisco reported an analyzer failure (skill_loader: SkillLoadError:MISSING_REQUIRED_MANIFEST_FIELD) |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### CRITICAL · COMPOUND_FIND_EXEC · process_tasks.sh:31
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 5acff34a68 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | partial |
| Cisco category | command_injection |
| Analyzer | pipeline |
| Evidence check | mismatch |
| Title | Discovery and execution chain (find -exec) |
Evidence snippet:

```text
#!/bin/bash
# Process tasks from AI Employee vault
# This is invoked by Claude Code as an Agent Skill

VAULT_PATH="${AI_EMPLOYEE_VAULT:-$HOME/hk3-project/AI_Employee_Vault}"

echo "🤖 AI Employee - Processing Tasks"
echo "=================================="
echo "Vault: $VAULT_PATH"
echo ""

# Check 
```
## Other notes

4 metadata-quality / scan-coverage rows: SKILL_LOAD_FALLBACK_USED (4).
