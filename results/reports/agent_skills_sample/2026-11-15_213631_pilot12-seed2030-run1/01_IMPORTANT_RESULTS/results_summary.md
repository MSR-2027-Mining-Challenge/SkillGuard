# Cisco Skill Scanner results: `2026-11-15_213631_pilot12-seed2030-run1`

Generated automatically by `notebooks/01_cisco_scanner_dataset_ready.ipynb` on 2026-11-16T05:40:28+00:00. Every number below is computed from the files in this run folder. A finding is a Cisco rule match on an operation, not a confirmed vulnerability.

## A. Experiment overview

| item | value |
|---|---|
| Run ID | 2026-11-15_213631_pilot12-seed2030-run1 |
| Run mode | scan (Cisco executed in this run) |
| Dataset | agent_skills_sample.db (SHA-256 683888c923a5...) |
| Sample | agent_skills_sample_seed2030_scripts400_supporting_no_scripts300_skill_md_only300 (12 skills; manifest results/skillguard_runs/main1000/manifests/pilot12_manifest.csv) |
| Scanner version that produced the reports | skill-scanner 2.3.1 |
| Scan policy (name / preset) | default / balanced |
| Policy fingerprint(s) | 3f48e661bfbc... |
| Scans executed (report timestamps, UTC) | 2026-11-16 05:36:36 to 2026-11-16 05:40:26 |
| Analysis written | 2026-11-16T05:40:28+00:00 |
| Skills selected / exported | 12 / 12 |
| Skill folders complete / incomplete | 10 / 2 |
| Configurations per skill | 4 |
| Configurations planned (skills x configurations) | 48 |
| Cisco scans executed | 48 |
| Configurations excluded by design: incomplete GitSkills folder (full-folder scan not run) | 0 |
| Outcomes of the executed scans | complete: 48, contract_only: 0, partial: 0, failed: 0 |
| Finding records (all readable reports) | 50 (complete scans: 50, contract-only scans: 0, partial scans: 0) |
| Security finding records in complete scans | 10 |
| Distinct rule/location combinations (skill, rule, file, line), all findings | 15 |
| Distinct rule/location combinations, security findings in complete scans | 5 |


Planned configurations, executed Cisco scans and outcomes per configuration. complete = primary results; contract_only = only Cisco's known rule-registration error, used in the sensitivity analysis only; partial = other analyzer problems, preliminary only; failed = Cisco ran but produced no usable report; excluded_incomplete_folder = design exclusion, Cisco was not run because GitSkills did not store the whole folder; missing = no saved report:

| configuration | planned | executed | complete | contract_only | partial | failed | excluded_incomplete_folder | missing |
|---|---|---|---|---|---|---|---|---|
| SKILL.md only \| default | 12 | 12 | 12 | 0 | 0 | 0 | 0 | 0 |
| SKILL.md only \| behavioral | 12 | 12 | 12 | 0 | 0 | 0 | 0 | 0 |
| Full folder \| default | 12 | 12 | 12 | 0 | 0 | 0 | 0 | 0 |
| Full folder \| behavioral | 12 | 12 | 12 | 0 | 0 | 0 | 0 | 0 |
| total | 48 | 48 | 48 | 0 | 0 | 0 | 0 | 0 |


Results by sampling stratum. Strata were sampled with equal allocation, so counts within a stratum can be reported directly, but proportions for the whole population need the design weights in `sample/sampling_metadata.json`:

| stratum | skills | complete folders | configurations planned | scans executed | scans complete | scans contract_only | scans partial | scans failed | configurations excluded_incomplete_folder | configurations missing | skills with >= 1 security finding (complete scans) | security finding records (complete scans) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| scripts | 4 | 3 | 16 | 16 | 16 | 0 | 0 | 0 | 0 | 0 | 1 | 2 |
| supporting_no_scripts | 4 | 3 | 16 | 16 | 16 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| skill_md_only | 4 | 4 | 16 | 16 | 16 | 0 | 0 | 0 | 0 | 0 | 1 | 8 |


## B. Security findings (complete scans only)

B1. Findings by severity

| configuration | CRITICAL | HIGH | MEDIUM | LOW |
|---|---|---|---|---|
| SKILL.md only \| default | 0 | 0 | 0 | 0 |
| SKILL.md only \| behavioral | 0 | 0 | 4 | 0 |
| Full folder \| default | 0 | 0 | 0 | 1 |
| Full folder \| behavioral | 0 | 0 | 4 | 1 |


B2. Findings by Cisco category (per configuration) and distinct skills affected (any complete configuration)

