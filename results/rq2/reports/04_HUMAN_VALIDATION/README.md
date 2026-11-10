# Human validation

Only the researcher assessment fields are used: status, impact, fix and notes.
No status is assigned by this reporting pipeline. To edit source labels, use:

`python scripts/rq2_edit.py --ids <candidate-id>`

`orphaned_previous_annotations.csv` records human annotations from the prior run whose IDs were not regenerated.
