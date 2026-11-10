# Sample `agent_skills_sample_seed2027_scripts10_supporting_no_scripts10_skill_md_only10`

Created 2026-11-04T00:12:06+00:00 from `data/sample/agent_skills_sample.db` (SHA-256 `683888c923a51952...`).
**Dataset:** official GitSkills sample database (sample-based methodological experiment; NOT representative of the full GitSkills population).

**Method:** stratified simple random sampling without replacement, equal allocation; unit = representative SKILL.md (one per file_sha); per stratum: frame ordered by file_sha, key = random.Random(2027).random(), smallest keys selected. Seed 2027.

**Population:** 29,786 SKILL.md occurrences, 13,000 distinct contents,
13,000 representatives (one per content hash). Eligible after exclusions: 11,298.

## Exclusions

| reason | representatives |
|---|---|
| excluded: listing truncated, script presence unknown | 1670 |
| excluded: program source but no executable script | 22 |
| excluded: folder listing not captured | 10 |

## Strata

| stratum | definition | population N | sample n | sampling fraction | design weight | complete folders in sample |
|---|---|---|---|---|---|---|
| scripts | at least one executable script among the supporting files | 1404 | 10 | 0.0071 | 140.4 | 7 of 10 |
| supporting_no_scripts | supporting files, but no executable script and no program source | 2634 | 10 | 0.0038 | 263.4 | 10 of 10 |
| skill_md_only | complete listing with no file besides SKILL.md | 7260 | 10 | 0.0014 | 726.0 | 10 of 10 |

Strata are assigned by ordered rules: (1) no listing -> excluded; (2) any executable script -> scripts; (3) truncated
listing -> excluded; (4) program source without scripts -> excluded; (5) any supporting file -> supporting_no_scripts;
(6) otherwise -> skill_md_only. Executable scripts: extensions bash, bat, cjs, cmd, cts, exs, fish, js, lua, mjs, mts, php, pl, ps1, psm1, py, r, rb, sh, ts, zsh, or an extensionless file starting with `#!`.

**Weighting.** Equal allocation over strata of very different sizes: within-stratum results can be reported
directly; population-level proportions must weight each skill by `design_weight`.

**Overlap with earlier pilots / keyword selections:** 0 skill(s).

## Selected skills

| # | stratum | repository | path | files listed | scripts | folder complete |
|---|---|---|---|---|---|---|
| 1 | scripts | NimaChu/free-imagegen | SKILL.md | 13 | 2 | False |
| 2 | scripts | niekbeckers/skills | skills/skill-creator/SKILL.md | 14 | 7 | True |
| 3 | scripts | tkstang/open-agent-toolkit | .agents/skills/oat-brainstorm/SKILL.md | 9 | 4 | False |
| 4 | scripts | doghelWang/amr_studio_v4 | skills/json-visual-diff/json-visual-diff/SKILL.md | 1 | 1 | True |
| 5 | scripts | at-src/cold-box | cold-box-room/skills/library/cb-user-behavior-analytics/SKILL.md | 1 | 1 | True |
| 6 | scripts | LauchnerMedia/nexus-bdr | SKILL.md | 176 | 48 | False |
| 7 | scripts | Will-Barnard-WB/Personal-Knowledge-Bot | .claude/skills/set-reminder/SKILL.md | 1 | 1 | True |
| 8 | scripts | theheavenlyd3mon/hermes-profiles | profiles/educate/skills/media/youtube-content/SKILL.md | 16 | 4 | True |
| 9 | scripts | rappdw/synthdata | skills/synthdata-compute/SKILL.md | 1 | 1 | True |
| 10 | scripts | mdbabumiamssm/AI-Agentic-Skills-by-Dr.-Mia | Skills/Genomics/Spatial_Transcriptomics/bioSkills/spatial-domains/SKILL.md | 2 | 1 | True |
| 11 | supporting_no_scripts | harivansh-afk/rpi | .claude/skills/create-research-questions/SKILL.md | 2 | 0 | True |
| 12 | supporting_no_scripts | comandante4e/claude-skills | skills/spdd/SKILL.md | 2 | 0 | True |
| 13 | supporting_no_scripts | richard-devbot/SDLC-rstack | skills/bounty-hunting/SKILL.md | 1 | 0 | True |
| 14 | supporting_no_scripts | Burakaz/admkrs-creative-suite | skills/admkrs-cs-performance-reporting/SKILL.md | 2 | 0 | True |
| 15 | supporting_no_scripts | munlucky/moonshot-relay | skills/moonshot-teams-runner/SKILL.md | 1 | 0 | True |
| 16 | supporting_no_scripts | FurtherBank/cpu-ai | skills/f-hypothesis-ledger/SKILL.md | 2 | 0 | True |
| 17 | supporting_no_scripts | ssrjkk/claude-skills | .claude/skills/devops/lxc-setup/SKILL.md | 1 | 0 | True |
| 18 | supporting_no_scripts | joleques/northstar-ai | .codex/skills/product-interviewer/SKILL.md | 1 | 0 | True |
| 19 | supporting_no_scripts | hiyenwong/ai_collection | collection/skills/nlp-llm/llama-cpp/SKILL.md | 3 | 0 | True |
| 20 | supporting_no_scripts | alec-c4/agent_dev_kit | skills/stacks/python/SKILL.md | 2 | 0 | True |
| 21 | skill_md_only | openclaw-commons/openclaw-skill-commons | skills/virtualenv-setup/SKILL.md | 0 | 0 | True |
| 22 | skill_md_only | jbro/pi-agent | skills/superpowers/brainstorming/SKILL.md | 0 | 0 | True |
| 23 | skill_md_only | nahisaho/satori | src/.github/skills/scientific-reactome-pathways/SKILL.md | 0 | 0 | True |
| 24 | skill_md_only | abdtirtayasa24/myworkflows-skills | engineering/skills/documentation-and-adrs/SKILL.md | 0 | 0 | True |
| 25 | skill_md_only | MikeCheng1208/BattleTree | .agents/skills/fastapi-workflow/SKILL.md | 0 | 0 | True |
| 26 | skill_md_only | MikeCheng1208/BattleTree | .agents/skills/notion-content/SKILL.md | 0 | 0 | True |
| 27 | skill_md_only | MikeCheng1208/BattleTree | .agents/skills/summarize_text_with_key_details/SKILL.md | 0 | 0 | True |
| 28 | skill_md_only | HaykTarkhanyan/python_math_ml_course | .claude/skills/slide-style/SKILL.md | 0 | 0 | True |
| 29 | skill_md_only | Pranav-Conova/code-review-workflow-for-local-gitea | .claude/skills/review-pr/SKILL.md | 0 | 0 | True |
| 30 | skill_md_only | everruns/everruns | .agents/skills/ship/SKILL.md | 0 | 0 | True |
