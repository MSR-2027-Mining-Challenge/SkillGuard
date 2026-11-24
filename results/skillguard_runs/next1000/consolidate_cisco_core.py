"""Copy the Cisco core results of the next1000 batches into the tracked results tree, lockbox-split.

Notebook 01 writes its tables to results/cisco_dataset_runs/.../runs/<run>/ (local, untracked: the folder
also holds the exported skills and raw reports). For traceability this script writes, per run,
next1000/cisco_core/<run>/{scans.csv, findings.csv} (+ sealed/ for lockbox skills, SHA256SUMS), with
the columns needed for analysis. Snippets, descriptions and raw metadata are left out: they quote
untrusted skill content and can contain secrets. Paths are kept repo-relative.

    .venv/bin/python -I results/skillguard_runs/next1000/consolidate_cisco_core.py <run_dir> [<run_dir> ...]
"""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import HERE, reset_sealed, write_split  # noqa: E402

SCAN_COLS = ["skill_id", "sample_stratum", "configuration", "status", "outcome", "status_detail", "analyzers_failed",
             "max_severity", "findings_count", "folder_complete", "files_missing", "frontmatter_valid",
             "scanner_version", "policy_name", "wall_seconds"]
FINDING_COLS = ["skill_id", "sample_stratum", "configuration", "finding_kind", "rule_id", "cisco_category",
                "research_category", "severity", "analyzer", "title", "file_path", "reported_line_number",
                "meta_from_code_block", "meta_block_language"]


def rows(path):
    with path.open(encoding="utf-8", newline="") as h:  # a few reports contain NUL bytes from skill content
        return list(csv.DictReader(line.replace("\0", "") for line in h))


def main():
    for run in (Path(a).resolve() for a in sys.argv[1:]):
        out = HERE / "cisco_core" / run.name
        out.mkdir(parents=True, exist_ok=True)
        reset_sealed(out)
        scans = [{c: r.get(c, "") for c in SCAN_COLS} for r in rows(run / "scan_summary.csv")]
        finds = []
        for r in rows(run / "individual_findings.csv"):
            row = {c: r.get(c, "") for c in FINDING_COLS}
            if row["file_path"].startswith("/"):  # absolute paths only occur for files outside the skill folder
                row["file_path"] = "<absolute path outside skill folder>"
            finds.append(row)
        counts = {"scans": write_split(out, "scans", scans), "findings": write_split(out, "findings", finds)}
        (out / "summary.json").write_text(json.dumps({"run": run.name, "rows_open_sealed": counts}, indent=2) + "\n")
        print(run.name, counts)


if __name__ == "__main__":
    main()
