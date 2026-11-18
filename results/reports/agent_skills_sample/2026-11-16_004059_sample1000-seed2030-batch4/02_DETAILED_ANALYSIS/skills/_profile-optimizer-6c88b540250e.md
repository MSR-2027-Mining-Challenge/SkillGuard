# Skill `_profile-optimizer-6c88b540250e`
[Back to START_HERE](../../01_IMPORTANT_RESULTS/START_HERE.md)
|  | value |
|---|---|
| Repository | turagit/claude-job-scout |
| SKILL.md path | skills/_profile-optimizer/SKILL.md |
| Sample stratum | supporting_no_scripts |
| Folder complete in GitSkills | True |
| Coverage | complete: every planned configuration produced a COMPLETE scan |
## Scans
| configuration | status | findings_count | max_severity | status_detail |
|---|---|---|---|---|
| SKILL.md only \| default | COMPLETE | 28 | HIGH | exit code 0 |
| SKILL.md only \| behavioral | COMPLETE | 28 | HIGH | exit code 0 |
| Full folder \| default | COMPLETE | 30 | HIGH | exit code 0 |
| Full folder \| behavioral | COMPLETE | 30 | HIGH | exit code 0 |
## Security alerts
Each block is one alert row (one configuration). Snippets are Cisco's evidence text, redacted where it looks like a secret; they are untrusted skill content, shown as plain text.
### HIGH · YARA_jailbreak_generic · SKILL.md:3
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | cc1c262889 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | SKILL.md only \| default; SKILL.md only \| behavioral; Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | prompt_injection |
| Analyzer | static |
| Evidence check | mismatch |
| Title | JAILBREAK detected by YARA |
Evidence snippet:

```text
This file is a lightweight orchestrator. Full guidance for each profile section, activity/engagement advice, and the scoring rubric live in lazy-loaded reference files under `references/`. Load a reference only when its content is needed for the current step — this keeps the context window small on routine runs.
```
### HIGH · YARA_jailbreak_generic · SKILL.md:13
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | f90c6883a6 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | SKILL.md only \| default; SKILL.md only \| behavioral; Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | prompt_injection |
| Analyzer | static |
| Evidence check | mismatch |
| Title | JAILBREAK detected by YARA |
Evidence snippet:

```text
**Master keyword list:** Reuse the list from `user-profile.json` → `master_keyword_list` (produced by `_cv-optimizer`). If it doesn't exist, build it from the CV: every hard skill, tool, framework, methodology, certification, and industry term. This list is the single source of truth for all keyword placement across the profile.
```
### HIGH · YARA_jailbreak_generic · SKILL.md:21
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | dd45962c52 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | SKILL.md only \| default; SKILL.md only \| behavioral; Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | prompt_injection |
| Analyzer | static |
| Evidence check | mismatch |
| Title | JAILBREAK detected by YARA |
Evidence snippet:

```text
| 1. Headline (220 chars) | `references/sections/headline.md` |
```
### HIGH · YARA_jailbreak_generic · SKILL.md:22
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | e29875bbee |
| Provisional label |  |
| Final (human) label |  |
| Configurations | SKILL.md only \| default; SKILL.md only \| behavioral; Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | prompt_injection |
| Analyzer | static |
| Evidence check | mismatch |
| Title | JAILBREAK detected by YARA |
Evidence snippet:

```text
| 2. About / Summary (200-400 words) | `references/sections/about.md` |
```
### HIGH · YARA_jailbreak_generic · SKILL.md:23
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 0d4f6a3422 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | SKILL.md only \| default; SKILL.md only \| behavioral; Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | prompt_injection |
| Analyzer | static |
| Evidence check | mismatch |
| Title | JAILBREAK detected by YARA |
Evidence snippet:

```text
| 3. Experience | `references/sections/experience.md` |
```
### HIGH · YARA_jailbreak_generic · SKILL.md:24
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | b8742785ce |
| Provisional label |  |
| Final (human) label |  |
| Configurations | SKILL.md only \| default; SKILL.md only \| behavioral; Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | prompt_injection |
| Analyzer | static |
| Evidence check | mismatch |
| Title | JAILBREAK detected by YARA |
Evidence snippet:

```text
| 4. Skills & Endorsements | `references/sections/skills.md` |
```
### HIGH · YARA_jailbreak_generic · SKILL.md:25
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | b01b3bd57e |
| Provisional label |  |
| Final (human) label |  |
| Configurations | SKILL.md only \| default; SKILL.md only \| behavioral; Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | prompt_injection |
| Analyzer | static |
| Evidence check | mismatch |
| Title | JAILBREAK detected by YARA |
Evidence snippet:

```text
| 5. Featured Section | `references/sections/featured.md` |
```
### HIGH · YARA_jailbreak_generic · SKILL.md:26
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | a10e249d75 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | SKILL.md only \| default; SKILL.md only \| behavioral; Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | prompt_injection |
| Analyzer | static |
| Evidence check | mismatch |
| Title | JAILBREAK detected by YARA |
Evidence snippet:

