"""Orchestrate the next 1,000-skill experiment (seed 2031) for one target: pilot or batch 1-4.

    caffeinate -i .venv/bin/python -I results/skillguard_runs/next1000/run_next1000.py pilot [--repeat]
    caffeinate -i .venv/bin/python -I results/skillguard_runs/next1000/run_next1000.py batch1   # ... batch4

Per target, in order (each step logs to run_log.jsonl and stops the job on failure):
  1. notebook 01 headless via main1000/run_notebook.py with the main1000 settings (manifest mode,
     4 core Cisco configurations, incomplete folders allowed and flagged); the notebook file on disk
     is never modified; the tracked results/reports index files it edits are restored afterwards;
  2. the main1000 status gate (verify() from main1000/run_main1000.py, unchanged);
  3. verify_export.py: exported bytes == DB text, folder manifests, missing-file accounting;
  4. run_cisco_atr.py: 5th Cisco configuration, full folder + behavioral + ATR rule pack;
  5. run_skillguard.py: frozen V3.1 and V3.2 on the same folders;
  6. MalSkills: malskills_runner.py prepare (byte copy + SHA256SUMS). If the environment variable
     MALSKILLS_BIN points to a MalSkills CLI, run + import as well; otherwise the step is logged as
     "pending: MalSkills not installed here" (MalSkills runs on the machine that has it, from the
     prepared corpus, then `malskills_runner.py import` is run here).
--repeat (pilot only) runs the SkillGuard and ATR steps a second time and compares outputs
(determinism check).
"""

from __future__ import annotations

import csv
import datetime as dt
import filecmp
import importlib.util
import json
import os
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
PY = str(REPO / ".venv/bin/python")
MAIN1000 = REPO / "results/skillguard_runs/main1000"
RUNS = REPO / "results/cisco_dataset_runs/agent_skills_sample/runs"
CORPORA = REPO / "results/malskills_corpus"  # local, untracked (contains skill files)
LOG = HERE / "run_log.jsonl"
SETTINGS = ['RUN_MODE="scan"', 'SELECTION_MODE="manifest"', 'ALLOW_INCOMPLETE_FOLDERS=True', 'POLICY="balanced"',
            'LENIENT=False', 'ENABLE_OSV=False', 'ENABLE_LLM_CONFIGS=False']
TRACKED_INDEX = ["results/reports/README.md", "results/reports/index.html"]
TARGETS = {"pilot": "pilot12_manifest.csv", **{f"batch{b}": f"batch{b}_of4_manifest.csv" for b in range(1, 5)}}


def log(**event):
    event = json.loads(json.dumps(event).replace(str(REPO) + "/", "").replace(str(REPO), "."))  # no absolute paths
    event["at"] = dt.datetime.now().astimezone().isoformat(timespec="seconds")
    with LOG.open("a", encoding="utf-8") as h:
        h.write(json.dumps(event) + "\n")
    print(json.dumps(event), flush=True)


def step(name, args, target):
    t0 = time.time()
    proc = subprocess.run(args, cwd=REPO, capture_output=True, text=True, env=dict(os.environ, PYTHONPATH=str(REPO / "src")))
    log(event=name, target=target, returncode=proc.returncode, seconds=round(time.time() - t0, 1),
        tail=(proc.stdout or "")[-800:], stderr_tail=(proc.stderr or "")[-800:] if proc.returncode else "")
    if proc.returncode != 0:
        log(event="stopped_for_investigation", target=target, at_step=name)
        sys.exit(2)
    return proc


def main():
    target = sys.argv[1]
    repeat = "--repeat" in sys.argv
    manifest = HERE / "manifests" / TARGETS[target]
    name = f"next1000-seed2031-{target}"
    log(event="target_start", target=target, manifest=str(manifest.relative_to(REPO)))
    t0 = time.time()
    proc = subprocess.run([PY, "-I", str(MAIN1000 / "run_notebook.py"), "notebooks/01_cisco_scanner_dataset_ready.ipynb",
                           str(HERE / f"provenance/01_{name}_executed.ipynb"), *SETTINGS,
                           f'SAMPLE_MANIFEST="{manifest.relative_to(REPO)}"', f'EXPERIMENT_NAME="{name}"'],
                          cwd=REPO, capture_output=True, text=True)
    restore = subprocess.run(["git", "checkout", "--", *TRACKED_INDEX], cwd=REPO, capture_output=True, text=True)
    runs = sorted(RUNS.glob(f"*_{name}"))
    log(event="notebook01", target=target, returncode=proc.returncode, minutes=round((time.time() - t0) / 60, 1),
        index_restored=restore.returncode == 0, run_dirs=[r.name for r in runs],
        stderr_tail=proc.stderr[-2000:] if proc.returncode else "")
    if proc.returncode != 0 or not runs:
        sys.exit(2)
    run_dir = runs[-1]
    spec = importlib.util.spec_from_file_location("run_main1000", MAIN1000 / "run_main1000.py")
    gate = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(gate)
    problems, stats = gate.verify(run_dir, manifest)
    log(event="status_gate", target=target, problems=problems, **stats)
    if problems:
        log(event="stopped_for_investigation", target=target, at_step="status_gate")
        sys.exit(2)
    step("verify_export", [PY, "-I", str(HERE / "verify_export.py"), str(run_dir)], target)
    step("cisco_atr", [PY, "-I", str(HERE / "run_cisco_atr.py"), str(run_dir)], target)
    step("skillguard", [PY, "-I", str(HERE / "run_skillguard.py"), str(run_dir)], target)
    corpus = CORPORA / run_dir.name
    step("malskills_prepare", [PY, "-I", str(HERE / "malskills_runner.py"), "prepare", str(run_dir), str(corpus)], target)
    if os.environ.get("MALSKILLS_BIN"):
        out = CORPORA / f"{run_dir.name}__malskills_output"
        step("malskills_run", [PY, "-I", str(HERE / "malskills_runner.py"), "run", str(corpus), str(out),
                               "--malskills-bin", os.environ["MALSKILLS_BIN"]], target)
        step("malskills_import", [PY, "-I", str(HERE / "malskills_runner.py"), "import", str(out), str(run_dir)], target)
    else:
        log(event="malskills_pending", target=target, corpus=str(corpus.relative_to(REPO)),
            note="MalSkills not installed here; run it on the prepared corpus, then malskills_runner.py import")
    if repeat:
        for sub, script in (("skillguard", "run_skillguard.py"), ("cisco_atr", "run_cisco_atr.py")):
            first = HERE / sub / run_dir.name
            saved = first.with_name(first.name + "__run1")
            first.rename(saved)
            step(f"{sub}_repeat", [PY, "-I", str(HERE / script), str(run_dir)], target)
            names = ["findings.csv", "scans.csv"] if sub == "cisco_atr" else \
                ["v31_behaviors.csv", "v32_behaviors.csv", "v32_chains.csv", "v32_coverage.csv"]
            same = {n: filecmp.cmp(saved / n, first / n, shallow=False) for n in names}
            if sub == "cisco_atr":  # timing column differs between runs; compare without it
                rows = lambda p: [{k: v for k, v in r.items() if k != "seconds"} for r in csv.DictReader(p.open())]
                same["scans.csv"] = rows(saved / "scans.csv") == rows(first / "scans.csv")
            log(event=f"{sub}_determinism", target=target, identical=same)
    log(event="target_done", target=target, run_dir=run_dir.name, minutes=round((time.time() - t0) / 60, 1))


if __name__ == "__main__":
    main()
