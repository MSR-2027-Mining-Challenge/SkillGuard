# Human validation status
Three tiers are kept strictly apart in every table of this report:
1. **Scanner alert**: Cisco reported it. Nothing more is known.
2. **Provisional**: a researcher-approved, AI-assisted label (`provisional_label`). Useful for triage, but **not** an independent human review, and never reported as validated.
3. **Human-validated**: `final_label` is filled and `adjudicated_by` names the adjudicator.
| tier | distinct alert locations |
|---|---|
| Human-validated | 0 |
| Provisional label (AI-assisted, not independent human review) | 0 |
| Scanner alert, awaiting human review | 22 |
| Scanner alert, not in the review queue | 0 |
No manual-review worksheet exists for this run yet. Create one with `notebooks/04_manual_review_worksheet.ipynb`.
