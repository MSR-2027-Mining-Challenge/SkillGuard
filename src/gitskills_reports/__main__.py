"""python -m gitskills_reports [--run RUN_FOLDER | --combined FOLDER | --all] [--out DIR]   (run from the repository root
with src on PYTHONPATH). Without arguments it rebuilds every report and the index."""

import argparse
from pathlib import Path

from .build import build_all, build_report, refresh_index
from .redaction import Portable
from .model import find_root, load_combined, load_run

parser = argparse.ArgumentParser(prog="gitskills_reports")
parser.add_argument("--run", help="one run folder (relative to the repository root or absolute)")
parser.add_argument("--combined", help="one notebook-02 combined report folder")
parser.add_argument("--out", help="output root (default results/reports)")
args = parser.parse_args()

root = find_root()
out = Path(args.out).resolve() if args.out else root / "results" / "reports"
if args.run or args.combined:
    folder = (root / (args.run or args.combined)).resolve()
    source = load_run(folder) if args.run else load_combined(folder, root)
    print("built", Portable(root).path(build_report(source, root, out)))
    refresh_index(root, out)
else:
    build_all(root, out, log=lambda msg: print(msg))
    print("index:", Portable(root).path(out / "index.html"))
