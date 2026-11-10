# Cisco Skill Scanner results: `2026-11-03_153301_pilot-loa-credentials`

Generated automatically by `notebooks/01_cisco_scanner_dataset_ready.ipynb` on 2026-11-03T23:33:13+00:00. Every number below is computed from the files in this run folder. A finding is a Cisco rule match on an operation, not a confirmed vulnerability.

## A. Experiment overview

| item | value |
|---|---|
| Run ID | 2026-11-03_153301_pilot-loa-credentials |
| Run mode | scan (Cisco executed in this run) |
| Dataset | agent_skills_sample.db (SHA-256 683888c923a5...) |
| Scanner version that produced the reports | skill-scanner 2.3.1 |
| Scan policy (name / preset) | default / balanced |
| Policy fingerprint(s) | 3f48e661bfbc... |
| Scans executed (report timestamps, UTC) | 2026-11-03 23:33:04 to 2026-11-03 23:33:13 |
| Analysis written | 2026-11-03T23:33:13+00:00 |
| Skills selected / exported | 1 / 1 |
| Skill folders complete / incomplete | 1 / 0 |
| Configurations per skill | 4 |
| Configuration runs attempted | 4 |
| Outcomes | complete: 4, contract_only: 0, partial: 0, failed: 0, skipped: 0, missing: 0 |
| Finding records (all readable reports) | 4 (complete scans: 4, contract-only scans: 0, partial scans: 0) |
| Security finding records in complete scans | 0 |
| Distinct rule/location combinations (skill, rule, file, line), all findings | 1 |
| Distinct rule/location combinations, security findings in complete scans | 0 |


