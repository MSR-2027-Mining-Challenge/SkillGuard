"""Build the list of previously used skills to exclude from the next 1,000-skill sample.

    .venv/bin/python -I results/skillguard_runs/next1000/build_exclusions.py

Identity = the DB's SKILL.md content identity ``file_sha`` (one representative per file_sha, the
sampling unit of notebook 03). Sources:
  * results/samples/*/sample_manifest.csv (seed 2027 and seed 2030 samples): file_sha column;
  * results/skillguard_runs/heldout/*/sample_manifest.csv (seed 2028 H1/H2, seed 2029 R100);
  * notebook 01 pilot / keyword selections (repo + path) -> file_sha via the DB;
  * the two MalSkills samples on branch origin/rio (package_test_1: 100, package_test_2: 1,000).
    They list only sha256 of the exported SKILL.md, which was written with Windows newline
    translation. Each value is matched against sha256 of the DB content under these
    normalizations (recorded per entry): as stored, LF->CRLF, CRLF->LF, Windows text-mode translation (\n -> \r\n
    applied to text that may already contain CRLF), plus trailing-newline
    and BOM variants. Unmatched entries are written to unresolved.csv and reported; they cannot
    be excluded without the folder mapping (skill_mapping.csv), which is not in the repository.
The DB is opened read-only. Outputs (overwritten deterministically; inputs are fixed):
  exclusions/excluded_file_shas.csv, exclusions/unresolved.csv, exclusions/summary.json
"""

from __future__ import annotations

import csv
import hashlib
import json
import sqlite3
import subprocess
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
DB = REPO / "data/sample/agent_skills_sample.db"
RIO_REF = "origin/rio"
RIO_MANIFESTS = {"malskills_package_test_1": "results/malskills/package_test_1/sample_manifest.json",
                 "malskills_package_test_2": "results/malskills/package_test_2/sample_manifest.json"}
PILOTS = {  # notebook 01 PILOTS and the keyword batch from notebook 03 PREVIOUS_SELECTIONS
    "pilot canary-tokens": ("26zl/cybersec-toolkit", ".claude/skills/implementing-canary-tokens-for-network-intrusion/SKILL.md"),
    "pilot x": ("AceDataCloud/Skills", "skills/x/SKILL.md"),
    "pilot loa-credentials": ("0xHoneyJar/loa-dixie", ".claude/skills/managing-credentials/SKILL.md"),
    "keyword batch API_KEY #1": ("0xHoneyJar/loa-constructs", ".claude/skills/bridgebuilder-review/SKILL.md"),
    "keyword batch API_KEY #3": ("1CestlaVie/astrbot-plugin-dev-skill", "SKILL.md"),
}


def variants(text):
    lf = text.replace("\r\n", "\n")
    crlf = lf.replace("\n", "\r\n")
    # Windows text-mode writing translates every "\n" to "\r\n", so text that already had CRLF
    # becomes "\r\r\n" ("windows_translation").
    out = {"as_stored": text, "lf_to_crlf": crlf, "crlf_to_lf": lf, "windows_translation": text.replace("\n", "\r\n")}
    for name, v in list(out.items()):
        out[name + "+bom"] = "﻿" + v
        out[name + "+strip_trailing"] = v.rstrip("\r\n")
        out[name + "+trailing_newline"] = v if v.endswith("\n") else v + ("\r\n" if "\r\n" in v else "\n")
    return out


def main():
    con = sqlite3.connect(DB.as_uri() + "?mode=ro", uri=True)
    con.execute("PRAGMA query_only = ON")
    db_sha = hashlib.sha256(DB.read_bytes()).hexdigest()
    sources = defaultdict(set)   # file_sha -> {source}
    methods = {}
    # 1. tracked sample manifests
    for path in sorted((REPO / "results/samples").glob("*/sample_manifest.csv")) + \
            sorted((REPO / "results/skillguard_runs/heldout").glob("*/sample_manifest.csv")):
        for row in csv.DictReader(path.open(encoding="utf-8")):
            sources[row["file_sha"]].add(path.parent.name)
            methods.setdefault(row["file_sha"], "manifest_file_sha")
    # 2. pilots by repo + path
    for label, (repo, spath) in PILOTS.items():
        row = con.execute("SELECT file_sha FROM artifacts WHERE repo_full_name=? AND path=?", (repo, spath)).fetchone()
        if row:
            sources[row[0]].add(f"notebook01_{label}")
            methods.setdefault(row[0], "repo_path_lookup")
    # 3. MalSkills manifests from git
    index = {}
    for content, fsha in con.execute("SELECT content, file_sha FROM artifacts WHERE content IS NOT NULL"):
        for name, v in variants(content).items():
            index.setdefault(hashlib.sha256(v.encode("utf-8")).hexdigest(), (fsha, name))
    rio_commit = subprocess.run(["git", "rev-parse", RIO_REF], capture_output=True, text=True, cwd=REPO).stdout.strip()
    unresolved = []
    malskills_counts = {}
    for label, gpath in RIO_MANIFESTS.items():
        text = subprocess.run(["git", "show", f"{RIO_REF}:{gpath}"], capture_output=True, text=True, cwd=REPO,
                              check=True).stdout
        entries = json.loads(text)["entries"]
        matched = 0
        for e in entries:
            hit = index.get(e["skill_content_sha256"])
            if hit:
                matched += 1
                sources[hit[0]].add(label)
                methods.setdefault(hit[0], f"sha256_{hit[1]}")
            else:
                unresolved.append({"source": label, "package": e["package"],
                                   "skill_content_sha256": e["skill_content_sha256"]})
        malskills_counts[label] = {"entries": len(entries), "matched": matched, "unresolved": len(entries) - matched}
    out = HERE / "exclusions"
    out.mkdir(exist_ok=True)
    with (out / "excluded_file_shas.csv").open("w", newline="", encoding="utf-8") as h:
        w = csv.writer(h, lineterminator="\n")
        w.writerow(["file_sha", "sources", "first_match_method"])
        for fsha in sorted(sources):
            w.writerow([fsha, ";".join(sorted(sources[fsha])), methods[fsha]])
    with (out / "unresolved.csv").open("w", newline="", encoding="utf-8") as h:
        w = csv.DictWriter(h, fieldnames=["source", "package", "skill_content_sha256"], lineterminator="\n")
        w.writeheader()
        w.writerows(unresolved)
    summary = {"database_sha256": db_sha, "rio_ref": RIO_REF, "rio_commit": rio_commit,
               "excluded_file_shas": len(sources), "malskills": malskills_counts,
               "unresolved_entries": len(unresolved),
               "by_source": {s: sum(1 for v in sources.values() if s in v)
                             for s in sorted({x for v in sources.values() for x in v})},
               "note": "Unresolved MalSkills entries cannot be excluded without skill_mapping.csv; at most this "
                       "many skills of the new sample could overlap the MalSkills samples."}
    (out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
