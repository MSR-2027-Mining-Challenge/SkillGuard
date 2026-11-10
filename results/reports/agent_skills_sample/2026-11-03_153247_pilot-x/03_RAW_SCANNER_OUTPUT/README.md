# Raw Cisco scanner output
The raw reports are **not copied** here: they stay in the source run folder, which is git-ignored because it holds exported, untrusted skill files. This folder holds an index of them with SHA-256 hashes, plus redacted copies of the small metadata files.
- Source folder: `results/cisco_dataset_runs/agent_skills_sample/runs/2026-11-03_153247_pilot-x`
- Per skill: `<skill_id>/manifest.json` (export provenance and file hashes), `only/SKILL.md`, `full/**` (exported files), `reports/<configuration>.json` (Cisco JSON exactly as printed) and `reports/<configuration>.run.json` (command, exit code, timing, stderr tail).
`raw_report_index.csv`: 4 report slots, 4 report files present, 4 hash(es) verified against the value recorded at scan time, 0 mismatch(es). Slots without a file are design exclusions or failures (see `status`).
Files: `raw_report_index.csv`, `scan_summary.csv` / `combined_scan_summary.csv`, `run_metadata.json` / `combined_metadata.json`, and the sample manifest when the run used one.