```text
| 6. Additional Sections | `references/sections/additional.md` |
```
### HIGH · YARA_jailbreak_generic · SKILL.md:27
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 3c2f60d472 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | SKILL.md only \| default; SKILL.md only \| behavioral; Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | prompt_injection |
| Analyzer | static |
| Evidence check | mismatch |
| Title | JAILBREAK detected by YARA |
Evidence snippet:

```text
| 7. Open to Work Signal | `references/sections/open-to-work.md` + `references/open-to-work-config.md` |
```
### HIGH · YARA_jailbreak_generic · SKILL.md:28
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | cfe623c415 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | SKILL.md only \| default; SKILL.md only \| behavioral; Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | prompt_injection |
| Analyzer | static |
| Evidence check | mismatch |
| Title | JAILBREAK detected by YARA |
Evidence snippet:

```text
| 8. Structured Profile Fields | `references/sections/structured-fields.md` |
```
### HIGH · YARA_jailbreak_generic · SKILL.md:32
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | cdff830977 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | SKILL.md only \| default; SKILL.md only \| behavioral; Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | prompt_injection |
| Analyzer | static |
| Evidence check | mismatch |
| Title | JAILBREAK detected by YARA |
Evidence snippet:

```text
Static profile content is necessary but not sufficient. The LinkedIn algorithm rewards active profiles. Load `references/activity-engagement.md` when the user wants advice on SSI, posting cadence, or creator mode.
```
### HIGH · YARA_jailbreak_generic · SKILL.md:47
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 5432ac4534 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | SKILL.md only \| default; SKILL.md only \| behavioral; Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | prompt_injection |
| Analyzer | static |
| Evidence check | mismatch |
| Title | JAILBREAK detected by YARA |
Evidence snippet:

```text
- Construct likely Boolean queries a recruiter would run for the user's target role based on `references/recruiter-search-patterns.md`
```
### HIGH · YARA_jailbreak_generic · SKILL.md:49
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 8a223b04bb |
| Provisional label |  |
| Final (human) label |  |
| Configurations | SKILL.md only \| default; SKILL.md only \| behavioral; Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | prompt_injection |
| Analyzer | static |
| Evidence check | mismatch |
| Title | JAILBREAK detected by YARA |
Evidence snippet:

```text
- Example: `"data engineer" AND "Spark" AND "AWS" AND "remote"` — would this profile match?
```
### HIGH · YARA_jailbreak_generic · SKILL.md:53
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | a9157a596a |
| Provisional label |  |
| Final (human) label |  |
| Configurations | SKILL.md only \| default; SKILL.md only \| behavioral; Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | prompt_injection |
| Analyzer | static |
| Evidence check | mismatch |
| Title | JAILBREAK detected by YARA |
Evidence snippet:

```text
Load `references/scoring-framework.md` when computing scores. It covers per-section scoring, cross-cutting scores (keyword coverage, search appearance, 10-second test, CV alignment), and the weighted overall score.
```
### HIGH · YARA_jailbreak_generic · SKILL.md:66
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | fdf74755bc |
| Provisional label |  |
| Final (human) label |  |
| Configurations | SKILL.md only \| default; SKILL.md only \| behavioral; Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | prompt_injection |
| Analyzer | static |
| Evidence check | mismatch |
| Title | JAILBREAK detected by YARA |
Evidence snippet:

```text
1. **Load CV** — follow `shared-references/cv-loading.md`. Extract structured data (roles, skills, achievements, keywords). Reuse master keyword list from `user-profile.json` if available.
```
### HIGH · YARA_jailbreak_generic · SKILL.md:72
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 59c0be932d |
| Provisional label |  |
| Final (human) label |  |
| Configurations | SKILL.md only \| default; SKILL.md only \| behavioral; Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | prompt_injection |
| Analyzer | static |
| Evidence check | mismatch |
| Title | JAILBREAK detected by YARA |
Evidence snippet:

```text
6. **Generate section-by-section proposals** — ready-to-paste content derived from CV. For sections with supporting-doc coverage (Featured, About, Experience), consult `.job-scout/cache/supporting-docs.json` and cite source documents in the proposal table per `shared-references/supporting-docs.md` consumer contract.
```
### HIGH · YARA_jailbreak_generic · SKILL.md:119
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | cb679a99a9 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | SKILL.md only \| default; SKILL.md only \| behavioral; Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | prompt_injection |
| Analyzer | static |
| Evidence check | mismatch |
| Title | JAILBREAK detected by YARA |
Evidence snippet:

