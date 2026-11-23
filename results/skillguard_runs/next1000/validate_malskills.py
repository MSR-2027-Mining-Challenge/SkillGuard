"""Validate the local MalSkills installation before using it in the experiment.

    .venv/bin/python -I results/skillguard_runs/next1000/validate_malskills.py --malskills-bin ~/MalSkills/.venv/bin/malskills

Check 1 (sanity on MalSkills' own labeled data): scan-corpus with the experiment flags on 5 labeled
malicious and 5 labeled benign skills from MalSkills' data/ground_truth (first 5 of each in CSV
order). Reported as observed verdicts; 10 samples are a smoke test, not an accuracy estimate.

Check 2 (equivalence with Rio's earlier run, branch origin/rio package_test_2): N skills from that
run (all 4 'malicious' plus SSO-bearing and SSO-free skills, chosen deterministically) are
re-exported from the DB exactly as Rio's notebook did (SKILL.md + sibling files with stored text,
written with Windows text-mode newline translation so the bytes, and MalSkills' skill_content_sha256,
match). We compare per skill: content hash, verdict, patterns, sso_count, artifact_count.

Skill content is only read and scanned statically by MalSkills (semgrep); nothing is executed.
Exports go to a temporary directory. Outputs: next1000/malskills_validation/<timestamp>/{summary.json,
groundtruth.csv, rio_equivalence.csv}.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import json
import shutil
import sqlite3
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_exclusions import variants  # noqa: E402
from common import HERE, REPO, write_csv  # noqa: E402
from malskills_runner import MALSKILLS_FLAGS, malskills_env, tool_metadata  # noqa: E402

RIO = "results/malskills/package_test_2"


def scan(bin_path, corpus, source, out, n):
    args = [str(bin_path), "scan-corpus", "--corpus-root", str(corpus), "--output", str(out), "--sample-size", str(n),
            "--source", source, "--seed", "1337", "--workers", "4", *MALSKILLS_FLAGS]
    proc = subprocess.run(args, capture_output=True, text=True, env=malskills_env(bin_path), cwd=str(bin_path.parents[2]))
    if proc.returncode != 0:
        raise SystemExit(f"scan-corpus failed: {proc.stderr[-3000:]}")
    return {json.loads(l)["package"]: json.loads(l) for l in (out / "scan_results.jsonl").read_text().splitlines()}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--malskills-bin", required=True)
    parser.add_argument("--rio-skills", type=int, default=40)
    args = parser.parse_args()
    bin_path = Path(args.malskills_bin).expanduser().resolve()
    ms_repo = bin_path.parents[2]
    out = HERE / "malskills_validation" / dt.datetime.now().strftime("%Y-%m-%d_%H%M%S")
    out.mkdir(parents=True)
    summary = {"tool": tool_metadata(bin_path), "flags": MALSKILLS_FLAGS}
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        # ---- check 1: MalSkills' own labeled samples
        rows = list(csv.DictReader((ms_repo / "data/ground_truth/ground_truth_final.csv").open(encoding="utf-8")))
        picks = [r for r in rows if r["Label"] == "malicious"][:5] + [r for r in rows if r["Label"] == "benign"][:5]
        for r in picks:
            shutil.copytree(ms_repo / r["Ground_truth_path"], tmp / "gt" / "groundtruth" / Path(r["Ground_truth_path"]).name)
        res = scan(bin_path, tmp / "gt", "groundtruth", tmp / "gt_out", len(picks))
        gt = [{"skill": Path(r["Ground_truth_path"]).name, "label": r["Label"],
               "verdict": res.get(Path(r["Ground_truth_path"]).name, {}).get("verdict"),
               "patterns": res.get(Path(r["Ground_truth_path"]).name, {}).get("patterns")} for r in picks]
        write_csv(out / "groundtruth.csv", gt)
        summary["groundtruth_smoke"] = {"samples": len(gt), "verdict_equals_label": sum(g["label"] == g["verdict"] for g in gt)}
        # ---- check 2: reproduce Rio's run on re-exported skills
        rio = [json.loads(l) for l in subprocess.run(["git", "show", f"origin/rio:{RIO}/scan_results.jsonl"],
                                                     capture_output=True, text=True, cwd=REPO).stdout.splitlines()]
        mal = [r for r in rio if r["verdict"] == "malicious"]
        sso = [r for r in rio if r["sso_count"] > 0 and r["verdict"] != "malicious"]
        none = [r for r in rio if r["sso_count"] == 0]
        k = max(0, args.rio_skills - len(mal))
        chosen = mal + sorted(sso, key=lambda r: r["package"])[: k * 2 // 3] + sorted(none, key=lambda r: r["package"])[: k - k * 2 // 3]
        con = sqlite3.connect((REPO / "data/sample/agent_skills_sample.db").as_uri() + "?mode=ro", uri=True)
        want = {r["skill_content_sha256"]: r for r in chosen}
        located = {}
        for repo, path, content in con.execute("SELECT repo_full_name, path, content FROM artifacts WHERE content IS NOT NULL"):
            for name, v in variants(content).items():
                h = hashlib.sha256(v.encode("utf-8")).hexdigest()
                if h in want and want[h]["package"] not in located:
                    located[want[h]["package"]] = (repo, path, content)
        src = tmp / "rio" / "exported_skills"
        for r in chosen:
            if r["package"] not in located:
                continue
            repo, path, content = located[r["package"]]
            folder = src / r["package"]
            folder.mkdir(parents=True)
            # Rio's notebook: Path.write_text on Windows -> newline translation "\n" -> "\r\n"
            (folder / "SKILL.md").write_bytes(content.replace("\n", "\r\n").encode("utf-8"))
            for name, text in con.execute("SELECT entry_name, content FROM artifact_siblings WHERE repo_full_name=? AND "
                                          "artifact_path=? AND entry_type='file' AND content IS NOT NULL", (repo, path)):
                rel = Path(name)
                if rel.is_absolute() or ".." in rel.parts or rel.as_posix().lower() == "skill.md":
                    continue
                (folder / rel).parent.mkdir(parents=True, exist_ok=True)
                (folder / rel).write_bytes(text.replace("\n", "\r\n").encode("utf-8"))
        n = len(list(src.iterdir()))
        res = scan(bin_path, tmp / "rio", "exported_skills", tmp / "rio_out", n)
        eq = []
        for r in chosen:
            new = res.get(r["package"])
            row = {"package": r["package"], "exported": r["package"] in located, "rio_verdict": r["verdict"],
                   "new_verdict": new and new["verdict"], "rio_patterns": r["patterns"], "new_patterns": new and new["patterns"],
                   "rio_sso_count": r["sso_count"], "new_sso_count": new and new["sso_count"],
                   "rio_artifacts": r["artifact_count"], "new_artifacts": new and new["artifact_count"],
                   "content_hash_match": bool(new) and new["skill_content_sha256"] == r["skill_content_sha256"]}
            row["identical"] = bool(new) and all(row[f"rio_{k}"] == row[f"new_{k}"] for k in ("verdict", "patterns", "sso_count"))
            eq.append(row)
        write_csv(out / "rio_equivalence.csv", eq)
        exp = [e for e in eq if e["exported"]]
        summary["rio_equivalence"] = {
            "chosen": len(chosen), "exported": len(exp), "content_hash_match": sum(e["content_hash_match"] for e in exp),
            "identical_verdict_patterns_ssocount": sum(e["identical"] for e in exp),
            "verdict_match": sum(e["rio_verdict"] == e["new_verdict"] for e in exp),
            "artifact_count_match": sum(e["rio_artifacts"] == e["new_artifacts"] for e in exp),
            "rio_malicious_reproduced": sum(e["new_verdict"] == "malicious" for e in exp if e["rio_verdict"] == "malicious")}
    (out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
