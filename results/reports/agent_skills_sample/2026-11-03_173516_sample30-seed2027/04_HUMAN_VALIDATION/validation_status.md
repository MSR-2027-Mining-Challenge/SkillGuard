# Human validation status
Three tiers are kept strictly apart in every table of this report:
1. **Scanner alert**: Cisco reported it. Nothing more is known.
2. **Provisional**: a researcher-approved, AI-assisted label (`provisional_label`). Useful for triage, but **not** an independent human review, and never reported as validated.
3. **Human-validated**: `final_label` is filled and `adjudicated_by` names the adjudicator.
| tier | distinct alert locations |
|---|---|
| Human-validated | 0 |
| Provisional label (AI-assisted, not independent human review) | 11 |
| Scanner alert, awaiting human review | 0 |
| Scanner alert, not in the review queue | 0 |
Worksheet: `results/manual_review/sample30-seed2027` (worksheet was generated from this run). 11 review items: Provisional label (AI-assisted, not independent human review) 11.
Provisional labels: intentional 5, scanner_parser_issue 4, uncertain 2.
Final human labels: none yet.
`snapshots/` holds redacted copies of the worksheet files as they were when this report was built (hashes in `report_manifest.json`). Edit the originals in `results/manual_review/`, never the snapshots, then rebuild.
