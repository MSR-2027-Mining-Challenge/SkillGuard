"""Run the 4 batches of the approved 1,000-skill experiment sequentially (pilot-validated configuration).

    caffeinate -i .venv/bin/python -I results/skillguard_runs/main1000/run_main1000.py [first_batch]

For each batch b (default 1..4):
  1. notebook 01 via run_notebook.py with exactly the pilot settings (only the manifest and
     EXPERIMENT_NAME differ); the notebook file on disk is never modified;
  2. verify scan_summary.csv: 250 skills x 4 configurations = 1,000 rows, every scan executed; only
     explained PARTIAL/CONTRACT_ONLY statuses are accepted (see verify()). Anything else STOPS the whole job (exit code 2) so failures are investigated first;
  3. frozen SkillGuard V3.1 on the batch's exported folders (run_skillguard_on_run.py);
  4. restore the tracked results/reports/README.md and index.html (notebook 01's report step
     edits them); the generated per-run report folders are kept.
Progress is appended to main_run_log.jsonl (one JSON object per event).
"""

import csv
import datetime as dt
import json
import subprocess
import sys
import time
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
PY = str(REPO / ".venv/bin/python")
RUNS = REPO / "results/cisco_dataset_runs/agent_skills_sample/runs"
LOG = HERE / "main_run_log.jsonl"
PILOT_SETTINGS = ['RUN_MODE="scan"', 'SELECTION_MODE="manifest"', 'ALLOW_INCOMPLETE_FOLDERS=True', 'POLICY="balanced"',
                  'LENIENT=False', 'ENABLE_OSV=False', 'ENABLE_LLM_CONFIGS=False']
TRACKED_INDEX = ["results/reports/README.md", "results/reports/index.html"]


def log(**event):
    event["at"] = dt.datetime.now().astimezone().isoformat()
    with LOG.open("a", encoding="utf-8") as h:
        h.write(json.dumps(event) + "\n")
    print(json.dumps(event), flush=True)


def verify(run_dir, manifest):
    expected = {r["skill_id"] for r in csv.DictReader(manifest.open(encoding="utf-8"))}
    rows = list(csv.DictReader((run_dir / "scan_summary.csv").open(encoding="utf-8")))
    per_skill = Counter(r["skill_id"] for r in rows)
    statuses = Counter(r["status"] for r in rows)
    problems = []
    if len(rows) != 4 * len(expected):
        problems.append(f"{len(rows)} rows, expected {4 * len(expected)}")
    if set(per_skill) != expected:
        problems.append(f"skill set differs: missing {sorted(expected - set(per_skill))[:5]}, extra {sorted(set(per_skill) - expected)[:5]}")
    if any(n != 4 for n in per_skill.values()):
        problems.append("some skills do not have exactly 4 configurations")
    # Gate (revised after batch 1, see SCAN_STATUS_INVESTIGATION.md): every scan must have executed. PARTIAL is
    # accepted only when Cisco's skill_loader rejected the SKILL.md frontmatter (a deterministic property of
    # the input, identical in all 4 configurations); CONTRACT_ONLY only for the known FindingContract
    # UNKNOWN_BUNDLED_PYTHON_RULE issue. Anything else stops the job.
    def explained(r):
        d = r["status_detail"]
        if r["status"] == "COMPLETE":
            return True
        if r["status"] == "PARTIAL":
            # Revised after batch 4: the loader rejection may co-occur with the known contract issue, and
            # Cisco's YAML loader is stricter than the dataset's frontmatter_valid flag (e.g. "value---").
            fails = json.loads(r["analyzers_failed"] or "[]")
            loader = [f for f in fails if f["analyzer"] == "skill_loader" and f["error"].startswith("SkillLoadError:")]
            others = [f for f in fails if f not in loader]
            return r["scan_executed"] == "True" and len(loader) == 1 and all("UNKNOWN_BUNDLED_PYTHON_RULE" in f["error"] for f in others)
        if r["status"] == "CONTRACT_ONLY":
            return r["scan_executed"] == "True" and "UNKNOWN_BUNDLED_PYTHON_RULE" in d
        if r["status"] == "FAILED_SCANNER_ERROR":
            # Added after batch 3: Cisco refuses a SKILL.md that contains NUL bytes (present in the source DB text).
            cfg = r["configuration"].replace("SKILL.md only", "skill_only").replace("Full folder", "full_folder").replace(" | ", "_")
            rec = run_dir / r["skill_id"] / "reports" / f"{cfg}.run.json"
            try:
                tail = json.loads(rec.read_text(encoding="utf-8")).get("stderr_tail", "")
            except (OSError, json.JSONDecodeError):
                return False
            return "SKILL.md contains null bytes" in tail and b"\x00" in (run_dir / r["skill_id"] / "only/SKILL.md").read_bytes()
        return False
    bad = [(r["skill_id"], r["configuration"], r["status"], r["status_detail"][:120]) for r in rows if not explained(r)]
    if bad:
        problems.append(f"{len(bad)} unexplained non-COMPLETE scans: {bad[:10]}")
    partial = {r["skill_id"] for r in rows if r["status"] == "PARTIAL"}
    for s in {r["skill_id"] for r in rows if r["status"] == "FAILED_SCANNER_ERROR"}:
        if sum(1 for r in rows if r["skill_id"] == s and r["status"] == "FAILED_SCANNER_ERROR") != 4:
            problems.append(f"{s}: scanner refusal not consistent across the 4 configurations")
    for s in partial:
        if sum(1 for r in rows if r["skill_id"] == s and r["status"] == "PARTIAL") != 4:
            problems.append(f"{s}: frontmatter PARTIAL not consistent across the 4 configurations")
    walls = [float(r["wall_seconds"]) for r in rows if r["wall_seconds"]]
    return problems, {"rows": len(rows), "skills": len(per_skill), "statuses": dict(statuses),
                      "wall_mean_s": round(sum(walls) / len(walls), 3) if walls else None, "wall_sum_s": round(sum(walls), 1),
                      "incomplete_folder_skills": len({r["skill_id"] for r in rows if r["folder_complete"] != "True"}),
                      "partial_frontmatter_skills": len(partial),
                      "null_byte_refused_skills": len({r["skill_id"] for r in rows if r["status"] == "FAILED_SCANNER_ERROR"})}


