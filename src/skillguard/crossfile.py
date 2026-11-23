"""Cross-file evidence: instruction -> file links, declared vs observed tools, combinations.

* Links: Markdown instructions (SKILL.md and other .md files) that run or reference files of
  the skill, e.g. ``python scripts/setup.py``, ``bash ${CLAUDE_SKILL_DIR}/scripts/x.sh``,
  ``node ~/.claude/skills/<name>/tool.js`` or a Markdown link. A link is ``executes`` when the
  path is used as a command (interpreter + path, or the path as the program) and
  ``references`` otherwise.
* Declared tools: the SKILL.md frontmatter ``allowed-tools`` value is parsed with the
  ``Tool(pattern)`` grammar (commas inside parentheses do not split entries) and compared with
  what the skill observably needs.
* Chains: combinations of findings that deserve review together (taxonomy.CHAINS). Every chain
  lists its member findings and the scope that connects them (same file, linked files, or only
  the same skill). Chains are risk indicators, never verdicts.
"""

from __future__ import annotations

import posixpath
import re
import shlex

import yaml

from . import engine as E
from . import taxonomy as T
from .configs import _NoAliasLoader

EXEC_SUFFIXES = (".py", ".sh", ".bash", ".zsh", ".js", ".mjs", ".cjs", ".ts", ".mts", ".cts", ".ps1", ".psm1", ".rb",
                 ".pl", ".php", ".lua")
INTERPRETERS = {"python", "python3", "python2", "py", "bash", "sh", "zsh", "node", "deno", "bun", "tsx", "ts-node",
                "pwsh", "powershell", "ruby", "perl", "php", "source", ".", "uv", "npx", "pnpm", "yarn", "lua"}
PATH_PREFIX = re.compile(
    r"^(?:\$\{?[A-Za-z_][A-Za-z0-9_]*\}?/|\{[A-Za-z_]+\}/|<[^>/]+>/|~?/?\.?(?:claude|codex|cursor|agents)/skills/[^/]+/"
    r"|\./)+")
PATH_TOKEN = re.compile(r"(?<![\w/.-])((?:[\w${}<>~.-]+/)*[\w.-]+\.(?:py|sh|bash|zsh|js|mjs|cjs|ts|mts|cts|ps1|rb|pl"
                        r"|json|ya?ml|toml|md))(?![\w/])")
MD_LINK = re.compile(r"\[[^\]]*\]\(([^)\s#]+)")
RUN_VERB = re.compile(r"(?i)\b(?:run|execute|invoke|call|launch|start)\b")


# ---------------------------------------------------------------------------
# Frontmatter and allowed-tools
# ---------------------------------------------------------------------------

