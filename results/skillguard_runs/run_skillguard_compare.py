"""Compare SkillGuard V1 (frozen) vs V2 (working tree) vs Cisco Static/Behavioral.

    # development sample (Nov-3 baseline, 30 skills)
    .venv/bin/python -I results/skillguard_runs/run_skillguard_compare.py dev30
    # held-out sample built by heldout/build_heldout_sample.py
    .venv/bin/python -I results/skillguard_runs/run_skillguard_compare.py heldout results/skillguard_runs/heldout/<dir>

Read-only with respect to skills: SkillGuard parses files (ast/shlex/regex);
nothing from a skill is imported or executed. Each run writes a new timestamped
folder and never overwrites earlier runs or Cisco results.

Units of analysis
  finding  = one SkillGuard row (one sink / one instruction line)
  behavior = SkillGuard V2 group_behaviors() output, per skill. V1 findings are
             grouped with the same V2 function (execution_context taken from the
             carrier) so both versions are counted the same way.
Cisco match = a Cisco finding with finding kind "security" (dev30: finding_kind
column; held-out: category != policy_violation and rule not MANIFEST_*/
SKILL_LOAD_*) in the same skill and file within +/-3 lines of any behavior line.
"""

from __future__ import annotations

import csv
import datetime as dt
import hashlib
import importlib.util
import json
import platform
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
V1_PATH = HERE / "versions/skillguard_capabilities_v1_a9e04f89.py"
V2_PATH = REPO / "src/skillguard_capabilities.py"
DEV = REPO / "results/cisco_dataset_runs/agent_skills_sample/runs/2026-11-03_173516_sample30-seed2027"
WINDOW = 3
NON_SECURITY_PREFIXES = ("MANIFEST_", "SKILL_LOAD_")


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


def skills_for(mode, arg):
    if mode == "dev30":
        return [(p.parent.name, "dev30", p) for p in sorted(DEV.glob("*/full"))]
    root = Path(arg).resolve()
    return [(p.parent.name, p.parent.parent.name, p) for p in sorted(root.glob("H*_*/*/full"))]


