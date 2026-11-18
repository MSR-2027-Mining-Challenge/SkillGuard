"""Evaluate frozen SkillGuard V1/V2/V3 and Cisco Static/Behavioral on identical inputs.

    .venv/bin/python -I results/skillguard_runs/run_skillguard_eval_v3.py results/skillguard_runs/heldout/<fresh_dir>

Inputs: <fresh_dir>/R100/<skill>/full (built by heldout/build_fresh_sample.py) and the
Cisco reports for exactly those folders in <fresh_dir>/cisco/R100/<skill>/ (written
by heldout/run_cisco_folders.py). SkillGuard versions are loaded from the frozen
files in versions/. Nothing from a skill is imported or executed.

Outputs (new folder under comparisons/, never overwritten):
  behaviors_v3.csv, findings_v3.csv, coverage_v3.csv, per_skill.csv, cisco_findings.csv,
  summary.json (counts, runtimes) and human_review/ (blind package, see LABELING_GUIDE.md).
Automated outputs never contain human labels; provisional AI labels are written
separately by the reviewer, never into the blind files.
"""

from __future__ import annotations

import csv
import datetime as dt
import hashlib
import importlib.util
import json
import platform
import random
import statistics
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
VERSIONS = {
    "v1": HERE / "versions/skillguard_capabilities_v1_a9e04f89.py",
    "v2": HERE / "versions/skillguard_capabilities_v2_0dea35a9.py",
    "v3": HERE / "versions/skillguard_capabilities_v3_9b625405.py",
}
WINDOW = 3
NON_SECURITY_PREFIXES = ("MANIFEST_", "SKILL_LOAD_")
SEED = 20291113
CLAIM = {
    "nested_agent_invocation": "launches or spawns another AI agent",
    "agent_config_modification": "writes/changes agent configuration or skill folders",
    "agent_env_marker_removal": "removes agent nesting/marker environment variables",
    "scheduler_invocation": "creates, lists or changes scheduled jobs",
    "approval_bypass_instruction": "tells the agent to skip permission/confirmation",
    "agent_credential_access": "reads agent credentials or tokens",
    "suspicious_agent_instruction": "hidden or future-session instruction to the agent",
}


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write_csv(path, rows, fields=None):
    fields = fields or (list(rows[0].keys()) if rows else ["empty"])
    with path.open("w", newline="", encoding="utf-8") as h:
        w = csv.DictWriter(h, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow({k: json.dumps(v, ensure_ascii=False) if isinstance(v, (list, dict)) else v for k, v in r.items()})


def excerpt(full, file, line, radius=1):
    try:
        lines = (full / file).read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeError):
        return ""
    if not line:
        return ""
    lo, hi = max(1, line - radius), min(len(lines), line + radius)
    return " ⏎ ".join(" ".join(lines[i - 1].split())[:220] for i in range(lo, hi + 1))