| cisco_category | SKILL.md only \| default | SKILL.md only \| behavioral | Full folder \| default | Full folder \| behavioral | distinct_skills |
|---|---|---|---|---|---|
| data_exfiltration | 0 | 4 | 0 | 4 | 1 |
| supply_chain_attack | 0 | 0 | 1 | 1 | 1 |


B3. Findings by research category (our mapping; categories without Cisco rules stay at zero)

| research_category | SKILL.md only \| default | SKILL.md only \| behavioral | Full folder \| default | Full folder \| behavioral | distinct_skills |
|---|---|---|---|---|---|
| Credential / secret access or exposure | 0 | 0 | 0 | 0 | 0 |
| External network communication / data exfiltration | 0 | 4 | 0 | 4 | 1 |
| Command execution / dangerous shell operations | 0 | 0 | 0 | 0 | 0 |
| File-system access or modification | 0 | 0 | 0 | 0 | 0 |
| Prompt injection / instruction manipulation | 0 | 0 | 0 | 0 | 0 |
| Excessive permissions / privilege escalation | 0 | 0 | 0 | 0 | 0 |
| Supply-chain / dependency risks | 0 | 0 | 1 | 1 | 1 |
| Account modification / sensitive external actions | 0 | 0 | 0 | 0 | 0 |


B4. Most frequently triggered security rules

| rule_id | cisco_category | findings | distinct_skills | severities |
|---|---|---|---|---|
| MDBLOCK_PYTHON_HTTP_POST | data_exfiltration | 8 | 1 | MEDIUM |
| SUPPLY_CHAIN_UNPINNED_DEPENDENCY | supply_chain_attack | 2 | 1 | LOW |


B5. Where the findings point

| location | SKILL.md only \| default | SKILL.md only \| behavioral | Full folder \| default | Full folder \| behavioral |
|---|---|---|---|---|
| SKILL.md | 0 | 4 | 0 | 4 |
| supporting file | 0 | 0 | 1 | 1 |


B6. Findings outside the primary group: contract-only and partial scans (excluded from B1-B5)

_No data._


## C. Configuration comparisons

The **primary analysis** uses only pairs in which both scans are COMPLETE (and, for SKILL.md-only vs full-folder, the folder is complete). The **sensitivity analysis** adds pairs that contain a CONTRACT_ONLY scan. Contract-only scans are not assumed complete or accurate; the sensitivity analysis only shows whether including them would change a result.

C1. Sample sizes and excluded pairs per comparison (`excluded_*` = pairs left out of the primary analysis, by reason; contract-only pairs are added back in the sensitivity analysis)

| comparison | pairs_total | primary_n | sensitivity_n | excluded_contract_only | excluded_partial | excluded_incomplete_folder | excluded_not_comparable |
|---|---|---|---|---|---|---|---|
| SKILL.md only -> Full folder: default | 12 | 10 | 10 | 0 | 0 | 2 | 0 |
| SKILL.md only -> Full folder: behavioral | 12 | 10 | 10 | 0 | 0 | 2 | 0 |
| default -> behavioral: SKILL.md only | 12 | 12 | 12 | 0 | 0 | 0 | 0 |
| default -> behavioral: Full folder | 12 | 12 | 12 | 0 | 0 | 0 | 0 |


C2. Primary analysis (complete scans only): finding-level changes summed over the pairs used

| comparison | pairs_used | pairs_with_findings | unchanged | changed | possibly_equivalent | additional | missing | skills_with_additional |
|---|---|---|---|---|---|---|---|---|
| SKILL.md only -> Full folder: default | 10 | 1 | 0 | 0 | 0 | 1 | 0 | 1 |
| SKILL.md only -> Full folder: behavioral | 10 | 2 | 4 | 0 | 0 | 1 | 0 | 1 |
| default -> behavioral: SKILL.md only | 12 | 1 | 0 | 0 | 0 | 4 | 0 | 1 |
| default -> behavioral: Full folder | 12 | 2 | 1 | 0 | 0 | 4 | 0 | 1 |


C3. Files that contribute the additional findings in the primary SKILL.md-only vs full-folder comparison (a SKILL.md row means Cisco re-read the instructions once the scripts were present)

| location | file_path | findings | skills | rules |
|---|---|---|---|---|
| supporting file | pyproject.toml | 2 | 1 | SUPPLY_CHAIN_UNPINNED_DEPENDENCY |


C4. Sensitivity analysis (complete + contract-only scans): finding-level changes summed over the pairs used

