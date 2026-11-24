# Research update: SkillGuard V3.2 and the three-scanner experiment

*Prepared 2026-11-23 for the mentor meeting. Details:*
- *[REPORT_next1000.md](REPORT_next1000.md): design, execution and numbers.*
- *[ANALYSIS_next1000.md](ANALYSIS_next1000.md): examples and interpretation.*

---

## 1. What we worked on since the last update

- Finished **SkillGuard V3.2** on a separate branch, with frozen V3.1 kept unchanged for comparison.
- Got **MalSkills** running locally and verified that it reproduces the teammate's earlier run. Finding and fixing two bugs in how it runs was a large part of this.
- Ran a **new 1,000-skill experiment** in which Cisco, MalSkills and SkillGuard scan exactly the same skills for the first time.
- Set aside a 250-skill **evaluation lockbox** for a future, cleaner evaluation.

## 2. What we improved in SkillGuard V3.2

The goal of SkillGuard is not to be another general code scanner. It focuses on **things that change what an AI agent is allowed to do, how it is configured, or who supervises it.**

Main changes since V3.1:
- **Taxonomy.** A proper taxonomy with nine categories. Every finding has a capability, an evidence level (code, config, metadata, instruction, documented example), and separate severity, confidence and review priority.
- **Two kinds of delegation.** Ordinary **sub-agent use** (the agent using its own Task tool) is now separated from **launching a different agent CLI** such as `codex exec` or `claude -p`. Only the second escapes the host agent's permission system.
- **New parsers:**
  - `allowed-tools` frontmatter, which tells scoped shell grants from unscoped `Bash`;
  - agent configuration files (Claude settings, hooks, MCP servers, Codex config);
  - JavaScript/TypeScript code.
- **Cross-file chains.** Behaviors are linked across files, e.g. "the skill pre-approves an unscoped shell *and* launches another agent with approvals disabled".
- **Validation:** 101 unit tests and a 65-case synthetic benchmark (141 checks, all pass). On 1,216 earlier skills, V3.2 keeps V3.1's findings except three deliberate drops, and it analyzes far more files (unanalyzed files fell from 1,235 to 397).

## 3. What we did in the new experiment

- **Sample.** 1,000 skills from the GitSkills database, stratified 400 / 300 / 300 by whether the skill has scripts, other supporting files, or only `SKILL.md`. These are the same strata and sizes as the earlier main1000 study. Every skill used in any earlier experiment (2,174 identities) was excluded, so all 1,000 are new.
- **Tools:**
  - Cisco skill-scanner 2.3.1: four configurations, plus its optional ATR rule pack as a fifth;
  - MalSkills (latest public commit, static mode);
  - SkillGuard V3.1 and V3.2.
- **Identical inputs.** Every exported file matched the database byte for byte. Folder checksums were verified before and after every scan.
- **Completion.**
  - MalSkills and SkillGuard: all 1,000 skills.
  - Cisco: 930 skills complete in all four configurations; 70 had a loader or analyzer error.
  - Run time: about 5.4 hours in four batches.
- **The MalSkills fixes:**
  - On macOS, MalSkills silently dropped every finding inside Markdown code blocks, because of a temp-folder symlink. After the fix it reproduces the earlier run exactly on 40/40 skills, against 18/40 before.
  - In folders containing several `SKILL.md` files, it sometimes scanned a subfolder instead of the skill. Our identity check caught this; we fixed it and re-ran that batch.

## 4. What Cisco detected

- **Headline:** 198 of 930 skills have a security finding in the main configuration (full folder, behavioral). That is 8.1% of the population once the strata are weighted; it was 9.6% in main1000.
- **Code drives it.** Nearly half of the skills with scripts are flagged (47%), but only 4–6% of the others. Scanning only `SKILL.md` finds about a tenth as many skills.
- **Common findings:** undeclared network access, outbound requests, `child_process` / `eval` patterns, unpinned dependencies.
- **Severity labels need reading next to the source.** One CRITICAL "eval" finding is on a line that only contains the *string* `"unsafe-eval allows eval()"`. A CRITICAL "exfiltration" finding is a `curl` that checks whether a deployed website responds.
- **The ATR pack fired on 899 of 941 skills (39,352 findings).** Its rules were written for live agent traffic. On documentation they match ordinary things: the word `bash` in a code fence, a `$TOKEN` placeholder, emoji.

## 5. What MalSkills detected

- **Two very different outputs:**
  - **Security-sensitive operations:** 491 of 1,000 skills. These are ordinary things like opening files, calling `subprocess`, installing packages.
  - **Malicious verdicts:** only **5** skills.