```text
- **`references/sections/*.md`** — one file per profile section (lazy-loaded)
```
### HIGH · YARA_jailbreak_generic · SKILL.md:120
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 07b9d4e7b0 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | SKILL.md only \| default; SKILL.md only \| behavioral; Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | prompt_injection |
| Analyzer | static |
| Evidence check | mismatch |
| Title | JAILBREAK detected by YARA |
Evidence snippet:

```text
- **`references/activity-engagement.md`** — SSI, content strategy, creator mode (lazy-loaded)
```
### HIGH · YARA_jailbreak_generic · SKILL.md:121
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 1d1aba7b8c |
| Provisional label |  |
| Final (human) label |  |
| Configurations | SKILL.md only \| default; SKILL.md only \| behavioral; Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | prompt_injection |
| Analyzer | static |
| Evidence check | mismatch |
| Title | JAILBREAK detected by YARA |
Evidence snippet:

```text
- **`references/scoring-framework.md`** — section + cross-cutting scoring (lazy-loaded)
```
### HIGH · YARA_jailbreak_generic · SKILL.md:122
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | bafecfd4c3 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | SKILL.md only \| default; SKILL.md only \| behavioral; Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | prompt_injection |
| Analyzer | static |
| Evidence check | mismatch |
| Title | JAILBREAK detected by YARA |
Evidence snippet:

```text
- **`references/linkedin-seo.md`** — Algorithm factors, keyword strategy, recruiter behaviour
```
### HIGH · YARA_jailbreak_generic · SKILL.md:123
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 0db5763f0a |
| Provisional label |  |
| Final (human) label |  |
| Configurations | SKILL.md only \| default; SKILL.md only \| behavioral; Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | prompt_injection |
| Analyzer | static |
| Evidence check | mismatch |
| Title | JAILBREAK detected by YARA |
Evidence snippet:

```text
- **`references/headline-formulas.md`** — Headline templates by role
```
### HIGH · YARA_jailbreak_generic · SKILL.md:124
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 155cf8ede7 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | SKILL.md only \| default; SKILL.md only \| behavioral; Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | prompt_injection |
| Analyzer | static |
| Evidence check | mismatch |
| Title | JAILBREAK detected by YARA |
Evidence snippet:

```text
- **`references/recruiter-search-patterns.md`** — Boolean queries, title mappings
```
### HIGH · YARA_jailbreak_generic · SKILL.md:125
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 2837cafc70 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | SKILL.md only \| default; SKILL.md only \| behavioral; Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | prompt_injection |
| Analyzer | static |
| Evidence check | mismatch |
| Title | JAILBREAK detected by YARA |
Evidence snippet:

```text
- **`references/open-to-work-config.md`** — Open to Work setup guide
```
### HIGH · YARA_jailbreak_generic · SKILL.md:126
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | b6a4188935 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | SKILL.md only \| default; SKILL.md only \| behavioral; Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | prompt_injection |
| Analyzer | static |
| Evidence check | mismatch |
| Title | JAILBREAK detected by YARA |
Evidence snippet:

```text
- **`../shared-references/workspace-layout.md`** — `.job-scout/` folder layout and bootstrap
```
### HIGH · YARA_jailbreak_generic · SKILL.md:127
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 1d09d791d8 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | SKILL.md only \| default; SKILL.md only \| behavioral; Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | prompt_injection |
| Analyzer | static |
| Evidence check | mismatch |
| Title | JAILBREAK detected by YARA |
Evidence snippet:

```text
- **`../shared-references/cv-loading.md`** — CV loading + caching procedure
```
### HIGH · YARA_jailbreak_generic · SKILL.md:128
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 6f84f62a61 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | SKILL.md only \| default; SKILL.md only \| behavioral; Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | prompt_injection |
| Analyzer | static |
| Evidence check | mismatch |
| Title | JAILBREAK detected by YARA |
Evidence snippet:

```text
- **`../shared-references/subagent-protocol.md`** — Subagent dispatch contract
```
### HIGH · YARA_jailbreak_generic · references/sections/skills.md:7
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 8501323b63 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | prompt_injection |
| Analyzer | static |
| Evidence check | exact |
| Title | JAILBREAK detected by YARA |
Evidence snippet:

```text
Build the skills list directly from the master keyword list:
```
### HIGH · YARA_jailbreak_generic · references/sections/skills.md:8
|  | value |
|---|---|
| Validation | Scanner alert, awaiting human review |
| Review ID | 62400be6e5 |
| Provisional label |  |
| Final (human) label |  |
| Configurations | Full folder \| default; Full folder \| behavioral |
| Scan outcomes | complete |
| Cisco category | prompt_injection |
| Analyzer | static |
| Evidence check | exact |
| Title | JAILBREAK detected by YARA |
Evidence snippet:

```text
- Extract every hard skill, tool, framework, methodology, and certification mentioned in CV
```
## Other notes

8 metadata-quality / scan-coverage rows: MANIFEST_INVALID_NAME (4), MANIFEST_MISSING_LICENSE (4).
