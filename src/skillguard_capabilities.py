"""Read-only V1 inventory of agent-specific capabilities in Python skill files.

Usage:
    PYTHONPATH=src python -m skillguard_capabilities /path/to/skill-folder
    PYTHONPATH=src python -m skillguard_capabilities /path/to/skill-folder --json

This prototype parses Python files and Python fenced blocks in Markdown. It never
executes skill content. A capability finding is NOT a vulnerability verdict.
Unsupported formats and parse failures are recorded as coverage limitations.
"""
from __future__ import annotations

import argparse
import ast
import json
import re
from pathlib import Path

AGENTS = {"agent", "claude", "codex", "opencode", "gemini", "cursor"}
SCHEDULERS = {"crontab", "schtasks", "launchctl"}
CONFIG_PATH = re.compile(r"(?:^|[/\\])\.(?:claude|cursor|codex)(?:[/\\]|$)|(?:^|[/\\])AGENTS\.md$", re.I)
FENCE = re.compile(r"^\s*(`{3,}|~{3,})([^\n]*)$")
PYTHON_TAGS = {"python", "py", "python3"}


def _literal(node):
    """Best-effort static string evaluation; unknown values stay unknown."""
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    if isinstance(node, ast.JoinedStr):
        parts = [_literal(x) for x in node.values]
        return "".join(parts) if all(p is not None for p in parts) else None
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        left, right = _literal(node.left), _literal(node.right)
        if left is not None and right is not None:
            return left + right
    if isinstance(node, ast.Call) and _dotted(node.func) in {"Path", "pathlib.Path", "os.path.expanduser"} and node.args:
        return _literal(node.args[0])
    return None


def _dotted(node):
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        parent = _dotted(node.value)
        return parent + "." + node.attr if parent else node.attr
    return ""


def _arguments(node):
    if isinstance(node, (ast.List, ast.Tuple)):
        return [_literal(item) for item in node.elts]
    return None


def _python_blocks(path, source):
    """Yield (python source, original first-line index, carrier), preserving offsets."""
    if path.suffix.lower() == ".py":
        yield source, 1, "executable_script"
        return
    if path.suffix.lower() != ".md":
        return
    lines = source.splitlines(keepends=True)
    opening = None
    language = ""
    for index, line in enumerate(lines):
        match = FENCE.match(line.rstrip("\r\n"))
        if not match:
            continue
        marker, info = match.groups()
        if opening is None:
            opening = (index, marker)
            language = info.strip().split()[0].lower() if info.strip() else ""
        elif marker[0] == opening[1][0] and len(marker) >= len(opening[1]) and not info.strip():
            if language in PYTHON_TAGS:
                yield "".join(lines[opening[0] + 1:index]), opening[0] + 2, "markdown_python_example"
            opening = None


def _analyze_python(source, first_line, carrier, path):
    tree = ast.parse(source)
    findings = []
    # Only syntactically recognizable expressions. Avoid matching strings/comments.
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = _dotted(node.func)
        command = None
        argv = None
        if func in {"subprocess.run", "subprocess.Popen", "subprocess.call",
                    "subprocess.check_call", "subprocess.check_output"} and node.args:
            argv = _arguments(node.args[0])
            command = argv[0] if argv else None
        elif func in {"os.system", "os.popen"} and node.args:
            raw = _literal(node.args[0])
            if raw:
                argv = raw.split()
                command = argv[0]
        if command:
            binary = Path(command).name.lower()
            if binary in SCHEDULERS:
                findings.append((node, "scheduler_invocation", {"command": binary}))
            if binary in AGENTS:
                flags = [arg for arg in (argv or [])[1:] if isinstance(arg, str)]
                trust = [flag for flag in flags if flag in {
                    "--trust", "--dangerously-skip-permissions", "--yolo",
                    "--full-auto", "--permission-mode"}]
                findings.append((node, "nested_agent_invocation",
                                 {"command": binary, "trust_flags": trust}))
        # For V1, match concrete path literals only, not arbitrary variable flow.
        if func.endswith((".write_text", ".write_bytes", ".mkdir", ".touch")) or func == "open":
            target = _literal(node.func.value) if isinstance(node.func, ast.Attribute) else (
                _literal(node.args[0]) if node.args else None)
            if target and CONFIG_PATH.search(target.replace("\\", "/")):
                findings.append((node, "agent_config_modification", {"target": target}))
    out = []
    for node, kind, details in findings:
        line = first_line + node.lineno - 1
        out.append({"file": path, "line": line, "carrier": carrier,
                    "capability": kind, "details": details, "assessment": "needs_context"})
    return out


def scan(folder):
    root = Path(folder)
    if not root.is_dir():
        raise ValueError(f"Not a skill folder: {root}")
    results = {"schema_version": 1, "root": str(root), "findings": [], "coverage": []}
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(root).as_posix()
        if path.suffix.lower() not in {".py", ".md"}:
            results["coverage"].append({"file": rel, "status": "unsupported_format"})
            continue
        try:
            source = path.read_text(encoding="utf-8")
        except (UnicodeError, OSError) as exc:
            results["coverage"].append({"file": rel, "status": "unreadable", "reason": type(exc).__name__})
            continue
        blocks = list(_python_blocks(path, source))
        if not blocks:
            results["coverage"].append({"file": rel, "status": "no_supported_python_blocks"})
        for block, first_line, carrier in blocks:
            try:
                results["findings"].extend(_analyze_python(block, first_line, carrier, rel))
                status = "analyzed"
            except SyntaxError as exc:
                status = "parse_error"
                results["coverage"].append({"file": rel, "status": status,
                    "line": first_line + (exc.lineno or 1) - 1})
                continue
            results["coverage"].append({"file": rel, "status": status,
                                         "first_line": first_line, "carrier": carrier})
    results["findings"].sort(key=lambda f: (f["file"], f["line"], f["capability"]))
    return results


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skill_folder")
    parser.add_argument("--json", action="store_true", help="print structured results")
    args = parser.parse_args(argv)
    result = scan(args.skill_folder)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        for hit in result["findings"]:
            print(f'{hit["file"]}:{hit["line"]} [{hit["carrier"]}] {hit["capability"]}: {hit["details"]}')
        print(f'{len(result["findings"])} capabilities; '
              f'{sum(x["status"] != "analyzed" for x in result["coverage"])} coverage limitations')


if __name__ == "__main__":
    main()