| comparison | pairs_used | pairs_with_findings | unchanged | changed | possibly_equivalent | additional | missing | skills_with_additional |
|---|---|---|---|---|---|---|---|---|
| SKILL.md only -> Full folder: default | 10 | 1 | 0 | 0 | 0 | 1 | 0 | 1 |
| SKILL.md only -> Full folder: behavioral | 10 | 2 | 4 | 0 | 0 | 1 | 0 | 1 |
| default -> behavioral: SKILL.md only | 12 | 1 | 0 | 0 | 0 | 4 | 0 | 1 |
| default -> behavioral: Full folder | 12 | 2 | 1 | 0 | 0 | 4 | 0 | 1 |


C5. Does including contract-only scans change the comparisons?

- SKILL.md only -> Full folder: default: no contract-only pairs, so the sensitivity analysis equals the primary analysis (n = 10).
- SKILL.md only -> Full folder: behavioral: no contract-only pairs, so the sensitivity analysis equals the primary analysis (n = 10).
- default -> behavioral: SKILL.md only: no contract-only pairs, so the sensitivity analysis equals the primary analysis (n = 12).
- default -> behavioral: Full folder: no contract-only pairs, so the sensitivity analysis equals the primary analysis (n = 12).

C6. Pair status per skill

| comparison | skill_id | before | after | pair_status |
|---|---|---|---|---|
| SKILL.md only -> Full folder: default | taxonomy-7c7d8d0b722f | SKILL.md only \| default (COMPLETE) | Full folder \| default (COMPLETE) | eligible |
| SKILL.md only -> Full folder: behavioral | taxonomy-7c7d8d0b722f | SKILL.md only \| behavioral (COMPLETE) | Full folder \| behavioral (COMPLETE) | eligible |
| SKILL.md only -> Full folder: default | performing-threat-modeling-with-owa-544917512477 | SKILL.md only \| default (COMPLETE) | Full folder \| default (COMPLETE) | eligible |
| SKILL.md only -> Full folder: behavioral | performing-threat-modeling-with-owa-544917512477 | SKILL.md only \| behavioral (COMPLETE) | Full folder \| behavioral (COMPLETE) | eligible |
| SKILL.md only -> Full folder: default | kafka-to-s3-6a3f6d978c83 | SKILL.md only \| default (COMPLETE) | Full folder \| default (COMPLETE) | eligible |
| SKILL.md only -> Full folder: behavioral | kafka-to-s3-6a3f6d978c83 | SKILL.md only \| behavioral (COMPLETE) | Full folder \| behavioral (COMPLETE) | eligible |
| SKILL.md only -> Full folder: default | quiz-generator-acd0e5548bb6 | SKILL.md only \| default (COMPLETE) | Full folder \| default (COMPLETE) | preliminary: incomplete folder |
| SKILL.md only -> Full folder: behavioral | quiz-generator-acd0e5548bb6 | SKILL.md only \| behavioral (COMPLETE) | Full folder \| behavioral (COMPLETE) | preliminary: incomplete folder |
| SKILL.md only -> Full folder: default | dot-matrix-xhs-3fc170f5ec5d | SKILL.md only \| default (COMPLETE) | Full folder \| default (COMPLETE) | preliminary: incomplete folder |
| SKILL.md only -> Full folder: behavioral | dot-matrix-xhs-3fc170f5ec5d | SKILL.md only \| behavioral (COMPLETE) | Full folder \| behavioral (COMPLETE) | preliminary: incomplete folder |
| SKILL.md only -> Full folder: default | ma-sanli-writer-c54bc9f0546b | SKILL.md only \| default (COMPLETE) | Full folder \| default (COMPLETE) | eligible |
| SKILL.md only -> Full folder: behavioral | ma-sanli-writer-c54bc9f0546b | SKILL.md only \| behavioral (COMPLETE) | Full folder \| behavioral (COMPLETE) | eligible |
| SKILL.md only -> Full folder: default | godmode-8823f2e9cfcf | SKILL.md only \| default (COMPLETE) | Full folder \| default (COMPLETE) | eligible |
| SKILL.md only -> Full folder: behavioral | godmode-8823f2e9cfcf | SKILL.md only \| behavioral (COMPLETE) | Full folder \| behavioral (COMPLETE) | eligible |
| SKILL.md only -> Full folder: default | telegram-dispatch-fa00b31a99ee | SKILL.md only \| default (COMPLETE) | Full folder \| default (COMPLETE) | eligible |
| SKILL.md only -> Full folder: behavioral | telegram-dispatch-fa00b31a99ee | SKILL.md only \| behavioral (COMPLETE) | Full folder \| behavioral (COMPLETE) | eligible |
| SKILL.md only -> Full folder: default | talk-storytelling-6b392902cf98 | SKILL.md only \| default (COMPLETE) | Full folder \| default (COMPLETE) | eligible |
| SKILL.md only -> Full folder: behavioral | talk-storytelling-6b392902cf98 | SKILL.md only \| behavioral (COMPLETE) | Full folder \| behavioral (COMPLETE) | eligible |
| SKILL.md only -> Full folder: default | bench-onboarding-9f9333898365 | SKILL.md only \| default (COMPLETE) | Full folder \| default (COMPLETE) | eligible |
| SKILL.md only -> Full folder: behavioral | bench-onboarding-9f9333898365 | SKILL.md only \| behavioral (COMPLETE) | Full folder \| behavioral (COMPLETE) | eligible |

