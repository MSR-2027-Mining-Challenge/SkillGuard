# MalSkills — 1,000-skill analysis (`package_test_2`)

## Corpus and verdicts
- Scan rows: **1,000**
- Distinct entry IDs: **1,000**
- Malicious verdicts: **4/1,000 (0.40%)**
- Benign verdicts: **996**
- Failed/non-OK rows: **0**
- Skills with >=1 SSO: **271**
- Skills with matched behavior patterns: **4**
- Skills with SSOs but no matched pattern: **267**
- Preserved case directories: **1,000**

## Four flagged cases
- `skill_0050`: SSOs=17, matched patterns=Malware_Delivery, Remote_Code_Execution
- `skill_0452`: SSOs=20, matched patterns=Malware_Delivery, Remote_Code_Execution
- `skill_0636`: SSOs=31, matched patterns=Malware_Delivery, Remote_Code_Execution
- `skill_0964`: SSOs=10, matched patterns=Malware_Delivery, Remote_Code_Execution

## Observed MalSkills detection pattern
Malicious verdicts correspond to matched MalSkills behavior patterns rather than merely high SSO counts.
See pattern_proofs.csv and flagged_case_study.csv for the rules and source-linked evidence.

Input directory: `/Users/samantharies/PycharmProjects/MSR2027/SkillGuard/results/malskills/package_test_2`