Scan outcomes per configuration (complete = primary results; contract_only = only Cisco's known rule-registration error, used in the sensitivity analysis only; partial = other analyzer problems, preliminary only):

| configuration | complete | contract_only | partial | failed | skipped | missing |
|---|---|---|---|---|---|---|
| SKILL.md only \| default | 1 | 0 | 0 | 0 | 0 | 0 |
| SKILL.md only \| behavioral | 1 | 0 | 0 | 0 | 0 | 0 |
| Full folder \| default | 1 | 0 | 0 | 0 | 0 | 0 |
| Full folder \| behavioral | 1 | 0 | 0 | 0 | 0 | 0 |


## B. Security findings (complete scans only)

B1. Findings by severity

_No data._


B2. Findings by Cisco category (per configuration) and distinct skills affected (any complete configuration)

_No data._


B3. Findings by research category (our mapping; categories without Cisco rules stay at zero)

_No data._


B4. Most frequently triggered security rules

_No data._


B5. Where the findings point

_No data._


B6. Findings outside the primary group: contract-only and partial scans (excluded from B1-B5)

_No data._


## C. Configuration comparisons

The **primary analysis** uses only pairs in which both scans are COMPLETE (and, for SKILL.md-only vs full-folder, the folder is complete). The **sensitivity analysis** adds pairs that contain a CONTRACT_ONLY scan. Contract-only scans are not assumed complete or accurate; the sensitivity analysis only shows whether including them would change a result.

C1. Sample sizes and excluded pairs per comparison (`excluded_*` = pairs left out of the primary analysis, by reason; contract-only pairs are added back in the sensitivity analysis)

| comparison | pairs_total | primary_n | sensitivity_n | excluded_contract_only | excluded_partial | excluded_incomplete_folder | excluded_not_comparable |
|---|---|---|---|---|---|---|---|
| SKILL.md only -> Full folder: default | 1 | 1 | 1 | 0 | 0 | 0 | 0 |
| SKILL.md only -> Full folder: behavioral | 1 | 1 | 1 | 0 | 0 | 0 | 0 |
| default -> behavioral: SKILL.md only | 1 | 1 | 1 | 0 | 0 | 0 | 0 |
| default -> behavioral: Full folder | 1 | 1 | 1 | 0 | 0 | 0 | 0 |


C2. Primary analysis (complete scans only): finding-level changes summed over the pairs used

| comparison | pairs_used | pairs_with_findings | unchanged | changed | possibly_equivalent | additional | missing | skills_with_additional |
|---|---|---|---|---|---|---|---|---|
| SKILL.md only -> Full folder: default | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| SKILL.md only -> Full folder: behavioral | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| default -> behavioral: SKILL.md only | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| default -> behavioral: Full folder | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |


C3. Files that contribute the additional findings in the primary SKILL.md-only vs full-folder comparison (a SKILL.md row means Cisco re-read the instructions once the scripts were present)

_No data._


C4. Sensitivity analysis (complete + contract-only scans): finding-level changes summed over the pairs used

| comparison | pairs_used | pairs_with_findings | unchanged | changed | possibly_equivalent | additional | missing | skills_with_additional |
|---|---|---|---|---|---|---|---|---|
| SKILL.md only -> Full folder: default | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| SKILL.md only -> Full folder: behavioral | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| default -> behavioral: SKILL.md only | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| default -> behavioral: Full folder | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |


C5. Does including contract-only scans change the comparisons?

- SKILL.md only -> Full folder: default: no contract-only pairs, so the sensitivity analysis equals the primary analysis (n = 1).
- SKILL.md only -> Full folder: behavioral: no contract-only pairs, so the sensitivity analysis equals the primary analysis (n = 1).
- default -> behavioral: SKILL.md only: no contract-only pairs, so the sensitivity analysis equals the primary analysis (n = 1).
- default -> behavioral: Full folder: no contract-only pairs, so the sensitivity analysis equals the primary analysis (n = 1).

C6. Pair status per skill

| comparison | before | after | pair_status |
|---|---|---|---|
| SKILL.md only -> Full folder: default | SKILL.md only \| default (COMPLETE) | Full folder \| default (COMPLETE) | eligible |
| SKILL.md only -> Full folder: behavioral | SKILL.md only \| behavioral (COMPLETE) | Full folder \| behavioral (COMPLETE) | eligible |
| default -> behavioral: SKILL.md only | SKILL.md only \| default (COMPLETE) | SKILL.md only \| behavioral (COMPLETE) | eligible |
| default -> behavioral: Full folder | Full folder \| default (COMPLETE) | Full folder \| behavioral (COMPLETE) | eligible |


## D. Scanner reliability

D1. Analyzer failures reported by Cisco

_No data._


D2. Skill folders

| skill_id | supporting_files_exported | files_missing | folder_complete | integrity |
|---|---|---|---|---|
| managing-credentials-46aa89b2bc87 | 1 | 0 | True | ok: written in this run |


D3. Scanner verdict vs finding severity

| configuration | outcome | is_safe | cisco_max_severity | highest_security_severity | security_findings | security_medium_or_lower | note |
|---|---|---|---|---|---|---|---|
| SKILL.md only \| default | complete | True | INFO | none | 0 | 0 | only metadata/coverage findings |
| SKILL.md only \| behavioral | complete | True | INFO | none | 0 | 0 | only metadata/coverage findings |
| Full folder \| default | complete | True | INFO | none | 0 | 0 | only metadata/coverage findings |
| Full folder \| behavioral | complete | True | INFO | none | 0 | 0 | only metadata/coverage findings |


D4. Evidence check of reported locations (counts of finding records per rule)

| rule_id | unavailable |
|---|---|
| MANIFEST_MISSING_LICENSE | 4 |


## E. Manual security review

`manual_review_template.csv` lists 0 distinct security finding location(s) (0 seen only in contract-only or partial scans) with Cisco's rule, severity, reported file and line, redacted evidence and evidence check. The columns `reviewer`, `evidence_verified`, `legitimate_purpose`, `interpretation` and `notes` are intentionally blank; no finding has been labelled as a vulnerability or a false positive.


## Limitations

- 4 finding record(s) could not be checked against the file (no file, line or evidence text).
- Only 1 skill(s) were analysed: these are pilot observations, not population estimates.
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
