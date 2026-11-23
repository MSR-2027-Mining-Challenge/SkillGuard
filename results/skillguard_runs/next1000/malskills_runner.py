"""MalSkills for the next 1,000-skill experiment: prepare corpus, run (pinned), import results.

    # 1. copy the exact exported folders into a MalSkills corpus (byte-identical, digests checked)
    .venv/bin/python -I results/skillguard_runs/next1000/malskills_runner.py prepare <cisco_run_dir> <corpus_root>
    # 2. run MalSkills (static profile, no LLM) - needs a local MalSkills checkout with semgrep
    .venv/bin/python -I results/skillguard_runs/next1000/malskills_runner.py run <corpus_root> <output_dir> \
        --malskills-bin /path/to/MalSkills/.venv/bin/malskills [--workers 4]
    # 3. normalize results (source-mapped lines, identity checks, statuses)
    .venv/bin/python -I results/skillguard_runs/next1000/malskills_runner.py import <output_dir> <cisco_run_dir>

Design decisions (see next1000/README.md):
* Corpus layout <corpus_root>/next1000/<skill_id>/... so MalSkills' package name == notebook-01
  skill_id (no skill_NNNN renumbering). Files are copied as bytes (never through a text-mode or
  Windows newline-translating path); a SHA256SUMS file lets the MalSkills machine verify them.
* `scan-corpus --profile static --retain all --sample-size N --seed 1337` with N = number of
  folders so MalSkills' own sampler keeps every folder; the import step fails if any skill is
  missing or if MalSkills' skill_content_sha256 differs from the exported SKILL.md bytes.
* The MalSkills git commit, semgrep version and the rules directory digest are recorded (the scan
  config's ruleset_digest was "none" in the earlier run).
* Lines: SSO findings in extracted Markdown fences (".malskills_fences/...") are mapped back to the
  source file via artifacts.json: file_line = source_start_line + span.start_line.
* Status per skill: ok / error / capped (artifact_count >= max_artifacts) / missing.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # python -I does not add the script folder
from common import HERE, folder_digest, skill_dirs, write_csv, write_split, reset_sealed

SOURCE = "next1000"


def prepare(run_dir, corpus_root):
    run = Path(run_dir).resolve()
    dest_root = Path(corpus_root).resolve() / SOURCE
    dest_root.mkdir(parents=True, exist_ok=False)
    sums, rows = [], []
    for skill_id, folder in skill_dirs(run):
        dest = dest_root / skill_id
        for p in sorted(folder.rglob("*")):
            if p.is_file() and not p.is_symlink():
                target = dest / p.relative_to(folder)
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(p, target)  # byte copy
                sums.append(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {SOURCE}/{skill_id}/{p.relative_to(folder).as_posix()}")
        same = folder_digest(folder) == folder_digest(dest)
        rows.append({"skill_id": skill_id, "digest_match": same})
        if not same:
            raise SystemExit(f"copy mismatch for {skill_id}")
    (Path(corpus_root) / "SHA256SUMS").write_text("\n".join(sums) + "\n")
    print(json.dumps({"skills": len(rows), "files": len(sums), "corpus": str(dest_root)}))


def run(corpus_root, output_dir, malskills_bin, workers):
    corpus = Path(corpus_root).resolve()
    n = len([p for p in (corpus / SOURCE).iterdir() if p.is_dir()])
    bin_path = Path(malskills_bin).resolve()
    repo = bin_path.parents[2] if len(bin_path.parents) > 2 else bin_path.parent
    meta = {"malskills_bin": str(bin_path),
            "malskills_commit": subprocess.run(["git", "-C", str(repo), "rev-parse", "HEAD"], capture_output=True,
                                               text=True).stdout.strip() or "unknown",
            "semgrep_version": subprocess.run([str(bin_path.parent / "semgrep"), "--version"], capture_output=True,
                                              text=True).stdout.strip() or "unknown",
            "rules_digest": _dir_digest(repo / "malskills" / "rules") if (repo / "malskills" / "rules").is_dir() else "unknown",
            "skills": n, "args": ["scan-corpus", "--corpus-root", str(corpus), "--output", str(output_dir),
                                  "--sample-size", str(n), "--profile", "static", "--source", SOURCE,
                                  "--seed", "1337", "--workers", str(workers), "--retain", "all"]}
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    (Path(output_dir) / "skillguard_run_metadata.json").write_text(json.dumps(meta, indent=2) + "\n")
    proc = subprocess.run([str(bin_path), *meta["args"]], text=True)
    sys.exit(proc.returncode)


def _dir_digest(path):
    h = hashlib.sha256()
    for p in sorted(Path(path).rglob("*")):
        if p.is_file():
            h.update(p.relative_to(path).as_posix().encode() + b"\0" + hashlib.sha256(p.read_bytes()).digest())
    return h.hexdigest()


def map_line(finding, artifacts):
    """(source_file, source_line) for an SSO finding, following fence extraction back to Markdown."""
    art_id = finding.get("artifact_id") or finding.get("provenance", {}).get("artifact", {}).get("id")
    art = artifacts.get(art_id, {})
    span = finding.get("span") or finding.get("provenance", {}).get("span") or {}
    line = span.get("start_line")
    if art.get("generated") in (True, "True") and art.get("source_artifact_path"):
        start = art.get("source_start_line")
        return art["source_artifact_path"], (int(start) + int(line)) if start is not None and line is not None else None
    return finding.get("artifact_path") or art.get("relative_path"), line


def import_results(output_dir, run_dir, max_artifacts=600):
    output = Path(output_dir)
    run = Path(run_dir).resolve() if run_dir else None
    exported = {sid: folder for sid, folder in skill_dirs(run)} if run else {}
    scans, findings, verdicts = [], [], []
    seen = set()
    for line in (output / "scan_results.jsonl").read_text(encoding="utf-8").splitlines():
        rec = json.loads(line)
        sid = rec["package"]
        seen.add(sid)
        status = "ok" if rec.get("status") == "ok" else "error"
        if status == "ok" and rec.get("artifact_count", 0) >= max_artifacts:
            status = "capped"
        identity = None
        if sid in exported:
            skill_md = exported[sid] / "SKILL.md"
            identity = skill_md.is_file() and hashlib.sha256(skill_md.read_bytes()).hexdigest() == rec.get("skill_content_sha256")
        scans.append({"skill_id": sid, "status": status, "verdict": rec.get("verdict"), "patterns": rec.get("patterns", []),
                      "sso_count": rec.get("sso_count"), "artifact_count": rec.get("artifact_count"),
                      "semgrep_status": rec.get("semgrep_status"), "identity_match": identity,
                      "runtime_sec": rec.get("runtime_sec")})
        case = output / rec["retained_output"] if rec.get("retained_output") else None
        if case is None or not case.is_dir():
            continue
        artifacts = {a["artifact_id"]: a for a in json.loads((case / "artifacts.json").read_text())}
        for f in json.loads((case / "sso_findings.json").read_text()):
            file, src_line = map_line(f, artifacts)
            findings.append({"skill_id": sid, "finding_id": f.get("finding_id"), "category": f.get("category"),
                             "rule_id": (f.get("attributes", {}).get("rule_id") or "").rsplit(".", 2)[-1],
                             "file": file, "line": src_line, "artifact_path": f.get("artifact_path"),
                             "matched_text": (f.get("matched_text") or "")[:160]})
        verdict = json.loads((case / "verdict.json").read_text())
        for p in verdict.get("supporting_patterns", []):
            verdicts.append({"skill_id": sid, "label": verdict.get("label"), "pattern": p.get("name"),
                             "severity": p.get("severity"), "finding_ids": p.get("finding_ids", [])})
    for sid in exported:
        if sid not in seen:
            scans.append({"skill_id": sid, "status": "missing"})
    dest = HERE / "malskills" / output.name
    dest.mkdir(parents=True, exist_ok=True)
    reset_sealed(dest)
    write_csv(dest / "scans.csv", scans)
    counts = {name: write_split(dest, name, rows) for name, rows in (("sso_findings", findings),
                                                                     ("pattern_verdicts", verdicts))}
    summary = {"output": str(output.name), "scans": len(scans), "statuses": dict(Counter(s["status"] for s in scans)),
               "identity_mismatches": sum(s.get("identity_match") is False for s in scans),
               "verdicts": dict(Counter(s.get("verdict") for s in scans)), "rows_open_sealed": counts}
    (dest / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary))
    return summary


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("prepare"); p.add_argument("run_dir"); p.add_argument("corpus_root")
    r = sub.add_parser("run"); r.add_argument("corpus_root"); r.add_argument("output_dir")
    r.add_argument("--malskills-bin", required=True); r.add_argument("--workers", type=int, default=4)
    i = sub.add_parser("import"); i.add_argument("output_dir"); i.add_argument("run_dir", nargs="?")
    args = parser.parse_args()
    if args.cmd == "prepare":
        prepare(args.run_dir, args.corpus_root)
    elif args.cmd == "run":
        run(args.corpus_root, args.output_dir, args.malskills_bin, args.workers)
    else:
        import_results(args.output_dir, args.run_dir)


if __name__ == "__main__":
    main()
