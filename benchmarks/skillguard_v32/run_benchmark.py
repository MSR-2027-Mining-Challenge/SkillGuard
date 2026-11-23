"""Run the controlled benchmark against SkillGuard V3.2 and frozen V3.1.

    PYTHONPATH=src .venv/bin/python -I benchmarks/skillguard_v32/run_benchmark.py [--out DIR] [--keep-fixtures DIR]

Each case is materialized into a temporary folder (or --keep-fixtures DIR, for Cisco/MalSkills
comparison runs), scanned, and checked against its expectations. V3.1 (versions/
skillguard_capabilities_v3.1_eebc59e7.py, hash-checked) is scored on the same expectations with a
documented, generous name mapping (nested_agent_invocation -> in_host_delegation when its
mechanism is a spawn instruction / Task call, else external_agent_launch) and a relaxed match:
for capabilities V3.1 knows, only capability + file + line are compared (V3.2-only fields such as
severity, priority, confidence and risk indicators are ignored). Checks about capabilities,
chains, links, coverage or declarations that V3.1 cannot produce are "not expressible".

This measures agreement with hand-written expectations on synthetic cases. It is a regression and
specification test, not a precision/recall estimate on real skills.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
import tempfile
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(REPO / "src"))
sys.path.insert(0, str(HERE))

from cases import CASES  # noqa: E402
from skillguard import scan  # noqa: E402

V31 = REPO / "results/skillguard_runs/versions/skillguard_capabilities_v3.1_eebc59e7.py"
V31_CAPS = {"external_agent_launch", "in_host_delegation", "scheduler_invocation", "agent_config_modification",
            "agent_env_marker_removal", "agent_credential_access", "approval_bypass_instruction",
            "suspicious_agent_instruction"}
PRIORITY = ["none", "low", "medium", "high"]


def load_v31():
    sha = hashlib.sha256(V31.read_bytes()).hexdigest()
    assert sha.startswith("eebc59e7"), sha
    spec = importlib.util.spec_from_file_location("skillguard_v31_frozen", V31)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def materialize(case, root):
    folder = root / case["id"]
    for rel, text in case["files"].items():
        path = folder / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(text.encode("utf-8"))
    return folder


def _subset(actual, expected):
    if isinstance(expected, list):
        return isinstance(actual, list) and all(e in actual for e in expected) and (expected or not actual)
    return actual == expected


def matches(f, e):
    if "cap" in e and f["capability"] != e["cap"]:
        return False
    for key, fkey in (("file", "file"), ("line", "line"), ("severity", "severity"), ("context", "execution_context"),
                      ("layer", "layer"), ("subcategory", "subcategory"), ("confidence", "confidence"),
                      ("priority", "review_priority")):
        if key in e and f.get(fkey) != e[key]:
            return False
    if "min_priority" in e and PRIORITY.index(f["review_priority"]) < PRIORITY.index(e["min_priority"]):
        return False
    if "risk" in e and not set(e["risk"]) <= set(f.get("risk_indicators", [])):
        return False
    for k, v in e.get("detail", {}).items():
        if not _subset(f["details"].get(k), v):
            return False
    return True


def check_v32(case, result):
    checks = []
    for e in case.get("expect", []):
        checks.append(("expect", e, any(matches(f, e) for f in result["findings"])))
    for e in case.get("forbid", []):
        checks.append(("forbid", e, not any(matches(f, e) for f in result["findings"])))
    for c in case.get("chains", []):
        ok = any(ch["rule"] == c["rule"] and all(ch.get(k) == v for k, v in c.items() if k != "rule")
                 for ch in result["chains"])
        checks.append(("chain", c, ok))
    for rule in case.get("forbid_chains", []):
        checks.append(("forbid_chain", rule, not any(ch["rule"] == rule for ch in result["chains"])))
    for l in case.get("links", []):
        ok = any(all(link.get(k) == v for k, v in l.items()) for link in result["links"])
        checks.append(("link", l, ok))
    status = {c["file"]: c["status"] for c in result["coverage"]["files"]}
    for file, expected in case.get("coverage", {}).items():
        checks.append(("coverage", {file: expected}, status.get(file) == expected))
    for k, v in case.get("declared", {}).items():
        checks.append(("declared", {k: v}, result["declared_tools"].get(k) == v))
    if "max_primary" in case:
        checks.append(("max_primary", case["max_primary"], result["summary"]["primary_findings"] <= case["max_primary"]))
    return checks


def v31_findings(mod, folder):
    out = []
    for f in mod.scan(folder)["findings"]:
        cap = f["capability"]
        if cap == "nested_agent_invocation":
            mech = f["details"].get("mechanism", "")
            cap = "in_host_delegation" if mech in {"agent_spawn_instruction", "agent_tool_call"} else "external_agent_launch"
        out.append({"capability": cap, "file": f["file"], "line": f["line"], "details": f["details"]})
    return out


def check_v31(case, findings):
    checks = []
    for kind in ("expect", "forbid"):
        for e in case.get(kind, []):
            # Relaxed comparison: V3.1 is credited when a finding of the (mapped) capability exists at the
            # expected file/line, ignoring V3.2-only fields (severity, priority, confidence, risk, details).
            if e.get("cap") not in V31_CAPS:
                checks.append((kind, e, None))
                continue
            hit = any(f["capability"] == e["cap"] and all(f[k] == e[k] for k in ("file", "line") if k in e)
                      for f in findings)
            checks.append((kind, e, hit if kind == "expect" else not hit))
    for kind in ("chains", "forbid_chains", "links", "coverage", "declared"):
        for item in (case.get(kind, {}).items() if isinstance(case.get(kind), dict) else case.get(kind, [])):
            checks.append((kind, item, None))
    if "max_primary" in case:
        checks.append(("max_primary", case["max_primary"], len(findings) <= case["max_primary"]))
    return checks


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", help="write results JSON + Markdown report to this directory")
    parser.add_argument("--keep-fixtures", help="materialize fixtures here (kept) instead of a temp dir")
    args = parser.parse_args()
    v31 = load_v31()
    rows = []
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(args.keep_fixtures) if args.keep_fixtures else Path(tmp)
        root.mkdir(parents=True, exist_ok=True)
        for case in CASES:
            folder = materialize(case, root)
            try:
                result = scan(folder)
                c32 = check_v32(case, result)
                error = None
            except Exception as exc:  # a crash is a failure of every check
                c32, error = [("crash", repr(exc), False)], repr(exc)
            c31 = check_v31(case, v31_findings(v31, folder))
            rows.append({"id": case["id"], "group": case["group"], "kind": case["kind"],
                         "description": case["description"], "error": error,
                         "v32": [{"type": t, "spec": s, "ok": ok} for t, s, ok in c32],
                         "v31": [{"type": t, "spec": s if not isinstance(s, tuple) else list(s), "ok": ok}
                                 for t, s, ok in c31]})
    total32 = sum(len(r["v32"]) for r in rows)
    pass32 = sum(c["ok"] for r in rows for c in r["v32"])
    cases_pass32 = sum(all(c["ok"] for c in r["v32"]) for r in rows)
    v31_all = [c for r in rows for c in r["v31"]]
    v31_expr = [c for c in v31_all if c["ok"] is not None]
    summary = {"cases": len(rows), "checks": total32, "v32_checks_passed": pass32, "v32_cases_fully_passed": cases_pass32,
               "v31_checks_passed": sum(1 for c in v31_expr if c["ok"]), "v31_checks_expressible": len(v31_expr),
               "v31_checks_not_expressible": len(v31_all) - len(v31_expr),
               "v31_cases_fully_passed": sum(all(c["ok"] for c in r["v31"]) for r in rows)}
    by_group = defaultdict(Counter)
    for r in rows:
        g = by_group[r["group"]]
        g["cases"] += 1
        g["v32_pass"] += all(c["ok"] for c in r["v32"])
        g["v31_pass"] += all(c["ok"] for c in r["v31"])
        g["v31_expressible_ok"] += sum(1 for c in r["v31"] if c["ok"])
        g["v31_expressible"] += sum(1 for c in r["v31"] if c["ok"] is not None)
    print(json.dumps(summary, indent=2))
    for r in rows:
        bad = [c for c in r["v32"] if not c["ok"]]
        if bad:
            print("FAIL", r["id"], json.dumps(bad, default=str)[:600])
    if args.out:
        out = Path(args.out)
        out.mkdir(parents=True, exist_ok=True)
        (out / "benchmark_results.json").write_text(json.dumps({"summary": summary, "by_group": by_group, "cases": rows},
                                                               indent=2, default=str) + "\n")
        lines = ["# SkillGuard controlled benchmark", "",
                 "Synthetic cases with hand-written expectations. This is a specification/regression test, "
                 "not an accuracy estimate on real skills.", "",
                 f"- Cases: {summary['cases']}; checks: {summary['checks']}",
                 f"- V3.2: {summary['v32_checks_passed']}/{summary['checks']} checks, "
                 f"{summary['v32_cases_fully_passed']}/{summary['cases']} cases fully passed",
                 f"- V3.1 (frozen, generous name mapping): {summary['v31_checks_passed']}/{summary['v31_checks_expressible']} "
                 f"expressible checks passed; {summary['v31_checks_not_expressible']} checks need V3.2-only output "
                 f"(severity, priority, confidence, chains, links, new formats); "
                 f"{summary['v31_cases_fully_passed']}/{summary['cases']} cases fully passed", "",
                 "| Group | Cases | V3.2 cases passed | V3.1 cases passed | V3.1 expressible checks passed |",
                 "|---|---|---|---|---|"]
        for g, c in sorted(by_group.items()):
            lines.append(f"| {g} | {c['cases']} | {c['v32_pass']} | {c['v31_pass']} | {c['v31_expressible_ok']}/{c['v31_expressible']} |")
        lines += ["", "| Case | Kind | V3.2 | V3.1 | Description |", "|---|---|---|---|---|"]
        for r in rows:
            v32 = "pass" if all(c["ok"] for c in r["v32"]) else "FAIL"
            v31c = [c["ok"] for c in r["v31"]]
            v31 = "pass" if all(v31c) else ("n/a" if all(x is None for x in v31c) else "fail")
            lines.append(f"| {r['id']} | {r['kind']} | {v32} | {v31} | {r['description']} |")
        (out / "BENCHMARK_REPORT.md").write_text("\n".join(lines) + "\n")
    return 0 if pass32 == total32 else 1


if __name__ == "__main__":
    sys.exit(main())