def main():
    root = Path(sys.argv[1]).resolve()
    mods = {k: load(f"sg_{k}", p) for k, p in VERSIONS.items()}
    started = dt.datetime.now().astimezone()
    out = HERE / "comparisons" / f"{started:%Y-%m-%d_%H%M%S}_{root.name}_v1-v2-v3-cisco"
    out.mkdir(parents=True, exist_ok=False)
    (out / "raw_v3").mkdir()
    review = out / "human_review"
    review.mkdir()
    manifest = {r["skill_id"]: r for r in csv.DictReader((root / "sample_manifest.csv").open(encoding="utf-8"))}
    folders = sorted(root.glob("R100/*/full"))

    b_rows, f_rows, cov_rows, skill_rows, cisco_rows = [], [], [], [], []
    runtimes = defaultdict(list)
    for full in folders:
        skill = full.parent.name
        results, times = {}, {}
        for name, mod in mods.items():
            t0 = time.perf_counter()
            results[name] = mod.scan(full)
            times[name] = time.perf_counter() - t0
            runtimes[name].append(times[name])
        r3 = results["v3"]
        (out / "raw_v3" / f"{skill}.json").write_text(json.dumps(r3, indent=2), encoding="utf-8")
        # Behaviors for V1 via V3's grouping (same counting rules for every version).
        for f in results["v1"]["findings"]:
            f["details"].setdefault("execution_context", mods["v3"].CONTEXT_BY_CARRIER.get(f["carrier"], "direct"))
        behaviors = {"v1": mods["v3"].group_behaviors(results["v1"]["findings"]),
                     "v2": results["v2"]["behaviors"], "v3": r3["behaviors"]}

        # Cisco (identical folder): both full-folder configurations.
        cisco, cisco_time, cisco_ok = [], 0.0, True
        for mode in ("default", "behavioral"):
            report = root / "cisco" / "R100" / skill / f"full_folder_{mode}.json"
            run = root / "cisco" / "R100" / skill / f"full_folder_{mode}.run.json"
            try:
                data = json.loads(report.read_text(encoding="utf-8"))
                record = json.loads(run.read_text(encoding="utf-8"))
                cisco_time += record.get("wall_seconds", 0)
                cisco_ok &= record.get("exit_code") == 0
            except (OSError, json.JSONDecodeError):
                cisco_ok = False
                continue
            for f in data.get("findings", []):
                rule = f.get("rule_id", "")
                security = not (f.get("category") == "policy_violation" or rule.startswith(NON_SECURITY_PREFIXES))
                cisco.append({"skill_id": skill, "configuration": f"Full folder | {mode}", "rule_id": rule,
                              "severity": f.get("severity"), "category": f.get("category"), "title": f.get("title"),
                              "file": f.get("file_path") or "SKILL.md", "line": f.get("line_number"),
                              "security": security})
        runtimes["cisco_full_default_plus_behavioral"].append(cisco_time)
        cisco_rows.extend(cisco)
        cisco_sec = [c for c in cisco if c["security"]]

        for b in r3["behaviors"]:
            lines = [(l["file"], l["line"]) for l in b["locations"] + b["documentation"]]
            near = sorted({f'{c["rule_id"]}@{c["file"]}:{c["line"]}' for c in cisco_sec for file, line in lines
                           if c["file"] == file and c["line"] is not None and abs(c["line"] - line) <= WINDOW})
            same_file = sorted({c["rule_id"] for c in cisco_sec if c["file"] in {f for f, _ in lines}})
            in_v2 = any(b2["capability"] == b["capability"] and
                        {(l["file"], l["line"]) for l in b2["locations"] + b2["documentation"]} & set(lines)
                        for b2 in behaviors["v2"])
            b_rows.append({"skill_id": skill, "stratum": manifest[skill]["stratum"], "behavior_id": b["behavior_id"],
                           "capability": b["capability"], "key": b["key"], "evidence_level": b["evidence_level"],
                           "review_priority": b["review_priority"], "risk_signals": b["risk_signals"],
                           "code_locations": [f'{l["file"]}:{l["line"]}' for l in b["locations"]],
                           "documentation": [f'{l["file"]}:{l["line"]}' for l in b["documentation"]],
                           "commands": b["commands"], "trust_flags": b["trust_flags"], "config_roots": b["config_roots"],
                           "operations": b["operations"], "context_tags": b["context_tags"],
                           "also_in_v2": in_v2, "cisco_security_near": near, "cisco_security_rules_same_file": same_file})
        for f in r3["findings"]:
            d = f["details"]
            f_rows.append({"skill_id": skill, "file": f["file"], "line": f["line"], "carrier": f["carrier"],
                           "capability": f["capability"], "execution_context": d.get("execution_context"),
                           "mechanism": d.get("mechanism", ""), "operation": d.get("operation", ""),
                           "commands": d.get("commands", d.get("command", "")), "trust": d.get("trust_by_command", d.get("trust_flags", "")),
                           "targets": d.get("targets", ""), "signals": d.get("signals", ""),
                           "evidence": d.get("evidence", ""), "evidence_sha256": d.get("evidence_sha256", "")})
        files = defaultdict(set)
        for c in r3["coverage"]:
            files[c["file"]].add(c["status"])
            cov_rows.append({"skill_id": skill, "file": c["file"], "status": c["status"], "line": c.get("line", c.get("first_line", "")),
                             "carrier": c.get("carrier", "")})
        covered = mods["v3"].COVERED_STATUSES
        row = {"skill_id": skill, "stratum": manifest[skill]["stratum"], "design_weight": manifest[skill]["design_weight"],
               "files": len(files),
               "files_code_analyzed": sum(1 for s in files.values() if s & {"analyzed", "analyzed_with_skipped_fences"}),
               "files_text_heuristic_only": sum(1 for s in files.values() if s and s <= {"markdown_instructions_only", "disguised_text_scanned"}),
               "files_not_analyzed": sum(1 for s in files.values() if not s & covered),
               "parse_errors": sum(c["status"] == "parse_error" for c in r3["coverage"]),
               "cisco_ok": cisco_ok, "cisco_security_findings": len(cisco_sec),
               "cisco_security_files": len({c["file"] for c in cisco_sec}),
               "cisco_seconds": round(cisco_time, 2)}
        for name in mods:
            bs = behaviors[name]
            row[f"{name}_findings"] = len(results[name]["findings"])
            row[f"{name}_behaviors"] = len(bs)
            row[f"{name}_seconds"] = round(times[name], 4)
        row["v3_high_priority"] = sum(b["review_priority"] == "high" for b in r3["behaviors"])
        skill_rows.append(row)

    write_csv(out / "behaviors_v3.csv", b_rows)
    write_csv(out / "findings_v3.csv", f_rows)
    write_csv(out / "coverage_v3.csv", cov_rows)
    write_csv(out / "per_skill.csv", skill_rows)
    write_csv(out / "cisco_findings.csv", cisco_rows)

    # ---- blind human-review package -------------------------------------------------
    items, key = [], []
    for b in b_rows:
        locs = json.loads(json.dumps(b["code_locations"])) + json.loads(json.dumps(b["documentation"]))
        first = locs[0] if locs else ":"
        file, line = first.rsplit(":", 1)
        items.append({"skill_id": b["skill_id"], "file": file, "line": int(line) if line.isdigit() else "",
                      "other_locations": locs[1:8], "claim": CLAIM.get(b["capability"], b["capability"]),
                      "_source": "skillguard_v3", "_ref": f'{b["behavior_id"]} {b["capability"]}',
                      "_priority": b["review_priority"]})
    seen = set()
    for c in cisco_rows:
        if not c["security"]:
            continue
        k = (c["skill_id"], c["file"], c["line"], c["rule_id"])
        if k in seen:
            continue
        seen.add(k)
        items.append({"skill_id": c["skill_id"], "file": c["file"], "line": c["line"] or "", "other_locations": [],
                      "claim": c["title"], "_source": "cisco", "_ref": c["rule_id"], "_priority": c["severity"]})
    random.Random(SEED).shuffle(items)
    blind = []
    for i, it in enumerate(items, 1):
        item_id = f"I{i:03d}"
        full = root / "R100" / it["skill_id"] / "full"
        blind.append({"item_id": item_id, "skill_id": it["skill_id"], "file": it["file"], "line": it["line"],
                      "other_locations": it["other_locations"], "claim": it["claim"],
                      "excerpt": excerpt(full, it["file"], it["line"] if isinstance(it["line"], int) else 0),
                      "claim_is_correct": "", "agent_directed": "", "security_relevant": "", "severity_if_relevant": "",
                      "reviewer": "", "review_date": "", "notes": ""})
        key.append({"item_id": item_id, "source": it["_source"], "reference": it["_ref"], "tool_priority": it["_priority"]})
    write_csv(review / "review_items_blind.csv", blind)
    write_csv(review / "review_key_DO_NOT_OPEN_BEFORE_LABELING.csv", key)
    audit = random.Random(SEED + 1).sample(sorted(manifest), 20)
    write_csv(review / "recall_audit_skills.csv",
              [{"skill_id": s, "stratum": manifest[s]["stratum"], "path": str((root / "R100" / s / "full").relative_to(REPO)),
                "n_files": manifest[s]["n_files"], "agent_specific_behaviors_found (file:line + description)": "",
                "reviewer": "", "review_date": "", "minutes_spent": "", "notes": ""} for s in sorted(audit)])

    def stats(xs):
        return {"total_s": round(sum(xs), 2), "mean_s": round(statistics.mean(xs), 4),
                "median_s": round(statistics.median(xs), 4), "max_s": round(max(xs), 3)}

    def total(k):
        return sum(r[k] for r in skill_rows)

    by_cap = Counter(b["capability"] for b in b_rows)
    summary = {
        "run": out.name, "input": str(root.relative_to(REPO)), "started_at": started.isoformat(),
        "python": platform.python_version(), "versions": {k: {"path": str(p.relative_to(REPO)), "sha256": sha(p)} for k, p in VERSIONS.items()},
        "runner_sha256": sha(__file__), "skills": len(folders), "files": total("files"),
        "behaviors": {k: total(f"{k}_behaviors") for k in mods},
        "findings": {k: total(f"{k}_findings") for k in mods},
        "skills_with_behaviors": {k: sum(r[f"{k}_behaviors"] > 0 for r in skill_rows) for k in mods},
        "v3_behaviors_by_capability": dict(by_cap),
        "v3_behaviors_by_evidence": dict(Counter(b["evidence_level"] for b in b_rows)),
        "v3_behaviors_by_priority": dict(Counter(b["review_priority"] for b in b_rows)),
        "v3_behaviors_also_in_v2": sum(b["also_in_v2"] for b in b_rows),
        "v3_behaviors_with_cisco_security_near": sum(bool(b["cisco_security_near"]) for b in b_rows),
        "cisco": {"security_findings_rows": sum(c["security"] for c in cisco_rows),
                  "security_items_unique": len(seen), "skills_with_security_findings": sum(r["cisco_security_findings"] > 0 for r in skill_rows),
                  "rules": dict(Counter(c["rule_id"] for c in cisco_rows if c["security"]).most_common(25)),
                  "all_reports_ok": all(r["cisco_ok"] for r in skill_rows)},
        "coverage_files": {"code_analyzed": total("files_code_analyzed"), "text_heuristic_only": total("files_text_heuristic_only"),
                           "not_analyzed": total("files_not_analyzed"), "parse_error_blocks": total("parse_errors")},
        "runtime": {**{k: stats(runtimes[k]) for k in mods}, "cisco_full_default_plus_behavioral": stats(runtimes["cisco_full_default_plus_behavioral"])},
        "human_review": {"blind_items": len(blind), "recall_audit_skills": len(audit), "labels_present": False},
        "executed_skill_code": False,
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))
    print("wrote", out.relative_to(REPO))


if __name__ == "__main__":
    main()