- **The four open malicious verdicts all come from one line of documentation piping a download into an interpreter.** Three are standard installers from the projects' own sites. One example is `curl -SsL https://get.riot.ml | sh -`, in the Riot project's own contributor skill. The fourth pipes a web page into `python3 -c` as *data* to parse; nothing downloaded is executed.
- **So a malicious verdict marks a structure, not intent.** We have not confirmed any of the five as malicious.

## 6. What SkillGuard detected

- **Headline:** 185 of 1,000 skills have a reviewable behavior (15.5% weighted). Only 9 have high review priority (0.26%).
- **Most common capabilities (whole sample):**
  - agent configuration modification (90 behaviors);
  - tool pre-approval (53);
  - approval-bypass instructions (36);
  - external agent launches (31);
  - schedulers (17) and MCP server definitions (15).
- **The high-priority cases are about delegation with safeguards turned down.** Good examples to discuss:
  - **`s-capture-loop`:** installs a daily cron job that runs `codex exec --yolo` on the skill's own instructions, i.e. an unattended agent with approvals and sandbox off. The finding comes from a *chain* linking `install.sh` (cron) and `capture-loop.sh` (agent launch); neither file shows it alone.
  - **`plan-multi-agent-review`:** pre-approves unscoped `Bash`, then launches six AI coding CLIs, one with `--allow-all-tools`. The skill openly documents which reviewers cannot be made read-only.
  - **`request-council-review`:** asks Claude, Codex and Grok to review documents, using `--dangerously-skip-permissions` and `--permission-mode bypassPermissions --always-approve`.
  - **`oci-functions-deploy`:** reads `~/.docker/config.json` credentials to check registry login before deploying. Plausible for its purpose, but it is credential access.
- **None of these high-priority skills was singled out by Cisco or MalSkills** (Cisco flagged three of them for unrelated lines).

## 7. What surprised us / what we learned

- **The tools barely look at the same things.**
  - Cisco and MalSkills largely agree: 183 of Cisco's 198 flagged skills also have MalSkills operations.
  - SkillGuard's findings rarely coincide with theirs at the line level: 5 of 246 behaviors near a Cisco alert, 32 near a MalSkills operation.
  - 53 skills are flagged by SkillGuard alone.
- **SkillGuard-only findings come from text and metadata, not code.** They are in instructions and `allowed-tools`, mostly in skills without scripts. That is exactly where the other tools do not look.
- **Our instruction detectors are imprecise.** Reading the open SkillGuard-only cases informally, roughly half of the approval-bypass and config-modification alerts look real. The rest are mentions, reads, or negations, e.g. *"Do not overwrite … without asking the user first"* was flagged as a bypass.
- **The new JS/TS and config parsers added coverage, not many findings.** Agent-steering in this population lives almost entirely in instructions and metadata.
- **Reproducing another tool is real work.** Without the two MalSkills fixes, our comparison would have quietly under-counted MalSkills on Markdown.

## 8. What our tool contributes

- **A different lens:** SkillGuard reports *agent-control* behavior (pre-approval, bypass, external agents, agent config, persistence), with the evidence level and file/line for each.
- **Cross-file evidence** that surfaces combinations a single-file view misses: a cron job plus an unattended agent run, or a pre-approved shell plus an external agent with bypass flags.
- **A reproducible comparison harness** for three scanners on identical inputs. It includes checks that would have caught both MalSkills problems automatically.

**What we can *not* claim yet:** that SkillGuard is more accurate, or that its distinct findings are real risks. There are no ground-truth labels.

## 9. What we should work on next

1. **A small, protocol-based human review:** sample alerts from each tool's distinct and shared regions, then evaluate a frozen version on the lockbox. This turns observations into precision numbers.
2. **Fix the instruction detectors:** negation ("never … without asking"), and telling *reads or mentions* of config files apart from *writes*.
3. **Deduplicate chain reporting:** one skill currently produces 16 chains.
4. **Optionally, run MalSkills and Cisco with their LLM stages,** to see whether the overlap pattern holds.
5. **Decide what to do about the lockbox exposure.** Lockbox outputs were briefly public on the branch. They are removed now but still in Git history; removing them fully would need a history rewrite and force-push, which is the team's decision.

---

### Questions to bring to the meeting

- Is "agent-control behavior" a strong enough framing for the paper, given that we cannot claim accuracy yet?
- How large should the human review be, and who labels? We need a protocol before looking at the lockbox.
- Should the lockbox be re-drawn because of the exposure, or kept with the exposure documented?
