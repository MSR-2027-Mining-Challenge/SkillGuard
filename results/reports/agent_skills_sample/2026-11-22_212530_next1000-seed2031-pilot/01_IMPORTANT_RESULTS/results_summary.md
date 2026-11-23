# Cisco Skill Scanner results: `2026-11-22_212530_next1000-seed2031-pilot`

Generated automatically by `notebooks/01_cisco_scanner_dataset_ready.ipynb` on 2026-11-23T05:29:23+00:00. Every number below is computed from the files in this run folder. A finding is a Cisco rule match on an operation, not a confirmed vulnerability.

## A. Experiment overview

| item | value |
|---|---|
| Run ID | 2026-11-22_212530_next1000-seed2031-pilot |
| Run mode | scan (Cisco executed in this run) |
| Dataset | agent_skills_sample.db (SHA-256 683888c923a5...) |
| Sample | agent_skills_sample_seed2031_scripts400_supporting_no_scripts300_skill_md_only300 (12 skills; manifest results/skillguard_runs/next1000/manifests/pilot12_manifest.csv) |
| Scanner version that produced the reports | skill-scanner 2.3.1 |
| Scan policy (name / preset) | default / balanced |
| Policy fingerprint(s) | 3f48e661bfbc... |
| Scans executed (report timestamps, UTC) | 2026-11-23 05:25:35 to 2026-11-23 05:29:21 |
| Analysis written | 2026-11-23T05:29:23+00:00 |
| Skills selected / exported | 12 / 12 |
| Skill folders complete / incomplete | 10 / 2 |
| Configurations per skill | 4 |
| Configurations planned (skills x configurations) | 48 |
| Cisco scans executed | 48 |
| Configurations excluded by design: incomplete GitSkills folder (full-folder scan not run) | 0 |
| Outcomes of the executed scans | complete: 48, contract_only: 0, partial: 0, failed: 0 |
| Finding records (all readable reports) | 54 (complete scans: 54, contract-only scans: 0, partial scans: 0) |
| Security finding records in complete scans | 18 |
| Distinct rule/location combinations (skill, rule, file, line), all findings | 16 |
| Distinct rule/location combinations, security findings in complete scans | 7 |


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
| supporting_no_scripts | 4 | 3 | 16 | 16 | 16 | 0 | 0 | 0 | 0 | 0 | 2 | 16 |
| skill_md_only | 4 | 4 | 16 | 16 | 16 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |


## B. Security findings (complete scans only)

B1. Findings by severity

| configuration | CRITICAL | HIGH | MEDIUM | LOW |
|---|---|---|---|---|
| SKILL.md only \| default | 1 | 1 | 0 | 0 |
| SKILL.md only \| behavioral | 1 | 1 | 2 | 0 |
| Full folder \| default | 1 | 1 | 1 | 2 |
| Full folder \| behavioral | 1 | 1 | 3 | 2 |


B2. Findings by Cisco category (per configuration) and distinct skills affected (any complete configuration)

| cisco_category | SKILL.md only \| default | SKILL.md only \| behavioral | Full folder \| default | Full folder \| behavioral | distinct_skills |
|---|---|---|---|---|---|
| command_injection | 2 | 4 | 2 | 4 | 1 |
| data_exfiltration | 0 | 0 | 1 | 1 | 1 |
| obfuscation | 0 | 0 | 2 | 2 | 1 |


B3. Findings by research category (our mapping; categories without Cisco rules stay at zero)

| research_category | SKILL.md only \| default | SKILL.md only \| behavioral | Full folder \| default | Full folder \| behavioral | distinct_skills |
|---|---|---|---|---|---|
| Credential / secret access or exposure | 0 | 0 | 0 | 0 | 0 |
| External network communication / data exfiltration | 0 | 0 | 1 | 1 | 1 |
| Command execution / dangerous shell operations | 2 | 4 | 2 | 4 | 1 |
| File-system access or modification | 0 | 0 | 0 | 0 | 0 |
| Prompt injection / instruction manipulation | 0 | 0 | 0 | 0 | 0 |
| Excessive permissions / privilege escalation | 0 | 0 | 0 | 0 | 0 |
| Supply-chain / dependency risks | 0 | 0 | 0 | 0 | 0 |
| Account modification / sensitive external actions | 0 | 0 | 0 | 0 | 0 |
| Other (obfuscation) | 0 | 0 | 2 | 2 | 1 |


B4. Most frequently triggered security rules

| rule_id | cisco_category | findings | distinct_skills | severities |
|---|---|---|---|---|
| ACTIVE_DYNAMIC_EXECUTION | command_injection | 4 | 1 | HIGH |
| FILE_MAGIC_MISMATCH | obfuscation | 4 | 1 | LOW |
| MDBLOCK_PYTHON_SUBPROCESS | command_injection | 4 | 1 | MEDIUM |
| YARA_command_injection_generic | command_injection | 4 | 1 | CRITICAL |
| DATA_EXFIL_JS_NETWORK | data_exfiltration | 2 | 1 | MEDIUM |


