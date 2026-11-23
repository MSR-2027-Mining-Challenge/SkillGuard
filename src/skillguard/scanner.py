"""SkillGuard V3.2 folder scanner: carriers -> raw events -> classified findings -> chains.

Output schema: docs/skillguard_v3.2_schema.md (schema_version "5.0").
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

from . import configs as C
from . import crossfile as X
from . import engine as E
from . import jsts as J
from . import taxonomy as T

VERSION = "3.2.0"
SCHEMA_VERSION = "5.0"
MARKDOWN_SUFFIXES = {".md", ".markdown", ".mdx"}
CODE_SUFFIXES = {".py"} | E.SHELL_SUFFIXES | E.POWERSHELL_SUFFIXES
PLAIN_DATA_SUFFIXES = {".csv", ".tsv", ".txt", ".xml", ".lock", ".log"}
MAX_FILE_BYTES = 2_000_000
CONTEXT_BY_CARRIER = dict(E.CONTEXT_BY_CARRIER, markdown_js_example="documented_example",
                          markdown_config_example="documented_example", config_file="bundled_config",
                          frontmatter="skill_metadata")
DETECTION_METHOD = {
    "executable_script": None, "markdown_python_example": "python_ast", "markdown_shell_example": "shell_tokens",
    "markdown_powershell_example": "powershell_lines", "markdown_instruction": "markdown_heuristic",
    "disguised_text": "markdown_heuristic", "markdown_js_example": "js_tree_sitter", "config_file": "config_structure",
    "markdown_config_example": "config_structure", "frontmatter": "config_structure",
}
SECRET_LIKE = re.compile(r"(?i)((?:api[_-]?key|token|secret|password|authorization)[\"']?\s*[:=]\s*[\"']?)([^\s\"',]{12,})")


def _tool_sha():
    digest = hashlib.sha256()
    for name in ("engine.py", "configs.py", "jsts.py", "crossfile.py", "scanner.py", "taxonomy.py"):
        digest.update((Path(__file__).parent / name).read_bytes())
    return digest.hexdigest()


def _redact_line(text):
    return SECRET_LIKE.sub(lambda m: m.group(1) + m.group(2)[:4] + "...(redacted)", text)


# ---------------------------------------------------------------------------
# Classification
# ---------------------------------------------------------------------------

def _has_hole(details):
    blob = json.dumps({k: v for k, v in details.items() if k in {"targets", "command", "commands", "argv_variants",
                                                                 "destination", "sources", "value"}}, default=str)
    return "\\u0000" in blob or "{" in blob and re.search(r"\{[^}\"]+\}", blob) is not None


def _confidence(raw, ctx):
    d = raw["details"]
    resolved = d.get("resolved_from", "")
    carrier = raw["carrier"]
    if resolved == "config_structure":
        return "high" if ctx in {"bundled_config", "skill_metadata"} else "medium"
    if carrier in {"markdown_instruction", "disguised_text"}:
        return "medium" if d.get("mechanism") == "inline_code" else "low"
    if ctx == "documented_example":
        return "medium"
    if raw["capability"] in {"network_send", "network_fetch"}:
        return "medium"
    if ctx == "generated":
        return "medium"
    if d.get("mechanism") == "js_dynamic_exec_of_download":
        return "low"
    # Code: the security-relevant token (agent binary, config/credential path) was matched as a
    # literal. Confidence drops when several alternative values were merged (runtime-selected
    # commands, branch-merged paths), because which one runs is not decided statically.
    alternatives = max(len(d.get("commands") or []), len(d.get("targets") or []), 1)
    return "medium" if alternatives > 1 else "high"


def _method(raw):
    carrier = raw["carrier"]
    if carrier == "executable_script":
        suffix = Path(raw["file"]).suffix.lower()
        if suffix == ".py":
            return "python_ast"
        if suffix in E.POWERSHELL_SUFFIXES:
            return "powershell_lines"
        if suffix in J.JS_SUFFIXES:
            return "js_tree_sitter"
        return "shell_tokens"
    return DETECTION_METHOD.get(carrier) or "unknown"


def _classify(raw, ctx):
    """(category, subcategory, severity, layer, risk_indicators, explanation_detail)."""
    cap = raw["capability"]
    d = raw["details"]
    category, sub, severity, supporting, _, _ = T.CAPABILITIES[cap]
    risks = list(d.get("risk_indicators", []))
    detail = ""
    layer = "capability"
    if cap == "external_agent_launch":
        cmds = ", ".join(d.get("commands") or [d.get("command", "?")])
        detail = f"Launches agent program(s): {cmds}."
        if d.get("trust_flags"):
            risks.append("bypass_flags")
            severity = "high"
            detail += f" Bypass flags: {', '.join(d['trust_flags'])}."
        if d.get("env_markers_removed"):
            risks.append("env_marker_removal")
            severity = "high"
    elif cap == "agent_config_modification":
        kinds = [E.config_target_kind(t) for t in d.get("targets", [])] or ["agent_dir"]
        best = max(kinds, key=lambda k: T.SEVERITIES.index(T.CONFIG_TARGET_KINDS[k][1]))
        d["target_kind"] = best
        sub, severity = T.CONFIG_TARGET_KINDS[best]
        if d.get("operation") in {"delete", "create_dir"}:
            severity = T.severity_min(severity, "medium")
        risks.append("persistent_target")
        detail = f"{d.get('operation', 'modifies')} -> {', '.join(d.get('targets', [])[:3])} ({best.replace('_', ' ')})."
    elif cap == "scheduler_invocation":
        if d.get("operation") == "list":
            severity = "low"
            detail = f"Queries scheduled tasks ({d.get('command')})."
        else:
            risks.append("persistent_target")
            detail = f"Creates or changes scheduled tasks ({d.get('command')})."
    elif cap == "approval_bypass_instruction":
        if d.get("mechanism") == "permission_flag":
            sub, severity = "T2.2", "high"
            risks.append("bypass_flags")
        else:
            severity = "low"
        if d.get("outward_action"):
            risks.append("outward_action")
            sub = "T2.3"
            severity = T.severity_max(severity, "medium")
        detail = f"Text: \"{d.get('matched', '')}\"."
    elif cap == "auto_approval_setting":
        severity = d.get("severity_hint", severity)
        detail = f"{d.get('setting')} = {d.get('value')}."
    elif cap == "tool_preapproval":
        if d.get("broad_entries"):
            severity = "medium"
            detail = f"Unscoped shell pre-approval: {', '.join(d['broad_entries'])}."
        else:
            severity = "info"
            detail = f"Pre-approved: {', '.join(d.get('entries', [])[:5])}."
    elif cap == "agent_endpoint_override":
        cls = d.get("endpoint_class")
        severity = {"non_official": "high", "local": "low"}.get(cls, "info")
        if re.search(r"(?i)proxy", str(d.get("variable", ""))):
            severity = "low" if cls == "non_official" else "info"  # network proxies are common configuration
        if cls == "non_official":
            risks.append("non_official_endpoint")
        detail = f"{d.get('variable')} -> {d.get('value')} ({cls})."
    elif cap == "mcp_server_definition":
        if "fetch_execute_in_command" in risks:
            severity = "high"
        elif "insecure_transport" in risks or "auto_enable" in risks:
            severity = "medium"
        detail = f"Server '{d.get('server')}' ({d.get('transport')}): {d.get('command') or d.get('url', '')}."
    elif cap == "agent_hook_command":
        if "fetch_execute_in_command" in risks or "credential_target" in risks:
            severity = "high"
        elif "network_in_command" in risks:
            severity = T.severity_max(severity, "medium")
        detail = f"{d.get('hook_kind')}{' ' + d['hook_event'] if d.get('hook_event') else ''}: {d.get('command')}."
    elif cap == "suspicious_agent_instruction":
        layer = "risk_indicator"
        signals = sorted(d.get("signals", {}))
        sub = "T1.2" if {"html_comment_instruction", "hidden_unicode", "disguised_file"} & set(signals) else \
            "T1.4" if "pre_approval_claim" in signals else "T1.3"
        if "concealment" in signals:
            risks.append("concealment")
        detail = f"Signals: {', '.join(signals)}."
    elif cap == "remote_fetch_execute":
        detail = f"{d.get('matched', '')}"
    elif cap in {"agent_credential_access", "developer_credential_access"}:
        risks.append("credential_target")
        detail = f"Targets: {', '.join(d.get('targets', [])[:3])}."
    elif cap == "os_persistence_write":
        risks.append("persistent_target")
        if d.get("content") == "environment_export":
            severity = "low"  # appends an `export VAR=...` line, no command
        detail = f"Targets: {', '.join(d.get('targets', [])[:3])}."
    elif cap == "agent_env_marker_removal":
        detail = f"Removed: {', '.join(d.get('removed', []))}."
    elif cap in {"network_send", "network_fetch"}:
        detail = f"{d.get('tool')} {d.get('destination', '')}".strip()
    elif cap == "unpinned_package_execution":
        risks.append("unpinned")
        detail = f"Package: {d.get('package')}."
    elif cap == "install_time_hook":
        if "fetch_execute_in_command" in risks or "network_in_command" in risks:
            severity = "high"
        detail = f"{d.get('hook')}: {d.get('command')}."
    elif cap == "registry_redirect":
        detail = f"{d.get('setting')} -> {d.get('registry')}."
    elif cap == "embedded_secret":
        detail = f"Key {d.get('key')}: {d.get('value')}."
    elif cap == "environment_harvesting":
        detail = f"{d.get('mechanism')}."
    if ctx == "generated":
        risks.append("generated_code")
    return category, sub, severity, layer, sorted(set(risks)), detail, supporting


PRIORITY = ["none", "low", "medium", "high"]


def _priority(f):
    """Triage order. Not a verdict and not the same as severity or confidence."""
    if f["supporting"] or f["severity"] == "info":
        return "none"
    level = {"critical": 3, "high": 3, "medium": 2, "low": 1}[f["severity"]]
    ctx = f["execution_context"]
    if ctx == "documented_example" or ctx == "bundled_config":
        level -= 1
    if "installation_doc" in f["context_tags"]:
        level = min(level, 1)
    boosters = {"bypass_flags", "fetch_execute_in_command", "env_marker_removal", "concealment", "credential_target"}
    if boosters & set(f["risk_indicators"]) and ctx not in {"documented_example"}:
        level += 1
    if f["confidence"] == "low":
        level = min(level, 2)
    return PRIORITY[max(1, min(3, level))]


def _excerpt(lines_by_file, file, line):
    lines = lines_by_file.get(file) or []
    if 1 <= line <= len(lines):
        return _redact_line(" ".join(lines[line - 1].split()))[:200]
    return ""


def normalize(raw, lines_by_file):
    d = raw["details"]
    ctx = d.get("execution_context") or CONTEXT_BY_CARRIER.get(raw["carrier"], "direct")
    if raw["carrier"].startswith("markdown_") and raw["carrier"] != "markdown_instruction" and ctx == "direct":
        ctx = "documented_example"
    tags = []
    if ctx not in {"direct", "generated", "bundled_config", "skill_metadata"} and \
            E.INSTALL_DOC.match(raw["file"].rsplit("/", 1)[-1]):
        tags.append("installation_doc")
    if d.get("context_tag") == "installation_doc" and "installation_doc" not in tags:
        tags.append("installation_doc")
    category, sub, severity, layer, risks, detail, supporting = _classify(raw, ctx)
    cap = raw["capability"]
    excerpt = d.get("evidence") or _excerpt(lines_by_file, raw["file"], raw["line"])
    excerpt = _redact_line(excerpt)
    f = {
        "capability": cap,
        "layer": layer,
        "category": category,
        "category_name": T.CATEGORIES[category],
        "subcategory": sub,
        "subcategory_name": T.SUBCATEGORIES.get(sub, ""),
        "severity": severity,
        "confidence": _confidence(raw, ctx),
        "detection_method": _method(raw),
        "execution_context": ctx,
        "context_tags": tags,
        "supporting": supporting,
        "risk_indicators": risks,
        "file": raw["file"],
        "line": raw["line"],
        "carrier": raw["carrier"],
        "evidence": {"excerpt": excerpt, "excerpt_sha256": hashlib.sha256(excerpt.encode()).hexdigest()[:16]},
        "explanation": (T.CAPABILITIES[cap][4] + (" " + detail if detail else "")).strip(),
        "remediation": T.CAPABILITIES[cap][5],
        "details": {k: (E._show(v) if isinstance(v, str) else v) for k, v in d.items()
                    if k not in {"evidence", "risk_indicators", "severity_hint"}},
        "validation": {"status": "unvalidated"},
    }
    f["details"] = json.loads(json.dumps(f["details"], default=str).replace("\\u0000", ""))
    key = json.dumps({k: f["details"].get(k) for k in ("operation", "command", "commands", "targets", "setting",
                                                         "server", "variable", "mechanism", "hook_event")}, sort_keys=True)
    f["fingerprint"] = hashlib.sha256(f"{cap}|{f['file']}|{f['line']}|{excerpt}|{key}".encode()).hexdigest()[:16]
    f["review_priority"] = _priority(f)
    return f


# ---------------------------------------------------------------------------
# Behaviors (grouping of findings for counting, as in V3.1)
# ---------------------------------------------------------------------------

def _evidence_level(ctxs):
    for ctx, level in (("direct", "code"), ("generated", "generated_code"), ("bundled_config", "config"),
                       ("skill_metadata", "skill_metadata"), ("documented_example", "documented_example")):
        if ctx in ctxs:
            return level
    return "instruction_only"


def _behavior_key(f):
    d = f["details"]
    cap = f["capability"]
    if cap == "external_agent_launch":
        return ",".join(sorted(set(d.get("commands") or [d.get("command", "")])))
    if cap == "scheduler_invocation":
        return "list" if d.get("operation") == "list" else "modify"
    if cap == "agent_config_modification":
        return d.get("target_kind", "")
    if cap in {"auto_approval_setting", "tool_preapproval"}:
        return str(d.get("setting") or d.get("source") or "")
    if cap == "mcp_server_definition":
        return str(d.get("server"))
    return ""


def group_behaviors(findings):
    groups = {}
    order = []
    for f in findings:
        code_like = f["execution_context"] in {"direct", "generated", "bundled_config", "skill_metadata"}
        key = (f["capability"], _behavior_key(f), "code" if code_like else "text")
        if key not in groups:
            groups[key] = []
            order.append(key)
        groups[key].append(f)
    # Text-only groups attach to the matching code group as documentation.
    behaviors = []
    for key in order:
        cap, bkey, cls = key
        members = groups[key]
        if cls == "text" and (cap, bkey, "code") in groups:
            continue
        docs = groups.get((cap, bkey, "text"), []) if cls == "code" else []
        all_members = members + docs
        sev = T.severity_max(*[m["severity"] for m in all_members])
        prio = max((m["review_priority"] for m in all_members), key=PRIORITY.index)
        behaviors.append({
            "behavior_id": f"B{len(behaviors) + 1}", "capability": cap, "key": bkey,
            "category": members[0]["category"], "subcategory": members[0]["subcategory"],
            "layer": members[0]["layer"], "supporting": members[0]["supporting"],
            "evidence_level": _evidence_level({m["execution_context"] for m in members}),
            "severity": sev, "confidence": max((m["confidence"] for m in all_members), key=T.CONFIDENCES.index),
            "review_priority": prio, "risk_indicators": sorted({r for m in all_members for r in m["risk_indicators"]}),
            "findings": [m["id"] for m in members], "documentation": [m["id"] for m in docs],
            "locations": [f"{m['file']}:{m['line']}" for m in members],
        })
    return behaviors


# ---------------------------------------------------------------------------
# Folder scan
# ---------------------------------------------------------------------------

def _read(path):
    data = path.read_bytes()
    if len(data) > MAX_FILE_BYTES:
        raise OverflowError
    if b"\x00" in data[:8192]:
        raise UnicodeError("binary")
    return data.decode("utf-8-sig")


def scan(folder, instructions=True, validations=None):
    root = Path(folder)
    if not root.is_dir():
        raise ValueError(f"Not a skill folder: {root}")
    raw, coverage = [], []
    lines_by_file, texts = {}, {}
    files = sorted(p for p in root.rglob("*") if p.is_file() and not p.is_symlink())
    rels = [p.relative_to(root).as_posix() for p in files]
    for path, rel in zip(files, rels):
        suffix = path.suffix.lower()
        name = path.name.lower()
        is_config = suffix in C.CONFIG_SUFFIXES or name in C.INI_NAMES or name in {".yarnrc.yml", ".yarnrc.yaml"}
        handled = suffix in CODE_SUFFIXES | MARKDOWN_SUFFIXES | set(J.JS_SUFFIXES) or is_config
        if not handled:
            status = "data_file_not_analyzed" if suffix in PLAIN_DATA_SUFFIXES else "unsupported_format"
            coverage.append({"file": rel, "status": status, "analyzers": []})
            continue
        try:
            source = _read(path)
        except OverflowError:
            coverage.append({"file": rel, "status": "too_large", "analyzers": []})
            continue
        except (UnicodeError, OSError) as exc:
            coverage.append({"file": rel, "status": "unreadable", "reason": type(exc).__name__, "analyzers": []})
            continue
        texts[rel] = source
        lines_by_file[rel] = source.splitlines()
        if is_config:
            found, entry = C.analyze_config_file(rel, source)
            raw.extend(found)
            entry["analyzers"] = [entry.pop("analyzer")] if "analyzer" in entry else []
            coverage.append(entry)
            continue
        if suffix in J.JS_SUFFIXES:
            if not J.AVAILABLE:
                coverage.append({"file": rel, "status": "analyzer_unavailable", "analyzers": []})
                continue
            try:
                found, errors = J.analyze_js(source, J.language_for(suffix), rel)
            except ValueError:
                coverage.append({"file": rel, "status": "too_large", "analyzers": []})
                continue
            raw.extend(found)
            coverage.append({"file": rel, "status": "analyzed_with_parse_errors" if errors else "analyzed",
                             "analyzers": ["js_tree_sitter"]})
            continue
        # Python / shell / PowerShell / Markdown, via the engine (V3.1 carriers + V3.2 additions)
        skipped = Counter()
        analyzed_lines = set()
        analyzers = []
        status = None
        blocks = list(E._code_blocks(path, source, skipped, analyzed_lines))
        is_markdown = suffix in MARKDOWN_SUFFIXES
        for analyzer, block, first_line, carrier in blocks:
            try:
                raw.extend(analyzer(block, first_line, carrier, rel))
                analyzers.append(carrier)
            except SyntaxError as exc:
                if suffix == ".py" and E._looks_like_markdown(source):
                    status = "disguised_text_scanned"
                    if instructions:
                        for line, kind, details in E._instruction_events(source, set(), rel) + \
                                E._suspicious_events(source, disguised=True):
                            raw.append(E._record_finding(rel, line, "disguised_text", kind, details))
                    analyzers.append("markdown_heuristic")
                    continue
                if not is_markdown:
                    status = "parse_error"
                    coverage.append({"file": rel, "status": "parse_error", "line": first_line + (exc.lineno or 1) - 1,
                                     "analyzers": []})
                else:
                    skipped[f"unparsable_{carrier}"] += 1
        if is_markdown:
            if J.AVAILABLE:
                for fence in E._markdown_fences(source):
                    lang = J.JS_FENCE_TAGS.get(fence["language"])
                    if not lang:
                        continue
                    skipped.pop(fence["language"], None)
                    try:
                        found, _ = J.analyze_js(fence["body"], lang, rel, fence["first_line"], "markdown_js_example")
                        raw.extend(found)
                        analyzed_lines.update(range(fence["open_index"], fence["close_index"] + 1))
                        analyzers.append("markdown_js_example")
                    except ValueError:
                        pass
            for found in [C.analyze_markdown_snippets(rel, source)]:
                if found:
                    analyzers.append("markdown_config_example")
                raw.extend(found)
            for fence, kind, _ in C.markdown_config_snippets(source):
                skipped.pop(fence["language"], None)
            if instructions:
                for line, kind, details in E._instruction_events(source, analyzed_lines, rel) + E._suspicious_events(source):
                    raw.append(E._record_finding(rel, line, "markdown_instruction", kind, details))
                analyzers.append("markdown_heuristic")
        if status != "parse_error":
            entry = {"file": rel, "status": status or ("analyzed" if any(a != "markdown_heuristic" for a in analyzers)
                                                          else "markdown_instructions_only" if is_markdown and instructions
                                                          else "markdown_without_supported_code"),
                     "analyzers": sorted(set(analyzers))}
            if skipped:
                entry["skipped_fences"] = dict(sorted(skipped.items()))
            coverage.append(entry)

    # Cross-file: links and declared tools
    links = []
    for rel, text in texts.items():
        if Path(rel).suffix.lower() in MARKDOWN_SUFFIXES:
            links.extend(X.find_links(rel, text, rels))
    skill_md = next((r for r in rels if r.lower() == "skill.md"), None)
    commands = X.link_commands(texts.get(skill_md, ""), [l for l in links if l["from_file"] == skill_md]) if skill_md else []
    declared, extra = X.declared_tools_section(texts.get(skill_md, "") if skill_md else "",
                                               [{"capability": r["capability"]} for r in raw], links, commands)
    raw.extend(extra)

    findings = []
    for r in raw:
        if r["capability"] not in T.CAPABILITIES:
            continue
        findings.append(normalize(r, lines_by_file))
    findings.sort(key=lambda f: (f["file"], f["line"], f["capability"]))
    # merge exact duplicates (same capability/file/line/excerpt) produced by overlapping analyzers
    merged, seen = [], {}
    for f in findings:
        key = f["fingerprint"]
        if key in seen:
            prev = seen[key]
            prev["risk_indicators"] = sorted(set(prev["risk_indicators"]) | set(f["risk_indicators"]))
            for k, v in f["details"].items():
                prev["details"].setdefault(k, v)
            continue
        seen[key] = f
        merged.append(f)
    findings = merged
    for i, f in enumerate(findings, 1):
        f["id"] = f"F{i}"

    # invoked-by annotations
    executes = defaultdict(list)
    for l in links:
        if l["relation"] == "executes":
            executes[l["target"]].append(f"{l['from_file']}:{l['from_line']}")
    for f in findings:
        if f["file"] in executes and f["execution_context"] in {"direct", "generated"}:
            f["invoked_by"] = executes[f["file"]][:5]
            if "invoked_by_instruction" not in f["risk_indicators"]:
                f["risk_indicators"] = sorted(f["risk_indicators"] + ["invoked_by_instruction"])

    config_findings = defaultdict(list)
    for f in findings:
        if f["execution_context"] == "bundled_config":
            config_findings[f["file"]].append(f)
    chains = X.build_chains(findings, links, config_findings)
    if declared.get("broad_shell"):
        for ch in [c for c in chains if c["rule"] == "instruction_runs_sensitive_script"]:
            sub, sev, expl, rem = T.CHAINS["preapproved_shell_runs_sensitive_script"]
            chains.append(dict(ch, rule="preapproved_shell_runs_sensitive_script", subcategory=sub, category="T8",
                               subcategory_name=T.SUBCATEGORIES.get(sub, ""), severity=sev,
                               explanation=expl.format(scope="linked files"), remediation=rem))
    for i, ch in enumerate(chains, 1):
        ch["chain_id"] = f"C{i}"
        level = {"critical": 3, "high": 3, "medium": 2, "low": 1, "info": 0}[ch["severity"]]
        if ch["confidence"] == "low":
            level = min(level, 2)
        ch["review_priority"] = PRIORITY[max(1, level)]
    for f in findings:
        f["in_chains"] = [c["chain_id"] for c in chains if f["id"] in c["members"]]

    _apply_validations(findings, validations)
    behaviors = group_behaviors(findings)
    result = {
        "schema": "skillguard/result",
        "schema_version": SCHEMA_VERSION,
        "tool": {"name": "SkillGuard", "version": VERSION, "sha256": _tool_sha(),
                 "python_parser": f"{sys.version_info.major}.{sys.version_info.minor}",
                 "js_parser": J.PARSER_VERSION},
        "root": str(root),
        "findings": findings,
        "chains": chains,
        "behaviors": behaviors,
        "links": links,
        "declared_tools": declared,
        "coverage": {"files": sorted(coverage, key=lambda c: c["file"]), "summary": _coverage_summary(coverage)},
    }
    result["summary"] = _summary(result)
    return result


ANALYZED = {"analyzed", "analyzed_with_parse_errors", "markdown_instructions_only", "disguised_text_scanned",
            "parsed_no_agent_config"}


def _coverage_summary(coverage):
    statuses = Counter(c["status"] for c in coverage)
    skipped = Counter(Path(c["file"]).suffix.lower() or "(none)" for c in coverage if c["status"] not in ANALYZED)
    return {"files": len(coverage), "analyzed": sum(v for k, v in statuses.items() if k in ANALYZED),
            "not_analyzed": sum(v for k, v in statuses.items() if k not in ANALYZED),
            "by_status": dict(sorted(statuses.items())), "not_analyzed_by_suffix": dict(skipped.most_common())}


def _summary(result):
    primary = [f for f in result["findings"] if not f["supporting"]]
    behaviors = [b for b in result["behaviors"] if not b["supporting"]]
    return {
        "findings": len(result["findings"]), "primary_findings": len(primary),
        "supporting_findings": len(result["findings"]) - len(primary),
        "behaviors": len(behaviors), "chains": len(result["chains"]),
        "by_layer": dict(Counter(f["layer"] for f in primary)),
        "by_category": dict(sorted(Counter(f["category"] for f in primary).items())),
        "by_capability": dict(sorted(Counter(f["capability"] for f in primary).items())),
        "by_review_priority": dict(Counter(f["review_priority"] for f in primary)),
        "behaviors_by_priority": dict(Counter(b["review_priority"] for b in behaviors)),
        "highest_priority": max([f["review_priority"] for f in primary] + [c["review_priority"] for c in result["chains"]]
                                + ["none"], key=PRIORITY.index),
    }


def _apply_validations(findings, validations):
    """Only an external validation record can promote a finding to confirmed_issue."""
    if not validations:
        return
    records = {v["fingerprint"]: v for v in validations if isinstance(v, dict) and v.get("fingerprint")}
    for f in findings:
        rec = records.get(f["fingerprint"])
        if not rec:
            continue
        status = rec.get("status")
        f["validation"] = {"status": status, "reviewer": rec.get("reviewer"), "note": rec.get("note"),
                           "date": rec.get("date")}
        if status == "confirmed" and rec.get("reviewer"):
            f["layer"] = "confirmed_issue"
        elif status == "rejected":
            f["review_priority"] = "none"


# ---------------------------------------------------------------------------
# Text report
# ---------------------------------------------------------------------------

def format_text(result, show_all=False):
    out = []
    s = result["summary"]
    out.append(f"SkillGuard {result['tool']['version']}  {result['root']}")
    out.append(f"{s['primary_findings']} findings ({s['supporting_findings']} supporting), {s['behaviors']} behaviors, "
               f"{s['chains']} chains; highest review priority: {s['highest_priority']}")
    for prio in ("high", "medium", "low") + (("none",) if show_all else ()):
        items = [f for f in result["findings"] if f["review_priority"] == prio and (show_all or not f["supporting"])]
        if not items:
            continue
        out.append(f"\n== review priority: {prio} ==")
        for f in items:
            out.append(f"[{f['id']}] {f['file']}:{f['line']}  {f['subcategory']} {f['capability']}  "
                       f"severity={f['severity']} confidence={f['confidence']} context={f['execution_context']}"
                       + (f" layer={f['layer']}" if f["layer"] != "capability" else ""))
            out.append(f"      why: {f['explanation']}")
            if f["risk_indicators"]:
                out.append(f"      risk indicators: {', '.join(f['risk_indicators'])}")
            if f["evidence"]["excerpt"]:
                out.append(f"      evidence: {f['evidence']['excerpt']}")
            if f["remediation"] and prio in {"high", "medium"}:
                out.append(f"      fix: {f['remediation']}")
    if result["chains"]:
        out.append("\n== combinations ==")
        for c in result["chains"]:
            ev = ", ".join(f"{e['file']}:{e['line']} {e['capability']}" for e in c["evidence"])
            out.append(f"[{c['chain_id']}] {c['rule']}  severity={c['severity']} confidence={c['confidence']} "
                       f"scope={c['scope']} priority={c['review_priority']}")
            out.append(f"      why: {c['explanation']}")
            out.append(f"      evidence: {ev}")
    d = result["declared_tools"]
    if d.get("declared"):
        out.append(f"\nallowed-tools: {', '.join(e['raw'] for e in d['declared'])}"
                   f"{'  (unscoped shell)' if d['broad_shell'] else ''}")
        for note in d.get("notes", []):
            out.append(f"  note: {note}")
    cov = result["coverage"]["summary"]
    out.append(f"\ncoverage: {cov['analyzed']}/{cov['files']} files analyzed; not analyzed: "
               + (", ".join(f"{k}={v}" for k, v in cov["not_analyzed_by_suffix"].items()) or "none"))
    out.append("Findings are capabilities and risk indicators, not confirmed vulnerabilities.")
    return "\n".join(out)
