"""Cisco skill-scanner (static) on the held-out skills, same args as the Nov-3 baseline.

    .venv/bin/python -I results/skillguard_runs/heldout/run_cisco_heldout.py <heldout_dir> [folder_glob]

Full-folder configurations only: default and --use-behavioral, policy balanced.
skill-scanner performs static analysis; skill code is not executed. Reports go to
<heldout_dir> [folder_glob]/cisco/<set>/<skill_id>/full_folder_<mode>.json (+ .run.json).
"""

import datetime as dt
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
SCANNER = REPO / ".venv/bin/skill-scanner"
MODES = {"default": [], "behavioral": ["--use-behavioral"]}


def main():
    root = Path(sys.argv[1]).resolve()
    folders = sorted(root.glob(sys.argv[2] if len(sys.argv) > 2 else "H*_*/*/full"))
    for i, full in enumerate(folders, 1):
        set_name, skill = full.parent.parent.name, full.parent.name
        dest = root / "cisco" / set_name / skill
        dest.mkdir(parents=True, exist_ok=True)
        for mode, extra in MODES.items():
            report = dest / f"full_folder_{mode}.json"
            if report.exists():
                continue
            cmd = [str(SCANNER), "scan", str(full), "--format", "json", "--policy", "balanced", *extra]
            start = time.time()
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
            report.write_text(proc.stdout, encoding="utf-8")
            (dest / f"full_folder_{mode}.run.json").write_text(json.dumps({
                "command": cmd, "exit_code": proc.returncode, "wall_seconds": round(time.time() - start, 2),
                "started_at": dt.datetime.fromtimestamp(start).astimezone().isoformat(),
                "stderr_tail": proc.stderr[-2000:],
                "report_sha256": hashlib.sha256(proc.stdout.encode()).hexdigest()}, indent=2), encoding="utf-8")
        print(f"[{i}/{len(folders)}] {set_name}/{skill}", flush=True)


if __name__ == "__main__":
    main()
