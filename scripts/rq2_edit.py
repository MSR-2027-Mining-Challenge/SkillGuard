#!/usr/bin/env python3
"""Record preliminary RQ2 defect investigations in the EXISTING candidate CSV.

This tool records only status/impact/fix/investigation notes for selected candidate IDs.
It does not execute any sampled skills.

Examples (run from SkillGuard repo root):
  python scripts/rq2_edit.py --ids 4d63af1de0d3
  python scripts/rq2_edit.py --ids c98b2f262d99 7294e718de72
  python scripts/rq2_edit.py --ids 4d63af1de0d3 --set candidate_status=false_positive \\
    --set 'investigation_notes=The text is not a filesystem path.'

To remove obsolete review columns from earlier CSV versions (with a backup):
  python scripts/rq2_edit.py --clean-legacy-columns
"""

from __future__ import annotations

import argparse
import csv
import os
import re
from pathlib import Path
import shutil
import sys
import tempfile

DEFAULT_CSV = Path("results/rq2/seed2027_defect_screening/rq2_defect_candidates.csv")
PRELIMINARY_FIELDS = (
    "candidate_status",
    "impact",
    "recommended_fix",
    "investigation_notes",
)
def legacy_column(name: str) -> bool:
    """Legacy multi-person fields are not used by this RQ2 workflow."""
    return bool(re.fullmatch(r"reviewer_[0-9]+(?:_.*)?|final_label|final_rationale|adjudicated_by", name))
STATUS_SUGGESTIONS = (
    "candidate", "confirmed_in_snapshot", "confirmed_defect", "likely_false_positive",
    "false_positive", "unresolved", "not_evaluable",
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--csv", default=str(DEFAULT_CSV), help="Existing RQ2 candidates CSV")
    parser.add_argument("--ids", nargs="+", help="One or more candidate_id values")
    parser.add_argument(
        "--set", dest="edits", action="append", default=[], metavar="FIELD=VALUE",
        help="Set a field directly, rather than answering interactive prompts (repeatable)",
    )
    parser.add_argument(
        "--clean-legacy-columns", action="store_true",
        help="Drop unused legacy review columns from the CSV (creates a backup)",
    )
    parser.add_argument("--yes", action="store_true", help="Skip save confirmation")
    args = parser.parse_args()

    path = Path(args.csv).expanduser().resolve()
    if not path.is_file():
        print(f"ERROR: CSV not found: {path}", file=sys.stderr)
        return 2
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            fieldnames = list(reader.fieldnames or [])
            rows = list(reader)
    except (OSError, csv.Error) as error:
        print(f"ERROR: Could not read CSV: {error}", file=sys.stderr)
        return 2

    if "candidate_id" not in fieldnames:
        print("ERROR: This file has no candidate_id column.", file=sys.stderr)
        return 2
    if "candidate_status" not in fieldnames:
        print("ERROR: This is not the expected RQ2 candidate CSV (missing candidate_status).", file=sys.stderr)
        return 2

    if not args.ids and not args.clean_legacy_columns:
        print("ERROR: Provide --ids or --clean-legacy-columns.", file=sys.stderr)
        return 2
    requested = list(dict.fromkeys(args.ids or []))
    selected = [r for r in rows if r.get("candidate_id") in requested]
    missing = set(requested) - {r["candidate_id"] for r in selected}
    if missing:
        print(f"ERROR: Unknown ID(s): {', '.join(sorted(missing))}. No changes made.", file=sys.stderr)
        return 2

    # Parse before mutating the file; reject dangerous/unexpected field names.
    changes: dict[str, str] = {}
    for item in args.edits:
        if "=" not in item:
            print(f"ERROR: Use --set FIELD=VALUE, not {item!r}", file=sys.stderr)
            return 2
        column, value = item.split("=", 1)
        column = column.strip()
        if column not in PRELIMINARY_FIELDS:
            print(f"ERROR: Field {column!r} is not editable. Allowed: {', '.join(PRELIMINARY_FIELDS)}", file=sys.stderr)
            return 2
        changes[column] = value

    print(f"\nFile: {path}")
    print(f"Selected {len(selected)} candidate(s):")
    for row in selected:
        print(f"  {row['candidate_id']}  {row.get('skill_id', '')}  {row.get('rule_id', '')}  "
              f"{row.get('file_path', '')}:{row.get('line_number', '')}")
    print("\nThis records preliminary RQ2 researcher assessments.")

    old_columns = [col for col in fieldnames if legacy_column(col)] if args.clean_legacy_columns else []
    if args.clean_legacy_columns:
        print("Unused legacy columns to remove:", ", ".join(old_columns) or "none")
    if not args.edits and not args.clean_legacy_columns:
        print("\nEnter findings. Press ENTER to keep the existing value.")
        print("Status suggestions: " + ", ".join(STATUS_SUGGESTIONS))
        print("Use 'investigation_notes' for evidence, rationale, and uncertainties.\n")
        for column in PRELIMINARY_FIELDS:
            current = selected[0].get(column, "")
            if any(r.get(column, "") != current for r in selected):
                current = "<different across selected IDs>"
            hint = current[:80] + ("..." if len(current) > 80 else "")
            try:
                value = input(f"{column}{' [' + hint + ']' if hint else ''}: ")
            except (EOFError, KeyboardInterrupt):
                print("\nCancelled; no changes saved.")
                return 1
            if value.strip():
                changes[column] = value

    if not changes and not old_columns:
        print("Nothing changed.")
        return 0

    if changes.get("candidate_status") and changes["candidate_status"] not in STATUS_SUGGESTIONS:
        print("NOTE: status is custom; suggested statuses: " + ", ".join(STATUS_SUGGESTIONS))

    print("\nUpdates to every selected candidate:")
    for column, value in changes.items():
        print(f"  {column} = {value}")
    if old_columns:
        print("  Remove unused legacy columns: " + ", ".join(old_columns))

    if not args.yes:
        try:
            answer = input("\nSave to this CSV? [y/N]: ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\nCancelled; no changes saved.")
            return 1
        if answer not in ("y", "yes"):
            print("Cancelled; no changes saved.")
            return 0

    # Keep scanner-produced columns and researcher notes. Remove obsolete
    # multi-person review schema only when explicitly requested.
    if "investigation_notes" in changes and "investigation_notes" not in fieldnames:
        fieldnames.append("investigation_notes")
    for row in rows:
        if row.get("candidate_id") in requested:
            row.update(changes)
    if old_columns:
        fieldnames = [column for column in fieldnames if column not in old_columns]
        for row in rows:
            for column in old_columns:
                row.pop(column, None)

    # Backup the original and atomically replace it in the same directory.
    backup = path.with_name(path.name + ".bak")
    tmp_path = None
    try:
        shutil.copy2(path, backup)
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", newline="", dir=path.parent,
            prefix="." + path.name + ".", suffix=".tmp", delete=False,
        ) as f:
            tmp_path = Path(f.name)
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(rows)
        os.replace(tmp_path, path)
    finally:
        if tmp_path is not None:
            tmp_path.unlink(missing_ok=True)

    print(f"\nSaved {len(selected)} candidate(s) in: {path}")
    print(f"Backup: {backup}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