B5. Where the findings point

| location | SKILL.md only \| default | SKILL.md only \| behavioral | Full folder \| default | Full folder \| behavioral |
|---|---|---|---|---|
| SKILL.md | 2 | 4 | 2 | 4 |
| supporting file | 0 | 0 | 3 | 3 |


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
| SKILL.md only -> Full folder: default | 10 | 2 | 0 | 0 | 0 | 3 | 0 | 2 |
| SKILL.md only -> Full folder: behavioral | 10 | 2 | 0 | 0 | 0 | 3 | 0 | 2 |
| default -> behavioral: SKILL.md only | 12 | 1 | 2 | 0 | 0 | 2 | 0 | 1 |
| default -> behavioral: Full folder | 12 | 3 | 5 | 0 | 0 | 2 | 0 | 1 |


C3. Files that contribute the additional findings in the primary SKILL.md-only vs full-folder comparison (a SKILL.md row means Cisco re-read the instructions once the scripts were present)

| location | file_path | findings | skills | rules |
|---|---|---|---|---|
| supporting file | scripts/apply-plan.mjs | 2 | 1 | DATA_EXFIL_JS_NETWORK |
| supporting file | templates/prd.template.md | 2 | 1 | FILE_MAGIC_MISMATCH |
| supporting file | templates/screen-prompt.template.md | 2 | 1 | FILE_MAGIC_MISMATCH |


C4. Sensitivity analysis (complete + contract-only scans): finding-level changes summed over the pairs used

| comparison | pairs_used | pairs_with_findings | unchanged | changed | possibly_equivalent | additional | missing | skills_with_additional |
|---|---|---|---|---|---|---|---|---|
| SKILL.md only -> Full folder: default | 10 | 2 | 0 | 0 | 0 | 3 | 0 | 2 |
| SKILL.md only -> Full folder: behavioral | 10 | 2 | 0 | 0 | 0 | 3 | 0 | 2 |
| default -> behavioral: SKILL.md only | 12 | 1 | 2 | 0 | 0 | 2 | 0 | 1 |
| default -> behavioral: Full folder | 12 | 3 | 5 | 0 | 0 | 2 | 0 | 1 |


C5. Does including contract-only scans change the comparisons?

- SKILL.md only -> Full folder: default: no contract-only pairs, so the sensitivity analysis equals the primary analysis (n = 10).
- SKILL.md only -> Full folder: behavioral: no contract-only pairs, so the sensitivity analysis equals the primary analysis (n = 10).
- default -> behavioral: SKILL.md only: no contract-only pairs, so the sensitivity analysis equals the primary analysis (n = 12).
- default -> behavioral: Full folder: no contract-only pairs, so the sensitivity analysis equals the primary analysis (n = 12).

C6. Pair status per skill

