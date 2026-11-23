"""Shared helpers for the next 1,000-skill experiment runners (no skill content is executed)."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
LOCKBOX = HERE / "manifests/lockbox_skill_ids.csv"


def lockbox_ids():
    return {r["skill_id"] for r in csv.DictReader(LOCKBOX.open(encoding="utf-8"))}


def skill_dirs(run_dir):
    """[(skill_id, full_folder)] for a notebook-01 run folder (only skills with an exported full folder)."""
    run = Path(run_dir)
    return [(p.parent.name, p) for p in sorted(run.glob("*/full")) if (p.parent / "manifest.json").is_file()]


def folder_digest(folder):
    """sha256 over sorted 'relative_path\\0sha256(bytes)' lines: detects any change to a folder."""
    lines = []
    for p in sorted(Path(folder).rglob("*")):
        if p.is_file() and not p.is_symlink():
            lines.append(f"{p.relative_to(folder).as_posix()}\0{hashlib.sha256(p.read_bytes()).hexdigest()}")
    return hashlib.sha256("\n".join(lines).encode()).hexdigest()


def write_csv(path, rows, fields=None):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = fields or (list(rows[0].keys()) if rows else ["empty"])
    with path.open("w", newline="", encoding="utf-8") as h:
        w = csv.DictWriter(h, fieldnames=fields, lineterminator="\n", extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow({k: json.dumps(v, ensure_ascii=False) if isinstance(v, (list, dict)) else v for k, v in r.items()})
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_split(out_dir, name, rows, key="skill_id"):
    """Write open rows to <out>/<name>.csv and lockbox rows to <out>/sealed/<name>.csv.

    The sealed files are for post-freeze evaluation only (LOCKBOX_POLICY.md); their sha256 is
    recorded in <out>/sealed/SHA256SUMS so later tampering or early edits are detectable."""
    sealed = lockbox_ids()
    open_rows = [r for r in rows if r[key] not in sealed]
    lock_rows = [r for r in rows if r[key] in sealed]
    fields = list(rows[0].keys()) if rows else ["empty"]
    write_csv(Path(out_dir) / f"{name}.csv", open_rows, fields)
    digest = write_csv(Path(out_dir) / "sealed" / f"{name}.csv", lock_rows, fields)
    with (Path(out_dir) / "sealed" / "SHA256SUMS").open("a", encoding="utf-8") as h:
        h.write(f"{digest}  {name}.csv\n")
    return len(open_rows), len(lock_rows)


def reset_sealed(out_dir):
    """Start a fresh sealed/SHA256SUMS for a (re)run of a runner into out_dir."""
    (Path(out_dir) / "sealed" / "SHA256SUMS").unlink(missing_ok=True)