def frontmatter(text):
    """(mapping or None, error or None, end_line)."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None, None, 0
    end = next((i for i in range(1, len(lines)) if lines[i].strip() in {"---", "..."}), None)
    if end is None:
        return None, "unterminated_frontmatter", 0
    try:
        data = yaml.load("\n".join(lines[1:end]), Loader=_NoAliasLoader)
    except yaml.YAMLError as exc:
        return None, f"invalid_yaml:{exc.__class__.__name__}", end + 1
    return (data if isinstance(data, dict) else None), None, end + 1


def parse_allowed_tools(value):
    """Parse allowed-tools (string or list). Returns [{"tool", "pattern", "raw"}].

    Entries are separated by commas or whitespace outside parentheses, so
    ``Bash(git add:*), Read`` -> Bash with pattern "git add:*", and Read."""
    items = []
    if isinstance(value, list):
        raw_items = [str(v) for v in value]
    elif isinstance(value, str):
        raw_items, depth, cur = [], 0, ""
        for ch in value:
            if ch == "(":
                depth += 1
            elif ch == ")":
                depth = max(0, depth - 1)
            if depth == 0 and (ch == "," or ch.isspace()):
                if cur.strip():
                    raw_items.append(cur.strip())
                cur = ""
                continue
            cur += ch
        if cur.strip():
            raw_items.append(cur.strip())
    else:
        return items
    for raw in raw_items:
        m = re.fullmatch(r"\s*([A-Za-z_][\w:*-]*)\s*(?:\((.*)\))?\s*", raw, re.S)
        if m:
            items.append({"tool": m.group(1), "pattern": (m.group(2) or "").strip(), "raw": raw})
        else:
            items.append({"tool": raw, "pattern": "", "raw": raw})
    return items


def _pattern_covers(pattern, command):
    """Claude-Code-style Bash pattern match: 'npm run test:*' (prefix), globs with *."""
    p = pattern.strip()
    if p in {"", "*"}:
        return True
    if p.endswith(":*"):
        return command.startswith(p[:-2])
    regex = "^" + re.escape(p).replace(r"\*", ".*") + "$"
    return bool(re.match(regex, command)) or command.startswith(p.rstrip("*").rstrip())


def is_broad_shell(entry):
    return entry["tool"].lower() in {"bash", "shell"} and entry["pattern"] in {"", "*"}


# ---------------------------------------------------------------------------
# Links
# ---------------------------------------------------------------------------

def _normalize(token):
    t = token.strip().strip("\"'`(),;")
    t = t.replace("\\", "/")
    t = PATH_PREFIX.sub("", t)
    return t


def _resolve(token, md_rel, files):
    """Resolve a token to a file of the skill. Returns (path, how) or (None, None)."""
    t = _normalize(token)
    if not t or "://" in t or t.startswith("/") and not t.startswith("/skill"):
        return None, None
    base = posixpath.dirname(md_rel)
    for cand, how in ((posixpath.normpath(posixpath.join(base, t)), "relative"), (posixpath.normpath(t), "root")):
        if cand in files:
            return cand, how
    parts = t.split("/")
    if len(parts) >= 2:
        tail = "/".join(parts[-2:])
        matches = [f for f in files if f == tail or f.endswith("/" + tail)]
        if len(matches) == 1:
            return matches[0], "suffix"
    else:
        matches = [f for f in files if posixpath.basename(f) == t]
        if len(matches) == 1:
            return matches[0], "basename"
    return None, None


def find_links(md_rel, text, files):
    """Links from one Markdown file to files of the skill."""
    files = set(files)
    links, seen = [], set()
    lines = text.splitlines()
    fence_lang, in_fence = {}, set()
    for fence in E._markdown_fences(text):
        for i in range(fence["open_index"] + 1, fence["close_index"]):
            in_fence.add(i)
            fence_lang[i] = fence["language"]

    def emit(index, token, relation, via):
        target, how = _resolve(token, md_rel, files)
        if not target or target == md_rel:
            return
        key = (index, target)
        if key in seen:
            return
        seen.add(key)
        links.append({"from_file": md_rel, "from_line": index + 1, "target": target, "relation": relation,
                      "via": via, "resolved_by": how, "evidence": E._brief(" ".join(lines[index].split()), 160)})

    for index, line in enumerate(lines):
        command_texts = []
        if index in in_fence:
            if fence_lang.get(index) in E.SHELL_TAGS | {"", "text", "powershell", "pwsh", "ps1"}:
                command_texts.append((line, "code_fence"))
        else:
            command_texts.extend((m.group(1), "inline_code") for m in re.finditer(r"`([^`\n]+)`", line))
        for text_, via in command_texts:
            try:
                argv = shlex.split(text_.strip().lstrip("$ "), comments=True)
            except ValueError:
                argv = text_.split()
            for j, tok in enumerate(argv):
                if not re.search(r"\.(?:py|sh|bash|zsh|js|mjs|cjs|ts|mts|cts|ps1|rb|pl|php|lua)$", tok):
                    continue
                prev = [E._binary(a) for a in argv[:j]]
                executes = j == 0 or any(p in INTERPRETERS for p in prev[-3:])
                emit(index, tok, "executes" if executes else "references", via)
        if index not in in_fence:
            for m in MD_LINK.finditer(line):
                emit(index, m.group(1), "references", "markdown_link")
            for m in PATH_TOKEN.finditer(re.sub(r"`[^`]*`", " ", line)):
                tok = m.group(1)
                relation = "executes" if tok.endswith(EXEC_SUFFIXES) and RUN_VERB.search(
                    E._sentence_around(line, m.start())) else "references"
                emit(index, tok, relation, "prose")
    return links


# ---------------------------------------------------------------------------
# Declared vs observed
# ---------------------------------------------------------------------------

def declared_tools_section(skill_md_text, findings, links, commands_by_link):
    fm, error, _ = frontmatter(skill_md_text or "")
    section = {"frontmatter_status": "absent" if fm is None and error is None else ("invalid" if error else "parsed"),
               "frontmatter_error": error, "declared": [], "broad_shell": False, "observed_needs": [],
               "uncovered_commands": [], "notes": []}
    if not fm:
        return section, []
    value = fm.get("allowed-tools", fm.get("allowed_tools"))
    entries = parse_allowed_tools(value) if value is not None else []
    section["declared"] = entries
    section["declared_present"] = value is not None
    section["broad_shell"] = any(is_broad_shell(e) for e in entries)
    caps = {f["capability"] for f in findings}
    needs = set()
    if any(l["relation"] == "executes" for l in links) or caps & {"external_agent_launch", "scheduler_invocation",
                                                                   "remote_fetch_execute"}:
        needs.add("Bash")
    if "in_host_delegation" in caps:
        needs.add("Task/Agent")
    if caps & {"network_send", "network_fetch"}:
        needs.add("network (via Bash or WebFetch)")
    section["observed_needs"] = sorted(needs)
    bash_patterns = [e["pattern"] for e in entries if e["tool"].lower() == "bash"]
    if value is not None and bash_patterns and not section["broad_shell"]:
        for link, command in commands_by_link:
            if command and not any(_pattern_covers(p, command) for p in bash_patterns):
                section["uncovered_commands"].append({"command": E._brief(command, 120), "from_line": link["from_line"],
                                                      "target": link["target"]})
        if section["uncovered_commands"]:
            section["notes"].append("Some instructed commands are outside the declared Bash scopes; the host will ask "
                                    "for approval (or the declaration is out of date).")
    if value is not None and "Bash" in needs and not bash_patterns:
        section["notes"].append("Instructions run commands but allowed-tools pre-approves no Bash scope; the host "
                                "will prompt for them.")
    extra = []
    if entries:
        broad = [e["raw"] for e in entries if is_broad_shell(e)]
        extra.append({"file": "SKILL.md", "line": _frontmatter_key_line(skill_md_text, ("allowed-tools", "allowed_tools")),
                      "carrier": "frontmatter", "capability": "tool_preapproval",
                      "details": {"entries": [e["raw"] for e in entries][:20], "broad_entries": broad,
                                  "risk_indicators": ["unscoped_shell"] if broad else [],
                                  "resolved_from": "config_structure", "execution_context": "skill_metadata",
                                  "source": "allowed-tools"}})
    mode = fm.get("permissionMode") or fm.get("permission-mode")
    if mode == "bypassPermissions":
        extra.append({"file": "SKILL.md", "line": _frontmatter_key_line(skill_md_text, ("permissionMode", "permission-mode")),
                      "carrier": "frontmatter", "capability": "auto_approval_setting",
                      "details": {"setting": "permissionMode", "value": mode, "risk_indicators": ["bypass_flags"],
                                  "resolved_from": "config_structure", "execution_context": "skill_metadata"}})
    return section, extra


def _frontmatter_key_line(text, keys):
    for i, line in enumerate((text or "").splitlines()[:200]):
        if any(re.match(rf"^\s*{re.escape(k)}\s*:", line) for k in keys):
            return i + 1
    return 1


def link_commands(text, links):
    """The command line text of each executes-link (for allowed-tools scope comparison)."""
    lines = text.splitlines()
    out = []
    for link in links:
        if link["relation"] != "executes":
            continue
        line = lines[link["from_line"] - 1] if link["from_line"] - 1 < len(lines) else ""
        m = re.search(r"`([^`]+)`", line) if link["via"] == "inline_code" else None
        command = (m.group(1) if m else line).strip().lstrip("$ ").strip()
        out.append((link, command))
    return out


# ---------------------------------------------------------------------------
# Chains
# ---------------------------------------------------------------------------

CHAIN_CONTEXTS = {"direct", "generated", "bundled_config", "instruction", "skill_metadata"}
PERSISTENCE_KINDS = {"os_persistence_write", "agent_hook_command"}


def _components(links):
    """file -> set of files connected to it by executes-links (instruction + all files it runs)."""
    comp = {}
    runs = {}
    for l in links:
        if l["relation"] == "executes":
            runs.setdefault(l["from_file"], set()).add(l["target"])
    for md, targets in runs.items():
        group = {md} | targets
        for f in group:
            comp.setdefault(f, set()).update(group)
    return comp


def build_chains(findings, links, files_with_config_findings):
    """findings: normalized V3.2 findings (with id, capability, file, execution_context, details)."""
    comp = _components(links)
    usable = [f for f in findings if f["execution_context"] in CHAIN_CONTEXTS
              and "installation_doc" not in f.get("context_tags", [])]
    by_cap = {}
    for f in usable:
        by_cap.setdefault(f["capability"], []).append(f)

    def scope(a, b):
        if a["file"] == b["file"]:
            return "same_file"
        if b["file"] in comp.get(a["file"], ()):
            return "linked_files"
        return "same_skill"

    chains, seen = [], set()

    def add(rule, members, sc, extra=None):
        key = (rule, tuple(sorted(m["id"] for m in members)))
        if key in seen:
            return
        seen.add(key)
        sub, severity, explanation, remediation = T.CHAINS[rule]
        confs = [m["confidence"] for m in members]
        conf = min(confs, key=T.CONFIDENCES.index)
        if sc == "same_skill":
            conf = "low"
            severity = T.bump(severity, -1)
        chains.append({"rule": rule, "category": sub.split(".")[0], "subcategory": sub,
                       "subcategory_name": T.SUBCATEGORIES.get(sub, ""), "severity": severity, "confidence": conf,
                       "scope": sc, "members": [m["id"] for m in members],
                       "evidence": [{"finding": m["id"], "file": m["file"], "line": m["line"],
                                     "capability": m["capability"]} for m in members],
                       "explanation": explanation.format(scope=sc.replace("_", " ")), "remediation": remediation,
                       "layer": "risk_indicator", **(extra or {})})

    def pairs(caps_a, caps_b, rule, cond_a=lambda f: True, cond_b=lambda f: True, allow_same_skill=True):
        for ca in caps_a:
            for a in by_cap.get(ca, []):
                if not cond_a(a):
                    continue
                for cb in caps_b:
                    for b in by_cap.get(cb, []):
                        if a is b or not cond_b(b):
                            continue
                        sc = scope(a, b)
                        if sc == "same_skill" and not allow_same_skill:
                            continue
                        add(rule, [a, b], sc)

    creds = ("agent_credential_access", "developer_credential_access", "environment_harvesting")
    pairs(creds, ("network_send",), "credential_access_with_network_send",
          cond_a=lambda f: f["execution_context"] in {"direct", "generated"},
          cond_b=lambda f: f["execution_context"] in {"direct", "generated"})
    is_bypass = lambda f: (f["capability"] == "approval_bypass_instruction" and f["details"].get("mechanism") == "permission_flag") \
        or (f["capability"] == "auto_approval_setting" and "bypass_flags" in f["risk_indicators"]) \
        or (f["capability"] == "tool_preapproval" and "unscoped_shell" in f["risk_indicators"])
    pairs(("external_agent_launch",), ("approval_bypass_instruction", "auto_approval_setting", "tool_preapproval"),
          "bypass_with_external_agent", cond_a=lambda f: not f["details"].get("trust_flags"), cond_b=is_bypass,
          allow_same_skill=False)
    pairs(("agent_env_marker_removal",), ("external_agent_launch",), "nesting_guard_removed_for_agent_launch",
          allow_same_skill=False)
    persist_cond = lambda f: f["capability"] in PERSISTENCE_KINDS or \
        (f["capability"] == "scheduler_invocation" and f["details"].get("operation") != "list") or \
        (f["capability"] == "agent_config_modification" and f["details"].get("target_kind") in {"hooks_or_settings", "mcp_config"})
    pairs(("remote_fetch_execute",), ("scheduler_invocation", "os_persistence_write", "agent_hook_command",
                                      "agent_config_modification"), "fetch_execute_with_persistence",
          cond_b=persist_cond, allow_same_skill=False)
    pairs(("scheduler_invocation",), ("external_agent_launch",), "scheduled_agent_run",
          cond_a=lambda f: f["details"].get("operation") != "list", allow_same_skill=False)
    # Code that copies a bundled config file into an agent config location.
    for f in by_cap.get("agent_config_modification", []):
        if f["execution_context"] not in {"direct", "generated"}:
            continue
        for src in f["details"].get("sources", []):
            norm = _normalize(E._show(src).replace("{skill_dir}/", "").replace("{cwd}/", ""))
            for cfg_file, cfg_findings in files_with_config_findings.items():
                if norm and (cfg_file == norm or cfg_file.endswith("/" + norm) or posixpath.basename(cfg_file) == norm):
                    relevant = [c for c in cfg_findings if c["capability"] not in {"network_send", "network_fetch"}]
                    if relevant:
                        add("script_installs_agent_config", [f] + relevant[:6], "linked_files",
                            {"installed_file": cfg_file})
    # Instructions that run bundled code with security-relevant capabilities.
    by_file = {}
    for f in findings:
        by_file.setdefault(f["file"], []).append(f)
    for link in links:
        if link["relation"] != "executes":
            continue
        targets = [f for f in by_file.get(link["target"], []) if f["execution_context"] in {"direct", "generated"}
                   and not f["supporting"] and T.SEVERITIES.index(f["severity"]) >= T.SEVERITIES.index("medium")]
        if targets:
            add("instruction_runs_sensitive_script", targets[:8], "linked_files",
                {"link": {"from_file": link["from_file"], "from_line": link["from_line"], "target": link["target"],
                          "evidence": link["evidence"]}})
    return chains