| comparison | skill_id | before | after | pair_status |
|---|---|---|---|---|
| SKILL.md only -> Full folder: default | ascii-to-infographic-20a0a3fb5b15 | SKILL.md only \| default (COMPLETE) | Full folder \| default (COMPLETE) | eligible |
| SKILL.md only -> Full folder: behavioral | ascii-to-infographic-20a0a3fb5b15 | SKILL.md only \| behavioral (COMPLETE) | Full folder \| behavioral (COMPLETE) | eligible |
| SKILL.md only -> Full folder: default | codex-counsel-7caabcfebd82 | SKILL.md only \| default (COMPLETE) | Full folder \| default (COMPLETE) | eligible |
| SKILL.md only -> Full folder: behavioral | codex-counsel-7caabcfebd82 | SKILL.md only \| behavioral (COMPLETE) | Full folder \| behavioral (COMPLETE) | eligible |
| SKILL.md only -> Full folder: default | review-l10n-22be0b42ed0e | SKILL.md only \| default (COMPLETE) | Full folder \| default (COMPLETE) | eligible |
| SKILL.md only -> Full folder: behavioral | review-l10n-22be0b42ed0e | SKILL.md only \| behavioral (COMPLETE) | Full folder \| behavioral (COMPLETE) | eligible |
| SKILL.md only -> Full folder: default | deepstream-profile-pipeline-74b92facf0e5 | SKILL.md only \| default (COMPLETE) | Full folder \| default (COMPLETE) | preliminary: incomplete folder |
| SKILL.md only -> Full folder: behavioral | deepstream-profile-pipeline-74b92facf0e5 | SKILL.md only \| behavioral (COMPLETE) | Full folder \| behavioral (COMPLETE) | preliminary: incomplete folder |
| SKILL.md only -> Full folder: default | prd-to-ux-9d070cab6320 | SKILL.md only \| default (COMPLETE) | Full folder \| default (COMPLETE) | eligible |
| SKILL.md only -> Full folder: behavioral | prd-to-ux-9d070cab6320 | SKILL.md only \| behavioral (COMPLETE) | Full folder \| behavioral (COMPLETE) | eligible |
| SKILL.md only -> Full folder: default | ascii-motd-profile-banner-11592c159d71 | SKILL.md only \| default (COMPLETE) | Full folder \| default (COMPLETE) | eligible |
| SKILL.md only -> Full folder: behavioral | ascii-motd-profile-banner-11592c159d71 | SKILL.md only \| behavioral (COMPLETE) | Full folder \| behavioral (COMPLETE) | eligible |
| SKILL.md only -> Full folder: default | skill-author-d38487c1ec18 | SKILL.md only \| default (COMPLETE) | Full folder \| default (COMPLETE) | eligible |
| SKILL.md only -> Full folder: behavioral | skill-author-d38487c1ec18 | SKILL.md only \| behavioral (COMPLETE) | Full folder \| behavioral (COMPLETE) | eligible |
| SKILL.md only -> Full folder: default | skill-8cbbd6f03f56 | SKILL.md only \| default (COMPLETE) | Full folder \| default (COMPLETE) | preliminary: incomplete folder |
| SKILL.md only -> Full folder: behavioral | skill-8cbbd6f03f56 | SKILL.md only \| behavioral (COMPLETE) | Full folder \| behavioral (COMPLETE) | preliminary: incomplete folder |
| SKILL.md only -> Full folder: default | cross-platform-compatibility-7f7130e82a24 | SKILL.md only \| default (COMPLETE) | Full folder \| default (COMPLETE) | eligible |
| SKILL.md only -> Full folder: behavioral | cross-platform-compatibility-7f7130e82a24 | SKILL.md only \| behavioral (COMPLETE) | Full folder \| behavioral (COMPLETE) | eligible |
| SKILL.md only -> Full folder: default | qa-local-5069fa79080b | SKILL.md only \| default (COMPLETE) | Full folder \| default (COMPLETE) | eligible |
| SKILL.md only -> Full folder: behavioral | qa-local-5069fa79080b | SKILL.md only \| behavioral (COMPLETE) | Full folder \| behavioral (COMPLETE) | eligible |

_28 more row(s) in the CSV files._


## D. Scanner reliability

D1. Analyzer failures reported by Cisco

_No data._


D2. Skill folders

| skill_id | supporting_files_exported | files_missing | folder_complete | integrity |
|---|---|---|---|---|
| ascii-to-infographic-20a0a3fb5b15 | 3 | 0 | True | ok: written in this run |
| codex-counsel-7caabcfebd82 | 5 | 0 | True | ok: written in this run |
| review-l10n-22be0b42ed0e | 10 | 0 | True | ok: written in this run |
| deepstream-profile-pipeline-74b92facf0e5 | 14 | 1 | False | ok: written in this run |
| prd-to-ux-9d070cab6320 | 13 | 0 | True | ok: written in this run |
| ascii-motd-profile-banner-11592c159d71 | 1 | 0 | True | ok: written in this run |
| skill-author-d38487c1ec18 | 3 | 0 | True | ok: written in this run |
| skill-8cbbd6f03f56 | 3 | 16 | False | ok: written in this run |
| cross-platform-compatibility-7f7130e82a24 | 0 | 0 | True | ok: written in this run |
| qa-local-5069fa79080b | 0 | 0 | True | ok: written in this run |
| peak-table-row-count-validation-560112be35ae | 0 | 0 | True | ok: written in this run |
| slides-to-site-336ddf37f13f | 0 | 0 | True | ok: written in this run |


D3. Scanner verdict vs finding severity