def cisco_findings(mode, arg):
    """(skill, file) -> [(line, rule, configuration)] security findings; plus scanned skills."""
    out, scanned = defaultdict(list), set()
    if mode == "dev30":
        for row in csv.DictReader((DEV / "individual_findings.csv").open(encoding="utf-8")):
            if row["finding_kind"] != "security":
                continue
            line = int(row["reported_line_number"]) if row["reported_line_number"].strip().isdigit() else None
            out[(row["skill_id"], row["file_path"])].append((line, row["rule_id"], row["configuration"]))
        for row in csv.DictReader((DEV / "scan_summary.csv").open(encoding="utf-8")):
            if row["status"] in {"COMPLETE", "PARTIAL"} and row["scope"] == "Full folder":
                scanned.add(row["skill_id"])
        return out, scanned
    root = Path(arg).resolve()
    for report in sorted(root.glob("cisco/*/*/full_folder_*.json")):
        skill, mode_name = report.parent.name, report.stem.replace("full_folder_", "")
        try:
            data = json.loads(report.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        scanned.add(skill)
        for f in data.get("findings", []):
            rule = f.get("rule_id", "")
            if f.get("category") == "policy_violation" or rule.startswith(NON_SECURITY_PREFIXES):
                continue
            out[(skill, f.get("file_path") or "SKILL.md")].append(
                (f.get("line_number"), rule, f"Full folder | {mode_name}"))
    return out, scanned


def behavior_lines(b):
    return [(l["file"], l["line"]) for l in b["locations"] + b["documentation"]]


def main():
    mode = sys.argv[1]
    arg = sys.argv[2] if len(sys.argv) > 2 else None
    v1, v2 = load("sg_v1", V1_PATH), load("sg_v2", V2_PATH)
    started = dt.datetime.now().astimezone()
    label = "dev30" if mode == "dev30" else Path(arg).name
    out = HERE / "comparisons" / f"{started:%Y-%m-%d_%H%M%S}_{label}_v1-v2-cisco"
    out.mkdir(parents=True, exist_ok=False)
    (out / "raw_v2").mkdir()
    cisco, cisco_scanned = cisco_findings(mode, arg)

    f_rows, b_rows, cov_rows, skill_rows = [], [], [], []
    for skill, set_name, full in skills_for(mode, arg):
        r1 = v1.scan(full)
        r2 = v2.scan(full)
        (out / "raw_v2" / f"{skill}.json").write_text(json.dumps(r2, indent=2), encoding="utf-8")
        # V1 findings grouped with V2's grouping function (context from carrier).
        for f in r1["findings"]:
            f["details"].setdefault("execution_context", v2.CONTEXT_BY_CARRIER.get(f["carrier"], "direct"))
        b1 = v2.group_behaviors(r1["findings"])
        v1_keys = {(f["file"], f["line"], f["capability"]) for f in r1["findings"]}

        for f in r2["findings"]:
            d = f["details"]
            f_rows.append({"set": set_name, "skill_id": skill, "file": f["file"], "line": f["line"],
                           "carrier": f["carrier"], "capability": f["capability"],
                           "execution_context": d.get("execution_context"), "mechanism": d.get("mechanism", ""),
                           "commands": d.get("commands", d.get("command", "")), "trust": d.get("trust_by_command", d.get("trust_flags", "")),
                           "targets": d.get("targets", ""), "removed": d.get("removed", d.get("env_markers_removed", "")),
                           "evidence": d.get("evidence", ""), "in_v1": (f["file"], f["line"], f["capability"]) in v1_keys})
        for b in r2["behaviors"]:
            lines = behavior_lines(b)
            near = sorted({f"{rule}@{file}:{cl}" for file, line in lines
                           for cl, rule, _ in cisco.get((skill, file), []) if cl is not None and abs(cl - line) <= WINDOW})
            in_v1 = any((file, line, b["capability"]) in v1_keys for file, line in lines)
            b_rows.append({"set": set_name, "skill_id": skill, "behavior_id": b["behavior_id"],
                           "capability": b["capability"], "key": b["key"], "evidence_level": b["evidence_level"],
                           "code_locations": [f'{l["file"]}:{l["line"]}' for l in b["locations"]],
                           "documentation": [f'{l["file"]}:{l["line"]}' for l in b["documentation"]],
                           "commands": b["commands"], "trust_flags": b["trust_flags"], "removed": b["removed"],
                           "config_roots": b["config_roots"], "detected_by_v1": in_v1,
                           "cisco_scanned": skill in cisco_scanned, "cisco_security_near": near})
        for c in r2["coverage"]:
            cov_rows.append({"set": set_name, "skill_id": skill, "file": c["file"], "status": c["status"],
                             "carrier": c.get("carrier", ""), "line": c.get("line", c.get("first_line", "")),
                             "skipped_fences": c.get("skipped_fences", "")})
        files2 = defaultdict(set)
        for c in r2["coverage"]:
            files2[c["file"]].add(c["status"])
        files1 = defaultdict(set)
        for c in r1["coverage"]:
            files1[c["file"]].add(c["status"])
        skill_rows.append({
            "set": set_name, "skill_id": skill, "files": len(files2),
            "v1_findings": len(r1["findings"]), "v1_behaviors": len(b1),
            "v1_code_behaviors": sum(b["evidence_level"] in {"code", "generated_code"} for b in b1),
            "v2_findings": len(r2["findings"]), "v2_behaviors": len(r2["behaviors"]),
            "v2_code_behaviors": sum(b["evidence_level"] == "code" for b in r2["behaviors"]),
            "v2_generated_behaviors": sum(b["evidence_level"] == "generated_code" for b in r2["behaviors"]),
            "v2_doc_only_behaviors": sum(b["evidence_level"] == "documented_example" for b in r2["behaviors"]),
            "v2_instruction_only_behaviors": sum(b["evidence_level"] == "instruction_only" for b in r2["behaviors"]),
            "v1_parse_errors": sum(c["status"] == "parse_error" for c in r1["coverage"]),
            "v2_parse_errors": sum(c["status"] == "parse_error" for c in r2["coverage"]),
            "v1_files_not_analyzed": sum(1 for s in files1.values() if not s & {"analyzed", "analyzed_with_skipped_fences"}),
            "v2_files_not_analyzed": sum(1 for s in files2.values() if not s & v2.COVERED_STATUSES),
            "v2_files_instruction_layer_only": sum(1 for s in files2.values() if s == {"markdown_instructions_only"}),
            "cisco_security_findings": sum(len(v) for (sk, _), v in cisco.items() if sk == skill),
            "cisco_scanned": skill in cisco_scanned,
        })

    write_csv(out / "findings_v2.csv", f_rows)
    write_csv(out / "behaviors_v2.csv", b_rows)
    write_csv(out / "coverage_v2.csv", cov_rows)
    write_csv(out / "per_skill.csv", skill_rows)

    def tot(key, rows=skill_rows):
        return sum(r[key] for r in rows)

    by_set = {}
    for set_name in sorted({r["set"] for r in skill_rows}):
        rows = [r for r in skill_rows if r["set"] == set_name]
        brows = [b for b in b_rows if b["set"] == set_name]
        by_set[set_name] = {
            "skills": len(rows), "files": tot("files", rows),
            "v1": {"findings": tot("v1_findings", rows), "behaviors": tot("v1_behaviors", rows),
                   "skills_with_behaviors": sum(r["v1_behaviors"] > 0 for r in rows),
                   "parse_errors": tot("v1_parse_errors", rows), "files_not_analyzed": tot("v1_files_not_analyzed", rows)},
            "v2": {"findings": tot("v2_findings", rows), "behaviors": tot("v2_behaviors", rows),
                   "behaviors_by_evidence": dict(Counter(b["evidence_level"] for b in brows)),
                   "behaviors_by_capability": dict(Counter(b["capability"] for b in brows)),
                   "skills_with_behaviors": sum(r["v2_behaviors"] > 0 for r in rows),
                   "skills_with_code_behaviors": sum((r["v2_code_behaviors"] + r["v2_generated_behaviors"]) > 0 for r in rows),
                   "parse_errors": tot("v2_parse_errors", rows), "files_not_analyzed": tot("v2_files_not_analyzed", rows),
                   "files_instruction_layer_only": tot("v2_files_instruction_layer_only", rows)},
            "v2_behaviors_also_found_by_v1": sum(b["detected_by_v1"] for b in brows),
            "v2_behaviors_with_cisco_security_near": sum(bool(b["cisco_security_near"]) for b in brows),
            "cisco_security_findings": tot("cisco_security_findings", rows),
            "skills_with_cisco_security_findings": sum(r["cisco_security_findings"] > 0 for r in rows),
            "cisco_scanned_skills": sum(r["cisco_scanned"] for r in rows),
        }
    meta = {"run": out.name, "mode": mode, "input": arg or str(DEV.relative_to(REPO)),
            "started_at": started.isoformat(), "python": platform.python_version(),
            "v1": {"path": str(V1_PATH.relative_to(REPO)), "sha256": sha(V1_PATH)},
            "v2": {"path": str(V2_PATH.relative_to(REPO)), "sha256": sha(V2_PATH)},
            "runner_sha256": sha(__file__), "cisco_window": WINDOW, "by_set": by_set,
            "executed_skill_code": False}
    (out / "summary.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(json.dumps(meta["by_set"], indent=2))
    print("wrote", out.relative_to(REPO))


if __name__ == "__main__":
    main()
