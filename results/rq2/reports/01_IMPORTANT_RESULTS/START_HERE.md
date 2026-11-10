# RQ2 — Start here

**All scanner output consists of candidates, not confirmed defects.**

- **70** candidate locations; **16** rules triggered; **24** skills flagged.
- **26** candidate statuses annotated by researchers; **44** remain unassessed.
- Source: `results/cisco_dataset_runs/agent_skills_sample/runs/2026-11-09_135034_sam-sample30-seed2027`

## Status summary

| Status | Count |
|---|---:|
| candidate | 44 |
| confirmed_defect | 1 |
| confirmed_in_snapshot | 12 |
| false_positive | 7 |
| likely_false_positive | 4 |
| unresolved | 2 |

## Rule summary

| Rule | Locations | Skills | Annotated |
|---|---:|---:|---:|
| P1 | 9 | 4 | 9 |
| P4 | 8 | 3 | 8 |
| P5 | 1 | 1 | 1 |
| R1.2 | 1 | 1 | 0 |
| R1.5 | 8 | 8 | 0 |
| R2.1 | 3 | 3 | 0 |
| R2.4 | 13 | 13 | 0 |
| R2.5 | 1 | 1 | 0 |
| R3.1 | 4 | 4 | 0 |
| R3.2 | 10 | 10 | 0 |
| R3.3 | 2 | 2 | 0 |
| R4.2 | 1 | 1 | 0 |
| R4.4 | 1 | 1 | 0 |
| R6.4 | 3 | 2 | 3 |
| S2 | 3 | 3 | 3 |
| S3 | 2 | 2 | 2 |

## Interpretation

Counts represent flagged locations, not unique defects or independently validated failures. Auto-triage hints are not scientific labels. Missing exported resources may be outside the folder, and multi-location warnings may refer to the same underlying issue.

Open `../02_DETAILED_ANALYSIS/candidate_review_queue.csv` for the review queue.