| skill_id | configuration | outcome | is_safe | cisco_max_severity | highest_security_severity | security_findings | security_medium_or_lower | note |
|---|---|---|---|---|---|---|---|---|
| ascii-to-infographic-20a0a3fb5b15 | SKILL.md only \| default | complete | True | INFO | none | 0 | 0 | only metadata/coverage findings |
| ascii-to-infographic-20a0a3fb5b15 | SKILL.md only \| behavioral | complete | True | INFO | none | 0 | 0 | only metadata/coverage findings |
| ascii-to-infographic-20a0a3fb5b15 | Full folder \| default | complete | True | INFO | none | 0 | 0 | only metadata/coverage findings |
| ascii-to-infographic-20a0a3fb5b15 | Full folder \| behavioral | complete | True | INFO | none | 0 | 0 | only metadata/coverage findings |
| codex-counsel-7caabcfebd82 | SKILL.md only \| default | complete | True | INFO | none | 0 | 0 | only metadata/coverage findings |
| codex-counsel-7caabcfebd82 | SKILL.md only \| behavioral | complete | True | INFO | none | 0 | 0 | only metadata/coverage findings |
| codex-counsel-7caabcfebd82 | Full folder \| default | complete | True | INFO | none | 0 | 0 | only metadata/coverage findings |
| codex-counsel-7caabcfebd82 | Full folder \| behavioral | complete | True | INFO | none | 0 | 0 | only metadata/coverage findings |
| review-l10n-22be0b42ed0e | SKILL.md only \| default | complete | True | INFO | none | 0 | 0 | only metadata/coverage findings |
| review-l10n-22be0b42ed0e | SKILL.md only \| behavioral | complete | True | INFO | none | 0 | 0 | only metadata/coverage findings |
| review-l10n-22be0b42ed0e | Full folder \| default | complete | True | MEDIUM | MEDIUM | 1 | 1 | is_safe=True although there are 1 security finding(s) up to MEDIUM |
| review-l10n-22be0b42ed0e | Full folder \| behavioral | complete | True | MEDIUM | MEDIUM | 1 | 1 | is_safe=True although there are 1 security finding(s) up to MEDIUM |
| deepstream-profile-pipeline-74b92facf0e5 | SKILL.md only \| default | complete | True | SAFE | none | 0 | 0 | no findings |
| deepstream-profile-pipeline-74b92facf0e5 | SKILL.md only \| behavioral | complete | True | SAFE | none | 0 | 0 | no findings |
| deepstream-profile-pipeline-74b92facf0e5 | Full folder \| default | complete | True | SAFE | none | 0 | 0 | no findings |
| deepstream-profile-pipeline-74b92facf0e5 | Full folder \| behavioral | complete | True | SAFE | none | 0 | 0 | no findings |
| prd-to-ux-9d070cab6320 | SKILL.md only \| default | complete | True | INFO | none | 0 | 0 | only metadata/coverage findings |
| prd-to-ux-9d070cab6320 | SKILL.md only \| behavioral | complete | True | INFO | none | 0 | 0 | only metadata/coverage findings |
| prd-to-ux-9d070cab6320 | Full folder \| default | complete | True | LOW | LOW | 2 | 2 | is_safe=True although there are 2 security finding(s) up to LOW |
| prd-to-ux-9d070cab6320 | Full folder \| behavioral | complete | True | LOW | LOW | 2 | 2 | is_safe=True although there are 2 security finding(s) up to LOW |

_28 more row(s) in the CSV files._


D4. Evidence check of reported locations (counts of finding records per rule)

| rule_id | exact | mismatch | unavailable |
|---|---|---|---|
| ACTIVE_DYNAMIC_EXECUTION | 4 | 0 | 0 |
| DATA_EXFIL_JS_NETWORK | 2 | 0 | 0 |
| FILE_MAGIC_MISMATCH | 0 | 0 | 4 |
| MANIFEST_MISSING_LICENSE | 0 | 0 | 36 |
| MDBLOCK_PYTHON_SUBPROCESS | 0 | 4 | 0 |
| YARA_command_injection_generic | 0 | 4 | 0 |


## E. Manual security review

`manual_review_template.csv` lists 7 distinct security finding location(s) (0 seen only in contract-only or partial scans) with Cisco's rule, severity, reported file and line, redacted evidence and evidence check. The columns `reviewer`, `evidence_verified`, `legitimate_purpose`, `interpretation` and `notes` are intentionally blank; no finding has been labelled as a vulnerability or a false positive.


## Figures

![Security findings by Cisco category and configuration (complete scans)](../02_DETAILED_ANALYSIS/figures/findings_by_category.png)

![Severity of security findings per configuration (complete scans)](../02_DETAILED_ANALYSIS/figures/severity_by_configuration.png)

![Finding-level changes between configurations (primary analysis: complete scans)](../02_DETAILED_ANALYSIS/figures/configuration_comparisons.png)


## Limitations

- 2 skill folder(s) are incomplete in GitSkills (17 supporting file(s) without stored text). This is a design exclusion, not a scanner failure: 0 of 48 planned configuration(s) (their full-folder scans) were not run, so 48 Cisco scans were executed. Their SKILL.md-only scans are kept, but their context-comparison pairs are reported as `excluded: incomplete folder`, and no finding count of zero is implied for the excluded configurations.
- 8 of 54 finding record(s) do not have their evidence on the reported line (mismatch 8, ambiguous 0); rules involved: YARA_command_injection_generic (4), MDBLOCK_PYTHON_SUBPROCESS (4). Reported line numbers are kept unchanged.
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