_28 more row(s) in the CSV files._


## D. Scanner reliability

D1. Analyzer failures reported by Cisco

_No data._


D2. Skill folders

| skill_id | supporting_files_exported | files_missing | folder_complete | integrity |
|---|---|---|---|---|
| taxonomy-7c7d8d0b722f | 4 | 0 | True | ok: written in this run |
| performing-threat-modeling-with-owa-544917512477 | 7 | 0 | True | ok: written in this run |
| kafka-to-s3-6a3f6d978c83 | 3 | 0 | True | ok: written in this run |
| quiz-generator-acd0e5548bb6 | 2 | 0 | False | ok: written in this run |
| dot-matrix-xhs-3fc170f5ec5d | 0 | 1 | False | ok: written in this run |
| ma-sanli-writer-c54bc9f0546b | 2 | 0 | True | ok: written in this run |
| godmode-8823f2e9cfcf | 1 | 0 | True | ok: written in this run |
| telegram-dispatch-fa00b31a99ee | 2 | 0 | True | ok: written in this run |
| talk-storytelling-6b392902cf98 | 0 | 0 | True | ok: written in this run |
| bench-onboarding-9f9333898365 | 0 | 0 | True | ok: written in this run |
| review-dispute-resolution-mechanism-8afeeb24ea09 | 0 | 0 | True | ok: written in this run |
| implementing-canary-tokens-for-netw-07811ef04df1 | 0 | 0 | True | ok: written in this run |


D3. Scanner verdict vs finding severity

| skill_id | configuration | outcome | is_safe | cisco_max_severity | highest_security_severity | security_findings | security_medium_or_lower | note |
|---|---|---|---|---|---|---|---|---|
| taxonomy-7c7d8d0b722f | SKILL.md only \| default | complete | True | INFO | none | 0 | 0 | only metadata/coverage findings |
| taxonomy-7c7d8d0b722f | SKILL.md only \| behavioral | complete | True | INFO | none | 0 | 0 | only metadata/coverage findings |
| taxonomy-7c7d8d0b722f | Full folder \| default | complete | True | LOW | LOW | 1 | 1 | is_safe=True although there are 1 security finding(s) up to LOW |
| taxonomy-7c7d8d0b722f | Full folder \| behavioral | complete | True | LOW | LOW | 1 | 1 | is_safe=True although there are 1 security finding(s) up to LOW |
| performing-threat-modeling-with-owa-544917512477 | SKILL.md only \| default | complete | True | SAFE | none | 0 | 0 | no findings |
| performing-threat-modeling-with-owa-544917512477 | SKILL.md only \| behavioral | complete | True | SAFE | none | 0 | 0 | no findings |
| performing-threat-modeling-with-owa-544917512477 | Full folder \| default | complete | True | SAFE | none | 0 | 0 | no findings |
| performing-threat-modeling-with-owa-544917512477 | Full folder \| behavioral | complete | True | SAFE | none | 0 | 0 | no findings |
| kafka-to-s3-6a3f6d978c83 | SKILL.md only \| default | complete | True | INFO | none | 0 | 0 | only metadata/coverage findings |
| kafka-to-s3-6a3f6d978c83 | SKILL.md only \| behavioral | complete | True | INFO | none | 0 | 0 | only metadata/coverage findings |
| kafka-to-s3-6a3f6d978c83 | Full folder \| default | complete | True | INFO | none | 0 | 0 | only metadata/coverage findings |
| kafka-to-s3-6a3f6d978c83 | Full folder \| behavioral | complete | True | INFO | none | 0 | 0 | only metadata/coverage findings |
| quiz-generator-acd0e5548bb6 | SKILL.md only \| default | complete | True | INFO | none | 0 | 0 | only metadata/coverage findings |
| quiz-generator-acd0e5548bb6 | SKILL.md only \| behavioral | complete | True | INFO | none | 0 | 0 | only metadata/coverage findings |
| quiz-generator-acd0e5548bb6 | Full folder \| default | complete | True | INFO | none | 0 | 0 | only metadata/coverage findings |
| quiz-generator-acd0e5548bb6 | Full folder \| behavioral | complete | True | INFO | none | 0 | 0 | only metadata/coverage findings |
| dot-matrix-xhs-3fc170f5ec5d | SKILL.md only \| default | complete | True | INFO | none | 0 | 0 | only metadata/coverage findings |
| dot-matrix-xhs-3fc170f5ec5d | SKILL.md only \| behavioral | complete | True | INFO | none | 0 | 0 | only metadata/coverage findings |
| dot-matrix-xhs-3fc170f5ec5d | Full folder \| default | complete | True | INFO | none | 0 | 0 | only metadata/coverage findings |
| dot-matrix-xhs-3fc170f5ec5d | Full folder \| behavioral | complete | True | INFO | none | 0 | 0 | only metadata/coverage findings |

