"""Verify that a notebook-01 export is byte-identical to the GitSkills DB and write folder manifests.

    .venv/bin/python -I results/skillguard_runs/next1000/verify_export.py <cisco_run_dir>

For every skill folder <run>/<skill_id>/full (and its manifest.json written by notebook 01):
  * every exported file is compared with the DB text (SKILL.md: artifacts.content;
    others: artifact_siblings.content), encoded as UTF-8 -> must be byte-identical;
  * files listed in the DB without stored text are recorded as missing;
  * a truncated listing (composition_truncated) is recorded as "missing count unknown";
  * a folder digest (common.folder_digest) is recorded so every scanner run can prove that it saw
    exactly these bytes and did not modify them.
Outputs: next1000/exports/<run_id>/folder_manifests.jsonl, export_summary.csv, summary.json.
The DB is opened read-only.
"""

from __future__ import annotations

import hashlib
import json
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # python -I does not add the script folder
from common import HERE, REPO, folder_digest, skill_dirs, write_csv

DB = REPO / "data/sample/agent_skills_sample.db"


def main():
    run = Path(sys.argv[1]).resolve()
    con = sqlite3.connect(DB.as_uri() + "?mode=ro", uri=True)
    con.execute("PRAGMA query_only = ON")
    out = HERE / "exports" / run.name
    out.mkdir(parents=True, exist_ok=True)
    rows, problems = [], 0
    with (out / "folder_manifests.jsonl").open("w", encoding="utf-8") as h:
        for skill_id, folder in skill_dirs(run):
            meta = json.loads((folder.parent / "manifest.json").read_text(encoding="utf-8"))
            repo, spath = meta["repo"], meta["skill_path"]
            art = con.execute("SELECT content, composition_truncated FROM artifacts WHERE repo_full_name=? AND path=?",
                              (repo, spath)).fetchone()
            sibs = {name: content for name, content, etype in con.execute(
                "SELECT entry_name, content, entry_type FROM artifact_siblings WHERE repo_full_name=? AND artifact_path=?",
                (repo, spath)) if etype == "file"}
            files, mismatches = [], []
            exported = {p.relative_to(folder).as_posix(): p for p in folder.rglob("*") if p.is_file()}
            for rel, path in sorted(exported.items()):
                data = path.read_bytes()
                expected = art[0] if rel == "SKILL.md" else sibs.get(rel)
                same = expected is not None and expected.encode("utf-8") == data
                if not same:
                    mismatches.append(rel)
                files.append({"path": rel, "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data),
                              "matches_db": same})
            missing = sorted(n for n, c in sibs.items() if c is None and n not in exported and n != "SKILL.md")
            record = {"skill_id": skill_id, "repo": repo, "skill_path": spath, "folder_digest": folder_digest(folder),
                      "files": files, "files_listed_without_text": missing,
                      "listing_truncated": bool(art[1]) if art else None,
                      "missing_count": "unknown" if art and art[1] else len(missing),
                      "byte_mismatches": mismatches}
            h.write(json.dumps(record, ensure_ascii=False) + "\n")
            problems += bool(mismatches)
            rows.append({"skill_id": skill_id, "files_exported": len(files), "files_missing_text": len(missing),
                         "listing_truncated": record["listing_truncated"], "missing_count": record["missing_count"],
                         "byte_mismatches": len(mismatches), "folder_digest": record["folder_digest"]})
    write_csv(out / "export_summary.csv", rows)
    summary = {"run": run.name, "skills": len(rows), "skills_with_byte_mismatch": problems,
               "skills_with_missing_files": sum(r["files_missing_text"] > 0 for r in rows),
               "skills_with_truncated_listing": sum(bool(r["listing_truncated"]) for r in rows),
               "files_exported": sum(r["files_exported"] for r in rows)}
    (out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
