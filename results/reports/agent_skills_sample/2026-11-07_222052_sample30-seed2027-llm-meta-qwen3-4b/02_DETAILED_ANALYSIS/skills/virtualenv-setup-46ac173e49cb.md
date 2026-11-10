# Skill `virtualenv-setup-46ac173e49cb`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | openclaw-commons/openclaw-skill-commons |
| SKILL.md path | skills/virtualenv-setup/SKILL.md |
| Sample stratum | skill_md_only |
| Folder complete in GitSkills | True |
| Coverage | no_complete_scan: Cisco ran, but no configuration produced a COMPLETE scan |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | PARTIAL | 1 | INFO | Cisco reported an analyzer failure (skill_loader: SkillLoadError:MISSING_REQUIRED_MANIFEST_FIELD) |
| SKILL.md only \| behavioral | PARTIAL | 1 | INFO | Cisco reported an analyzer failure (skill_loader: SkillLoadError:MISSING_REQUIRED_MANIFEST_FIELD) |
| Full folder \| default | PARTIAL | 1 | INFO | Cisco reported an analyzer failure (skill_loader: SkillLoadError:MISSING_REQUIRED_MANIFEST_FIELD) |
| Full folder \| behavioral | PARTIAL | 1 | INFO | Cisco reported an analyzer failure (skill_loader: SkillLoadError:MISSING_REQUIRED_MANIFEST_FIELD) |
| SKILL.md only \| behavioral+llm | PARTIAL | 2 | LOW | Cisco reported an analyzer failure (skill_loader: SkillLoadError:MISSING_REQUIRED_MANIFEST_FIELD) |
| SKILL.md only \| behavioral+meta | PARTIAL | 1 | INFO | Cisco reported an analyzer failure (skill_loader: SkillLoadError:MISSING_REQUIRED_MANIFEST_FIELD); Meta-Analyzer did not complete: Meta-analysis failed: SKILL.md missing required field: name |
| SKILL.md only \| behavioral+llm+meta | PARTIAL | 2 | LOW | Cisco reported an analyzer failure (skill_loader: SkillLoadError:MISSING_REQUIRED_MANIFEST_FIELD); Meta-Analyzer did not complete: Meta-analysis failed: SKILL.md missing required field: name |
| Full folder \| behavioral+llm | PARTIAL | 2 | LOW | Cisco reported an analyzer failure (skill_loader: SkillLoadError:MISSING_REQUIRED_MANIFEST_FIELD) |
| Full folder \| behavioral+meta | PARTIAL | 1 | INFO | Cisco reported an analyzer failure (skill_loader: SkillLoadError:MISSING_REQUIRED_MANIFEST_FIELD); Meta-Analyzer did not complete: Meta-analysis failed: SKILL.md missing required field: name |
| Full folder \| behavioral+llm+meta | PARTIAL | 2 | LOW | Cisco reported an analyzer failure (skill_loader: SkillLoadError:MISSING_REQUIRED_MANIFEST_FIELD); Meta-Analyzer did not complete: Meta-analysis failed: SKILL.md missing required field: name |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### LOW · LLM_PROMPT_INJECTION · SKILL.md:
|  | value |
|---|---|
| Validation | Scanner alert, not in the review queue |
| Review ID |  |
| Provisional label |  |
| Final (human) label |  |
| Configurations | SKILL.md only \| behavioral+llm; SKILL.md only \| behavioral+llm+meta; Full folder \| behavioral+llm; Full folder \| behavioral+llm+meta |
| Scan outcomes | partial |
| Cisco category | prompt_injection |
| Analyzer | llm |
| Evidence check | unavailable |
| Title | Potential prompt injection via command-line flags |
Evidence snippet:

```text
YAML Manifest Details [evidence_id=SRC:bd43a7da36c1cfe1] and Instruction Body (SKILL.md markdown) [evidence_id=SRC:0e95f5a3666031d6]
```
## Other notes

10 metadata-quality / scan-coverage rows: SKILL_LOAD_FALLBACK_USED (10).
