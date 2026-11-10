# RQ2 — Defect Taxonomy and Operational Codebook (v0.1)

**Project:** MSR 2027 · SkillGuard  |  **Status:** proposed study codebook, not validated results  |  **Date:** 2026-11-09

## 1. Sources and scope

- **Primary categories and rule IDs:** Zhang et al., *What Keeps Agent Skills from Being Reusable?* [Section 3.2 / Figure 1](https://arxiv.org/abs/2608.08453): R1–R7, **31 checks**. We retain their identifiers, but the operational criteria and exclusions below are **our reproducible study implementation**, not necessarily identical to the paper’s released detector.

- **Supplementary vocabulary:** Hong et al., *From Anatomy to Smells* [Table III](https://arxiv.org/abs/2607.01456): 26 skill smells. The crosswalk below prevents double counting overlapping phenomena.

- **Normative baseline:** [Agent Skills specification](https://agentskills.io/specification). Its mandatory constraints differ from published quality heuristics.

- **New full-folder extension:** P1–P5, introduced here to assess problems not observable in SKILL.md alone. They are not claimed as categories from either paper.

**Important:** Neither a matching string nor a scanner alert establishes a security vulnerability or a task failure. The initial label is a *candidate*.

## 2. Category-level taxonomy

| Family | Category | Original checks | Analysis target |
|---|---|---:|---|
| R1 | Routing Metadata | 6 | Metadata-only selection and trigger clarity |
| R2 | Body Content | 5 | Actionability and context efficiency |
| R3 | Resource Organization | 3 | Progressive disclosure and examples |
| R4 | Prohibited Content | 4 | Boilerplate and unfinished instructions |
| R5 | Behavioral Safety | 6 | Sensitive actions, credentials, trust boundaries |
| R6 | Portability | 4 | Host/model/OS/environment assumptions |
| R7 | Persona & Scope | 3 | Identity conflicts, inappropriate task boundaries |

### Baseline specification preflight (separate from the 31 published checks)

These four simple checks are performed first and reported separately to avoid treating recommendations as mandatory constraints.

| ID | Condition | Repair |
|---|---|---|
| **S1 — Missing SKILL.md** | skill folder does not contain SKILL.md exactly where required | Add SKILL.md |
| **S2 — Invalid YAML frontmatter** | frontmatter missing delimiters or is not parseable as expected YAML mapping | Repair YAML |
| **S3 — Invalid skill name** | name absent, malformed, >64, consecutive hyphens, or does not equal parent directory | Correct name and directory |
| **S4 — Invalid description length** | description absent/empty or >1024 characters | Correct description |

**Normative/heuristic distinction:** The spec requires nonempty `name` and `description`, `name` length ≤64 and matching the directory name, and `description` length ≤1024. It **recommends** (not requires) keeping the body under 500 lines and organizing resources for progressive disclosure. Zhang et al. use a **30-character lower and 300-character upper** description heuristic; a 301-character description is *not* itself a spec violation.

## 3. Reproducible checks (R1–R7; adapted from the published taxonomy)

### R1 — Routing Metadata

| Rule | Candidate detection criterion | Exclusion / evidence standard | Method |
|---|---|---|---|
| **R1.1 Missing description** | Parsed YAML frontmatter has no description key or its trimmed value is empty. | Treat YAML parse failures separately under S02; do not treat an empty description as a missing trigger phrase. | static |
| **R1.2 Description too short** | Description length after trim is <30 Unicode characters. | This 30-character threshold comes from the study, not the official minimum of one character. | static |
| **R1.3 Missing trigger guidance** | Description conveys the action but never states a usage condition, triggering situation, or task type. | Do not require literal words "Use when"; equivalent language counts. | hybrid |
| **R1.4 Non-functional description** | Description fails to identify a concrete capability or differentiating outcome (e.g., "helps with things"). | Short yet precise descriptions are not automatically nonfunctional. | manual |
| **R1.5 Overlong routing description** | Description length after trim >300 characters (paper Figure 1 baseline). | 301–1024 characters violates the paper heuristic but not the official 1024-character maximum; >1024 is S04. | static |
| **R1.6 Routing guidance only in body** | Body contains explicit when-to-use/trigger guidance missing from the description. | A trigger included in both locations is fine. | hybrid |

### R2 — Body Content

| Rule | Candidate detection criterion | Exclusion / evidence standard | Method |
|---|---|---|---|
| **R2.1 Oversized body** | SKILL.md Markdown body has >500 physical lines, excluding frontmatter. | The 500-line target is guidance, not an invalid SKILL.md format. | static |
| **R2.2 Non-actionable body** | Body does not give identifiable instructions, constraints, or executable decisions for its stated task. | An information-reference skill can be useful without numbered steps. | manual |
| **R2.3 Explains obvious** | Body spends substantive space defining generic concepts not needed to perform the advertised task. | Domain-specific prerequisites and safety explanations are not redundant. | manual |
| **R2.4 Name repeated as H1** | First H1 of body is textually identical to frontmatter name after lowercasing, replacing hyphens/underscores with spaces and trimming punctuation. | A descriptive H1 that adds additional words does not trigger. | static |
| **R2.5 Description duplicated in body** | First body paragraph repeats the full description verbatim after collapsing whitespace and case. | Partial elaboration or paraphrase is not a verbatim duplicate. | static |

### R3 — Resource Organization

| Rule | Candidate detection criterion | Exclusion / evidence standard | Method |
|---|---|---|---|
| **R3.1 Excessive inline code** | More than 60% of nonblank body lines lie inside fenced code blocks. | Ratio is our reproducible implementation of the paper threshold, not a claim about its original exact parser. | static |
| **R3.2 Too many code examples** | More than eight fenced code blocks occur in the SKILL.md body. | Code blocks are a proxy for examples; a block containing essential output syntax may not be an example. | static |
| **R3.3 Monolithic skill without resources** | Body >300 lines AND the package has no scripts/ or references/ files that are actually referenced. | 300 is an explicit project pilot threshold; tune in sensitivity analysis and do not attribute it to the paper. | hybrid |

### R4 — Prohibited Content

| Rule | Candidate detection criterion | Exclusion / evidence standard | Method |
|---|---|---|---|
| **R4.1 Installation instructions in body** | SKILL.md contains explicit package/plugin installation steps unrelated to executing the skill. | Required runtime setup may be legitimate; do not classify all pip/npm commands as a defect. | hybrid |
| **R4.2 Changelog in active instructions** | Body includes a CHANGELOG/Version History section with historical entries. | A version constraint for an API is not a changelog. | static |
| **R4.3 License boilerplate in body** | Body reproduces a full copyright/license clause instead of referring to LICENSE. | A brief legally necessary usage restriction is not automatically problematic. | hybrid |
| **R4.4 Unfinished markers** | Operational prose contains TODO, FIXME, TBD, or a placeholder requiring completion. | Do not count markers in explicitly labeled examples or code demonstrating how to find TODOs. | static |

### R5 — Behavioral Safety

| Rule | Candidate detection criterion | Exclusion / evidence standard | Method |
|---|---|---|---|
| **R5.1 Hardcoded credentials** | Static content contains a plausible live API key, token, password, or private key intended for reuse. | Synthetic examples, placeholders, and public test vectors are not confirmed exposures. Never reproduce credential values in reports. | hybrid |
| **R5.2 Safety bypass instruction** | Active instructions/scripts disable integrity or safety controls (e.g., --no-verify, disabled certificate verification). | A quotation in security-training documentation is not an active bypass. | hybrid |
| **R5.3 Instruction hierarchy / injection pattern** | Skill instructs the agent to ignore higher-priority instructions, or asks it to follow untrusted data as authoritative commands. | Legitimate defensive examples and quotations are not automatically attacks. | manual |
| **R5.4 Unguarded destructive actions** | Active steps can erase/overwrite data, change cron/jobs, or terminate unrelated processes without a stated scope check, preview, or user approval where material. | Expected, narrow, user-authorized operations with adequate scope guards are not automatically defects. | hybrid |
| **R5.5 Error suppression** | Exceptions/nonzero exits that materially affect success are silently discarded and workflow reports success. | Best-effort cleanup with documented tolerable failure can be appropriate. | hybrid |
| **R5.6 User-specific path leakage** | Literal absolute path exposes an individual home directory/account/machine path not required by functionality. | Generic example paths and env-based path expansion are not user leakage. | hybrid |

### R6 — Portability

| Rule | Candidate detection criterion | Exclusion / evidence standard | Method |
|---|---|---|---|
| **R6.1 Hardcoded model name** | Task is broadly advertised but requires a specific named LLM model with no supported alternative. | A skill explicitly intended for that model is not necessarily defective. | hybrid |
| **R6.2 Platform-specific hardcoded paths** | Hardcoded Windows drive or Unix absolute path is required for operation but not documented or parameterized. | Generic /tmp and user-supplied paths may be intentional; Windows backslash notation is not itself a defect. | hybrid |
| **R6.3 Platform-specific tool calls** | Instructions require an agent-host-specific tool/API without stating platform compatibility or fallback. | Platform-scoped skill with explicit compatibility is acceptable. | hybrid |
| **R6.4 OS-specific commands** | Essential command is OS-specific (e.g., pbcopy, apt, crontab) but no OS requirement or alternative is documented. | Explicitly platform-scoped skills are not automatically defective. | hybrid |

### R7 — Persona & Scope

| Rule | Candidate detection criterion | Exclusion / evidence standard | Method |
|---|---|---|---|
| **R7.1 Persona redefinition** | Skill orders agent to assume a conflicting primary identity or overarching role rather than a bounded task role. | Task personas ("act as a code reviewer") can be benign. | manual |
| **R7.2 Overrides prior instructions** | Active directive claims precedence over system/developer/user rules or instructs to ignore earlier constraints. | Quoting malicious prompts in defensive material is not an active override. | manual |
| **R7.3 Scope mismatch** | Body/script performs an unrelated task or requests privileges/data not implied by description. | Necessary internal subtasks are not automatically out of scope. | manual |

## 4. Proposed package-level checks (new to SkillGuard)

These checks use **full folder** evidence. Do not merge their prevalence with the paper’s 31-check prevalence without reporting the expanded operationalization.

| ID | Defect / testable signal | Exclusions | Verification / fix |
|---|---|---|---|
| **P1 — Broken supporting-file reference** | An explicit relative path or Markdown link in SKILL.md/reference points to a file absent from the complete skill package. | Ignore URLs, templated paths, documented generated files, or deliberately external paths. | Resolve relative to skill root with symlink containment checks; record broken path. **Fix:** Fix link or include file. |
| **P2 — Undocumented runtime dependency** | Referenced executable script requires a nonstandard executable/library/service absent from documented prerequisites/compatibility. | A dependency bundled in repo or standard with declared platform is satisfied. | Parse imports and subprocess targets; compare requirements/config and docs. **Fix:** Declare/install/replace dependency or provide fallback. |
| **P3 — Instruction–implementation contradiction** | Active SKILL.md instructions and actual script interface/behavior disagree (flags, file locations, returned fields, effect). | Multiple compatible usage modes are not contradictions. | Trace one claim to implementation/test and record both line ranges. **Fix:** Update instruction or script and add regression test. |
| **P4 — Unprotected side effect in supporting script** | Referenced script modifies persistent jobs, files, system state, or network targets beyond advertised behavior without adequate guardrails. | Normal user-requested side effects with safe target and scope are not defects. | Static data-flow and guard review; test in hermetic fixture if appropriate. **Fix:** Add authorization, target constraints, preview/rollback. |
| **P5 — Reproducible functional correctness failure** | A normal documented use case produces wrong output, wrong timing, a crash, or incompatible artifact, verified with safe deterministic test. | Speculative possible errors without a demonstrable supported input do not count. | Create minimal expected-vs-actual fixture in sandbox, no untrusted execution on host. **Fix:** Patch logic and prove regression passes. |

## 5. Mapping the 26 skill smells to this codebook

The 26 names/acronyms below come from Hong et al. Table III. The mapping is our interpretation and **does not imply that the smells and R codes are logically equivalent**.

| Smell | Source category | Related code(s) | Caveat |
|---|---|---|---|
| **TSW** — The Stepless Workflow | Under-Specified Guidance | R2.2 | Partial overlap; workflow quality |
| **TOB** — The Option Buffet | Under-Specified Guidance | R2.2 | Partial overlap; unclear default selection |
| **MUS** — Missing Utility Script | Under-Specified Guidance | (no direct equivalent) | No direct counterpart; track as separate skill-smell if relevant |
| **MDT** — Missing Decision Tree | Under-Specified Guidance | R2.2 | No strict equivalent |
| **SOC** — Series of Commands | Over-Prescribed Guidance | R2.2 | Potentially conflicts with a deliberately deterministic workflow |
| **NVS** — No Validation Step | Missing Verification & Feedback Loop | (no direct equivalent) | No direct counterpart; missing validation is not itself a reproduced P5 failure |
| **EWP** — Execute Without a Plan | Missing Verification & Feedback Loop | R5.4 | Only overlapping for high-impact actions |
| **NAH** — Never Asks Human | Missing Verification & Feedback Loop | R5.4 | Only overlapping when user approval is warranted |
| **RL** — Rationalization Loophole | Missing Follow-Through Guards | R2.2 | Weak conceptual link only; no exact equivalent |
| **NPT** — No Progress Tracking | Missing Follow-Through Guards | R2.2 | No exact equivalent; multi-step work only |
| **UD** — Undelegated Detail | Context Bloat | R3.1, R3.3 | Close overlap |
| **LSB** — Lengthy Skill Body | Context Bloat | R2.1 | Different thresholds: 5000 words vs 500 lines |
| **LSN** — Lengthy Skill Name | Context Bloat | S3 | Same official 64-character maximum |
| **LSD** — Lengthy Skill Description | Context Bloat | S4, R1.5 | 1024 official chars vs 300 heuristic |
| **CSD** — Confusing Skill Description | Context Bloat | R1.3, R1.4 | Close semantic overlap |
| **NG** — No Guardrails | Missing Safeguards | R5.4 | Only when guarded action is relevant |
| **BG** — Buried Gotchas | Missing Safeguards | R2.2 | No exact equivalent; information placement |
| **MUR** — Missing Usage Rules | Missing Safeguards | R1.3 | Partial overlap with trigger guidance |
| **MC** — Missing Caveats | Missing Safeguards | R2.2 | No exact equivalent |
| **ME** — Missing Example | Inadequate Contextual Grounding | R2.2 | No exact equivalent; examples not mandatory |
| **TSS** — Time Sensitive Skill | Inadequate Contextual Grounding | P5 | Only when stale time assumption causes demonstrable failure |
| **XID** — XML Included Description | Security Hazard | R5.3 | Potential injection marker; no proof of actual exploit |
| **BP** — Backslash Path | Convention & Style Violations | R6.2 | Not equivalent; Windows paths can be valid |
| **USN** — Unclear Skill Name | Convention & Style Violations | R1.4 | Name quality vs description quality; only indirect overlap |
| **NTPD** — Non Third Person Description | Convention & Style Violations | R1.4 | Stylistic; not a direct routing failure |
| **MT** — Missing Template | Unstructured Output | P3 | Only when output format promised but implementation lacks it |

## 6. Standardized review protocol

**Unit of analysis.** One finding instance per `skill SHA-256 + rule ID + normalized file path + evidence span`. Track a separate `behavior_id` when two rules or locations refer to one underlying behavior. Count scanner configurations separately only for RQ1, not as independent defects.

**Screening.** Record `SKILL_md_only` or `full_folder`, visible evidence, source lines, relevant instruction context, proposed impact, and repair. A static rule yields a *candidate*, not a confirmed defect.

**Verification.** The candidate CSV uses `candidate`, `confirmed_in_snapshot`, `confirmed_defect`, `likely_false_positive`, `false_positive`, `unresolved`, and `not_evaluable`. Record a rationale and supporting evidence before changing a status; use `textual_only`, `source_verified`, or `test_reproduced` when available.

**Researcher investigation.** The researcher inspects each candidate against its trigger and exclusion criteria and records a preliminary status, impact, recommended fix, and investigation notes. For semantic rules (R2.2, R5.3, R7.3), notes identify the exact instruction and explain whether exclusion criteria apply. No agreement or adjudication statistic is claimed by this workflow.

**Evidence and remediation.** Main row fields include `candidate_id, skill_id, rule_id, file_path, line_number, signal, supporting_excerpt, candidate_status, impact, recommended_fix, investigation_notes`. Compare `SKILL.md`-only and full-folder evidence for each candidate when both are available.

**Execution safety.** Do not run scraped Python/shell or any skill-referenced script on a workstation. Prefer AST/text inspection; reproduce a logic bug only in a disposable container with no sensitive credentials, restricted file access, and no outbound network.

## 7. Pilot starting set (9 priority defect checks + 4 baseline preflight checks)

Prioritize **S1–S4**, **R1.3**, **R3.1**, **R5.1**, **R5.4**, **R6.4**, **P1**, **P2**, **P3**, and **P5** for initial tool prototyping; S1–S4 are counted as a single preflight stage. Report both check-level and behavior-level counts. This subset is a practical pilot, *not* a published list.

## 8. Example anchored to the existing sample

`set-reminder`: the code maps a datetime to cron fields `minute hour day month *`, omitting the year. A normal future target with a different year can be scheduled in an earlier year. Under **P5**, this is a **candidate functional scheduling defect** until a controlled fixture demonstrates expected-versus-actual behavior. Its outbound Telegram request is not automatically R5 malicious exfiltration; sending reminders is the skill’s advertised purpose. A Cisco `allowed-tools` parser issue should not be recoded as an actual skill defect.

## 9. Thresholds and sensitivity

Freeze the thresholds above before scoring (R1.2 <30, R1.5 >300, R2.1 >500, R3.1 >60%, R3.2 >8, P/R3.3 project threshold >300 lines). Independently report normatively invalid files and heuristic candidates. For R3.1 and R3.3, rerun a sensitivity comparison (e.g., 50/60/70% and 250/300/500 lines) instead of treating threshold-dependent results as objective truth.

## 10. Sources

1. Zhang et al. (2026), *What Keeps Agent Skills from Being Reusable? Evidence from 138K SKILL.md Files*, §3.2, Figure 1. https://arxiv.org/abs/2608.08453
2. Hong, Imani & Ahmed (2026), *From Anatomy to Smells: An Empirical Study of SKILL.md in Agent Skills*, Table III. https://arxiv.org/abs/2607.01456
3. Agent Skills Specification. https://agentskills.io/specification
