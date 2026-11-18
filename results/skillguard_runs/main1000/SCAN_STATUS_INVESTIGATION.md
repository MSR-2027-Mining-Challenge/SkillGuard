> Investigation notes for the scan-status gate in all three pauses of the 1,000-skill run (batches 1, 3 and 4). The file was renamed from `BATCH1_INVESTIGATION.md` on 2026-11-17; `main_run_log.jsonl` still uses the old name.

# Batch 1 stop: investigation (2026-11-15)

`run_main1000.py` stopped after batch 1 (exit 2). The stop came from the batch gate, not from a crash. All 1,000 Cisco scans (250 skills × 4 configurations) **executed**, produced valid reports, and were recorded. Of these, 937 were `COMPLETE`, 60 `PARTIAL` and 3 `CONTRACT_ONLY`. The gate stopped the job because it accepted only `COMPLETE`, which is stricter than the pilot runbook's requirement of "an executed status".

## The 63 non-COMPLETE scans

| Status | Scans | Skills | Cause |
|---|---|---|---|
| `PARTIAL` | 60 | 15 | Cisco's `skill_loader` rejected the SKILL.md frontmatter: `MISSING_REQUIRED_MANIFEST_FIELD` (48 scans, 12 skills) or `MALFORMED_YAML_FRONTMATTER` (12 scans, 3 skills). It happens in all 4 configurations of each skill. |
| `CONTRACT_ONLY` | 3 | 3 | Full folder, behavioral mode: the known Cisco `FindingContract` / `UNKNOWN_BUNDLED_PYTHON_RULE` registration error (notebook 01 §5) |

**Checks**

- All 60 `PARTIAL` rows have `frontmatter_valid = 0`.
- 11 of the 15 skills have no `---` frontmatter at all; their SKILL.md starts with a Markdown heading.
- The others use non-standard fields, for example `title:` instead of `name:`, or YAML that does not parse.
- The cause is a fixed property of the input file, so re-scanning would give the same result. Cisco still ran its other analyzers: every `PARTIAL` scan has at least 1 finding (usually the manifest finding).
- 12 `COMPLETE` rows (3 skills) also have `frontmatter_valid = 0`. Cisco tolerated their frontmatter.

**How these scans are used.** Notebook 01 already excludes `PARTIAL` and `CONTRACT_ONLY` findings from its primary tables. The consolidated analysis does the same: **primary analyses use `COMPLETE` scans**, and these scans appear separately as a scan-execution and coverage category.

## Gate change (batches 2–4)

`verify()` now accepts only these statuses:

- `COMPLETE`
- `PARTIAL`, only when it is executed, has exactly one analyzer failure (`skill_loader: SkillLoadError:*`), has `frontmatter_valid = 0`, and occurs in all 4 configurations
- `CONTRACT_ONLY`, only with `UNKNOWN_BUNDLED_PYTHON_RULE`

Anything else (failed, timed out, missing report, other analyzer failures, wrong row or skill counts) still stops the job. Re-verifying batch 1 with the revised gate: 0 problems.

The batch-1 run folder, SkillGuard output and log were kept unchanged. The job resumed with `run_main1000.py 2`.

# Batch 3 stop: investigation (2026-11-16)

Batch 2 passed the gate (900 `COMPLETE`, 96 `PARTIAL` from 24 frontmatter skills, 4 `CONTRACT_ONLY`). Batch 3 stopped on 4 `FAILED_SCANNER_ERROR` scans, all from one skill, `android-icon-processing-fdd8ec963741` (`ZHLX2005/fr`). The scan failed with exit code 1 and no JSON in all 4 configurations.

**Cause.** Cisco's stderr says: `Error loading skill: SKILL.md contains null bytes (binary content is not allowed)`.

- The exported SKILL.md has exactly one NUL byte, at offset 2605, inside a code example: `.convert("RG\x00BA")`.
- The same NUL is present in the source text in `data/sample/agent_skills_sample.db` (`artifacts.content`).
- Export did not introduce it: the sha256 matches the manifest.
- It is the **only** artifact in the sample DB with a NUL byte.
- Cisco 2.3.1 refuses such files by design, so re-scanning would fail the same way.

**How this skill is used.**

- **Cisco:** it has no Cisco result. It is excluded from the primary Cisco analysis set and listed under scan-execution limitations.
- **SkillGuard V3.1:** it analyzed the folder normally.

**Gate change (batch 4).** `FAILED_SCANNER_ERROR` is accepted only when all three conditions hold:

- the `.run.json` stderr contains `SKILL.md contains null bytes`
- the exported SKILL.md really contains a NUL byte
- it happens in all 4 configurations

Re-verifying batches 1–3 with the revised gate: 0 problems. The job resumed with `run_main1000.py 4`.

# Batch 4 stop: investigation (2026-11-16)

All 1,000 scans executed (943 `COMPLETE`, 52 `PARTIAL`, 5 `CONTRACT_ONLY`). The gate rejected 5 `PARTIAL` scans from 2 skills. Both have known causes, but they are combinations the gate rule did not yet allow:

1. **`translation-skill-a6e365bea591`:** the SKILL.md frontmatter is rejected (`MISSING_REQUIRED_MANIFEST_FIELD`) in all 4 configurations. In *Full folder | behavioral*, the known `UNKNOWN_BUNDLED_PYTHON_RULE` contract errors also occur, giving 3 analyzer failures in that one scan.
2. **`engineering-mobile-app-builder-f7310f56891a`:** Cisco reports `MALFORMED_YAML_FRONTMATTER` in all 4 configurations, while the dataset has `frontmatter_valid = 1`. The closing delimiter is glued to the previous line (`owner: Your Organization---`): the dataset's lenient parser accepts this, and Cisco's YAML loader does not. The cause is still in the input; the two parsers disagree.

**Gate change.** `PARTIAL` is accepted when the scan executed, there is exactly one `skill_loader` `SkillLoadError`, and any other analyzer failures are only the known `UNKNOWN_BUNDLED_PYTHON_RULE` contract errors. The condition `frontmatter_valid = 0` was dropped. The 4-configuration consistency check stays.

Re-verifying batches 1–4 with the final gate: 0 problems in each. **All four batches are accepted.** The final scan-status mix for 4,000 scans:

- 3,712 `COMPLETE`
- 272 `PARTIAL` (68 skills)
- 12 `CONTRACT_ONLY`
- 4 `FAILED_SCANNER_ERROR` (1 skill)
