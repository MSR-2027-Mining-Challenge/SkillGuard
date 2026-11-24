"""One-time remediation (2026-11-23): move lockbox rows of already-written scans.csv tables to sealed/.

The Cisco+ATR and MalSkills runners originally wrote per-skill scan statuses (and MalSkills verdicts)
for all skills to the open scans.csv. They now use write_split; this script applies the same split to
the outputs written before that change. Rows are moved, not changed: open + sealed == original rows.

    .venv/bin/python -I results/skillguard_runs/next1000/seal_scan_tables.py
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import HERE, lockbox_ids, write_split  # noqa: E402


def main():
    sealed = lockbox_ids()
    targets = sorted(HERE.glob("cisco_atr/*/scans.csv")) + sorted(HERE.glob("malskills/*/scans.csv"))
    for scans in targets:
        original = scans.read_bytes()
        rows = list(csv.DictReader(scans.open(encoding="utf-8")))
        n_lock = sum(r["skill_id"] in sealed for r in rows)
        if n_lock == 0:
            print(f"{scans.relative_to(HERE)}: no lockbox rows")
            continue
        if (scans.parent / "sealed" / "scans.csv").exists():
            raise SystemExit(f"{scans}: sealed/scans.csv already exists")
        write_split(scans.parent, "scans", rows)
        back = list(csv.DictReader(scans.open(encoding="utf-8"))) + \
            list(csv.DictReader((scans.parent / "sealed" / "scans.csv").open(encoding="utf-8")))
        key = lambda r: r["skill_id"]
        if sorted(back, key=key) != sorted(rows, key=key):
            scans.write_bytes(original)
            raise SystemExit(f"{scans}: split changed rows; restored original")
        print(f"{scans.relative_to(HERE)}: moved {n_lock} lockbox rows to sealed/")


if __name__ == "__main__":
    main()
