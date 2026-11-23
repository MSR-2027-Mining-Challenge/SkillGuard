"""Run Cisco skill-scanner (core, and core + ATR pack) on the V3.2 controlled benchmark fixtures.

    .venv/bin/python -I results/skillguard_runs/v32_scanner_comparison/run_benchmark_scanners.py

The fixtures are the synthetic, team-written folders of benchmarks/skillguard_v32/cases.py
(materialized into a temporary directory). For every expected V3.2 finding with a file (and line)
we record whether each Cisco configuration reports a security finding in the same file within
+/-3 lines (or anywhere in the file when the expectation has no line).

This shows which *specified behaviors* each scanner surfaces on synthetic inputs. It is not an
accuracy estimate, and Cisco is not designed around SkillGuard's capability definitions.
MalSkills is not run here: it is not installed in this environment (see next1000/README.md).

Outputs: results/skillguard_runs/v32_scanner_comparison/<timestamp>/ with cisco_raw/*.json
(synthetic fixtures only, so no dataset content), expectation_coverage.csv, summary.json, REPORT.md.
"""

from __future__ import annotations

import csv
import datetime as dt
import json
import subprocess
import sys
import tempfile
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(REPO / "benchmarks/skillguard_v32"))
sys.path.insert(0, str(REPO / "src"))
from cases import CASES  # noqa: E402
from run_benchmark import materialize  # noqa: E402

SCANNER = str(REPO / ".venv/bin/skill-scanner")
CONFIGS = {"cisco_core_behavioral": ["--use-behavioral"],
           "cisco_core_atr_behavioral": ["--use-behavioral", "--rule-packs", "atr"]}
WINDOW = 3
SECURITY_EXCLUDE = {"MANIFEST_MISSING_LICENSE", "SKILL_LOAD_FALLBACK_USED", "MANIFEST_DESCRIPTION_TOO_LONG",
                    "SOCIAL_ENG_VAGUE_DESCRIPTION"}


def cisco_findings(report):
    out = []
    for f in report.get("findings", []):
        rule = f.get("rule_id", "")
        if rule in SECURITY_EXCLUDE or f.get("severity") == "INFO":
            continue
        path = (f.get("file_path") or "")
        line = f.get("line_number")
        out.append({"rule": rule, "category": f.get("category"), "severity": f.get("severity"),
                    "file": path, "line": line})
    return out


def rel(path, folder):
    if not path:
        return ""
    p = Path(path)
    try:
        return p.resolve().relative_to(folder.resolve()).as_posix()
    except ValueError:
        return p.as_posix().lstrip("./")


def main():
    out = HERE / dt.datetime.now().strftime("%Y-%m-%d_%H%M%S")
    (out / "cisco_raw").mkdir(parents=True)
    version = subprocess.run([SCANNER, "--version"], capture_output=True, text=True).stdout.strip()
    rows, per_config = [], defaultdict(Counter)
    with tempfile.TemporaryDirectory() as tmp:
        for case in CASES:
            folder = materialize(case, Path(tmp))
            reports = {}
            for name, extra in CONFIGS.items():
                proc = subprocess.run([SCANNER, "scan", str(folder), "--format", "json", "--policy", "balanced", *extra],
                                      capture_output=True, text=True, timeout=300)
                try:
                    report = json.loads(proc.stdout)
                except json.JSONDecodeError:
                    report = {"error": proc.stderr[-2000:], "findings": []}
                text = json.dumps(report, indent=1).replace(str(folder), "<fixture>")
                (out / "cisco_raw" / f"{case['id']}__{name}.json").write_text(text)
                reports[name] = [dict(f, file=rel(f["file"], folder)) for f in cisco_findings(report)]
                per_config[name]["cases_with_security_finding"] += bool(reports[name])
                per_config[name]["security_findings"] += len(reports[name])
                per_config[name]["scan_errors"] += "error" in report
            for e in case.get("expect", []):
                if "file" not in e:
                    continue
                row = {"case": case["id"], "group": case["group"], "capability": e["cap"], "file": e["file"],
                       "line": e.get("line", "")}
                for name in CONFIGS:
                    near = [f["rule"] for f in reports[name] if f["file"] == e["file"]
                            and ("line" not in e or (f["line"] is not None and abs(int(f["line"]) - e["line"]) <= WINDOW))]
                    row[name] = sorted(set(near))
                rows.append(row)
    with (out / "expectation_coverage.csv").open("w", newline="") as h:
        w = csv.DictWriter(h, fieldnames=list(rows[0].keys()))
        w.writeheader()
        for r in rows:
            w.writerow({k: json.dumps(v) if isinstance(v, list) else v for k, v in r.items()})
    by_cap = defaultdict(lambda: Counter())
    for r in rows:
        c = by_cap[r["capability"]]
        c["expected"] += 1
        for name in CONFIGS:
            c[name] += bool(r[name])
    summary = {"scanner_version": version, "policy": "balanced", "configs": CONFIGS, "cases": len(CASES),
               "expected_findings_with_location": len(rows),
               "located_by": {name: sum(bool(r[name]) for r in rows) for name in CONFIGS},
               "per_config": per_config, "by_capability": by_cap}
    (out / "summary.json").write_text(json.dumps(summary, indent=2, default=dict) + "\n")
    lines = ["# Cisco core vs core+ATR on the SkillGuard V3.2 controlled benchmark", "",
             f"Scanner: {version}, policy balanced, behavioral analyzer on. Synthetic fixtures only.", "",
             "A cell counts an expected V3.2 finding as *located* when the configuration reports a non-INFO "
             "finding in the same file within +/-3 lines. Locating is not the same as classifying it the same way.", "",
             "| Capability (V3.2) | Expected | Cisco core | Cisco core + ATR |", "|---|---|---|---|"]
    for cap, c in sorted(by_cap.items()):
        lines.append(f"| {cap} | {c['expected']} | {c['cisco_core_behavioral']} | {c['cisco_core_atr_behavioral']} |")
    lines.append(f"| **total** | {len(rows)} | {summary['located_by']['cisco_core_behavioral']} | "
                 f"{summary['located_by']['cisco_core_atr_behavioral']} |")
    (out / "REPORT.md").write_text("\n".join(lines) + "\n")
    print(json.dumps(summary["located_by"]), out)


if __name__ == "__main__":
    main()