_28 more row(s) in the CSV files._


D4. Evidence check of reported locations (counts of finding records per rule)

| rule_id | ambiguous | exact | mismatch | unavailable |
|---|---|---|---|---|
| MANIFEST_MISSING_LICENSE | 0 | 0 | 0 | 36 |
| MDBLOCK_PYTHON_HTTP_POST | 6 | 0 | 2 | 0 |
| SOCIAL_ENG_VAGUE_DESCRIPTION | 0 | 0 | 0 | 4 |
| SUPPLY_CHAIN_UNPINNED_DEPENDENCY | 0 | 2 | 0 | 0 |


## E. Manual security review

`manual_review_template.csv` lists 5 distinct security finding location(s) (0 seen only in contract-only or partial scans) with Cisco's rule, severity, reported file and line, redacted evidence and evidence check. The columns `reviewer`, `evidence_verified`, `legitimate_purpose`, `interpretation` and `notes` are intentionally blank; no finding has been labelled as a vulnerability or a false positive.


## Figures

![Security findings by Cisco category and configuration (complete scans)](../02_DETAILED_ANALYSIS/figures/findings_by_category.png)

![Severity of security findings per configuration (complete scans)](../02_DETAILED_ANALYSIS/figures/severity_by_configuration.png)

![Finding-level changes between configurations (primary analysis: complete scans)](../02_DETAILED_ANALYSIS/figures/configuration_comparisons.png)


## Limitations

- 2 skill folder(s) are incomplete in GitSkills (1 supporting file(s) without stored text). This is a design exclusion, not a scanner failure: 0 of 48 planned configuration(s) (their full-folder scans) were not run, so 48 Cisco scans were executed. Their SKILL.md-only scans are kept, but their context-comparison pairs are reported as `excluded: incomplete folder`, and no finding count of zero is implied for the excluded configurations.
- 8 of 50 finding record(s) do not have their evidence on the reported line (mismatch 2, ambiguous 6); rules involved: MDBLOCK_PYTHON_HTTP_POST (8). Reported line numbers are kept unchanged.
- For MDBLOCK_* rules Cisco 2.3.1 counts lines from the code-block fence and, in SKILL.md, from the end of the YAML frontmatter, so their reported lines point above the code; use evidence_candidate_lines to locate it.
- 40 finding record(s) could not be checked against the file (no file, line or evidence text).
- Only 12 skill(s) were analysed: these are pilot observations, not population estimates.
- Scanner findings are rule matches on operations; they are not confirmed vulnerabilities, and nothing here is a false-negative claim (there is no ground truth).
- Finding counts are per matching line; one script can contribute many findings. Distinct skills are reported separately.
- Comparisons match findings by rule, file, reported line and evidence; equivalent behavior reported under different rule IDs is not matched automatically.


## Files in this run folder

- `scan_summary.csv`: one row per skill x configuration: status, outcome, analyzer failures, verdict, counts, versions
- `individual_findings.csv`: one row per Cisco finding: original fields, normalized path, evidence check
- `context_comparison.csv / analyzer_comparison.csv`: finding-level comparisons; pair_status says primary (eligible), sensitivity or preliminary
- `manual_review_template.csv`: blank reviewer columns for manual interpretation
- `run_metadata.json`: settings, dataset hash, scanner versions, policy fingerprints, outcome counts
- `<skill_id>/reports/*.json`: raw Cisco reports, unmodified
- `<skill_id>/manifest.json`: exported files with SHA-256 hashes and missing files
- `figures/*.png`: the charts above