def main():
    first = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    for b in range(first, 5):
        manifest = HERE / f"manifests/batch{b}_of4_manifest.csv"
        name = f"sample1000-seed2030-batch{b}"
        log(event="batch_start", batch=b, manifest=str(manifest.relative_to(REPO)))
        t0 = time.time()
        proc = subprocess.run([PY, "-I", str(HERE / "run_notebook.py"), "notebooks/01_cisco_scanner_dataset_ready.ipynb",
                               str(HERE / f"provenance/01_{name}_executed.ipynb"), *PILOT_SETTINGS,
                               f'SAMPLE_MANIFEST="{manifest.relative_to(REPO)}"', f'EXPERIMENT_NAME="{name}"'],
                              cwd=REPO, capture_output=True, text=True)
        runs = sorted(RUNS.glob(f"*_{name}"))
        if proc.returncode != 0 or not runs:
            log(event="notebook_failed", batch=b, returncode=proc.returncode, stderr_tail=proc.stderr[-3000:],
                run_dirs=[str(r.relative_to(REPO)) for r in runs])
            sys.exit(2)
        run_dir = runs[-1]
        problems, stats = verify(run_dir, manifest)
        log(event="batch_scanned", batch=b, run_dir=str(run_dir.relative_to(REPO)), minutes=round((time.time() - t0) / 60, 1),
            problems=problems, **stats)
        sg = subprocess.run([PY, "-I", str(HERE / "run_skillguard_on_run.py"), str(run_dir)], cwd=REPO, capture_output=True, text=True)
        log(event="skillguard_done", batch=b, returncode=sg.returncode, tail=(sg.stdout or sg.stderr)[-600:])
        restore = subprocess.run(["git", "checkout", "--", *TRACKED_INDEX], cwd=REPO, capture_output=True, text=True)
        log(event="tracked_index_restored", batch=b, returncode=restore.returncode, stderr=restore.stderr[-300:])
        if problems or sg.returncode != 0:
            log(event="stopped_for_investigation", batch=b)
            sys.exit(2)
    log(event="all_batches_done")


if __name__ == "__main__":
    main()
