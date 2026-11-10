"""Read-only prototype for capability extraction from agent skill folders.

V1 reports three observable capabilities: scheduler changes, nested agent
execution, and agent configuration writes. Findings are NOT vulnerability
verdicts. Nothing in a skill is executed or imported.

Usage:
    PYTHONPATH=src python -m skillguard_proto path/to/skill
    PYTHONPATH=src python -m skillguard_proto path/to/skill --json
"""
from __future__ import annotations

import argparse
import ast
import json
import re
import shlex
import textwrap
from pathlib import Path

SUPPORTED = {".py", ".sh", ".bash", ".md"}
AGENTS = {"agent", "claude", "codex", "opencode", "gemini"}
TRUST_FLAGS = {
    "--trust", "--dangerously-skip-permissions", "--yolo",
    "--full-auto", "--skip-permissions",
}
EXEC_CALLS = {
    "subprocess.run", "subprocess.Popen", "subprocess.call",
    "subprocess.check_call", "subprocess.check_output",
    "os.system", "os.popen",
}
WRITE_METHODS = {"write_text", "write_bytes", "touch", "mkdir"}
COPY_CALLS = {"shutil.copy", "shutil.copy2", "shutil.copyfile", "shutil.move"}
CONFIG_PATH = re.compile(
    r"(^|[/\\])(\.claude|\.cursor|\.codex)([/\\]|$)"
    r"|(^|[/\\])(CLAUDE\.md|AGENTS\.md)$",
    re.IGNORECASE,
)
FENCE = re.compile(r"^\s*(\x60{3,}|~{3,})\s*([\w+-]*)")
FILENAME_PROMPT = re.compile(r"^\s*\$\s+")


def _dotted(node: ast.AST) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        prefix = _dotted(node.value)
        return f"{prefix}.{node.attr}" if prefix else node.attr
    return ""


def _resolve(node: ast.AST, variables: dict[str, str]) -> str | list[str] | None:
    """Small, conservative constant/path resolver; never evaluates source."""
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    if isinstance(node, ast.Name):
        return variables.get(node.id)
    if isinstance(node, (ast.List, ast.Tuple)):
        parts = [_resolve(x, variables) for x in node.elts]
        return [x if isinstance(x, str) else "<dynamic>" for x in parts]
    if isinstance(node, ast.JoinedStr):
        return "".join(
            value.value if isinstance(value, ast.Constant) and isinstance(value.value, str)
            else "<dynamic>"
            for value in node.values
        )
    if isinstance(node, ast.BinOp) and isinstance(node.op, (ast.Div, ast.Add)):
        left, right = _resolve(node.left, variables), _resolve(node.right, variables)
        if not isinstance(left, str):
            return None
        if right is None:
            right = "<dynamic>"
        if not isinstance(right, str):
            return None
        return left.rstrip("/") + "/" + right if isinstance(node.op, ast.Div) else left + right
    if isinstance(node, ast.Call):
        name = _dotted(node.func)
        if name in {"Path", "pathlib.Path", "PurePath"} and node.args:
            return _resolve(node.args[0], variables)
        if name in {"Path.home", "pathlib.Path.home"}:
            return "~"
        if name in {"os.path.expanduser", "os.path.abspath", "str"} and node.args:
            return _resolve(node.args[0], variables)
        if name in {"os.path.join", "posixpath.join"}:
            parts = [_resolve(x, variables) for x in node.args]
            if parts and isinstance(parts[0], str):
                return "/".join(x if isinstance(x, str) else "<dynamic>" for x in parts)
        if isinstance(node.func, ast.Attribute) and node.func.attr in {"expanduser", "resolve", "absolute"}:
            return _resolve(node.func.value, variables)
    return None


def _argv(value: str | list[str] | None) -> list[str]:
    if isinstance(value, list):
        return value
    if isinstance(value, str):
        try:
            return shlex.split(value)
        except ValueError:
            return []
    return []


def _command_behavior(args: list[str]) -> tuple[str, str, str] | None:
    """Return (rule_id, stable behavior signature, explanation)."""
    if not args:
        return None
    command = Path(args[0]).name.lower()
    if command == "crontab" and "-" in args[1:]:
        return ("SCHEDULER_WRITE", "scheduler:crontab:write",
                "Command installs or replaces crontab entries.")
    if command in AGENTS and len(args) >= 2:
        flags = sorted(set(arg for arg in args[1:] if arg in TRUST_FLAGS))
        # Capability detection applies even without a trust-bypass flag.
        signature = f"nested-agent:{command}:{','.join(flags) or 'ordinary'}"
        explanation = "Nested agent CLI invoked"
        if flags:
            explanation += f" with trust/permission-related flag(s): {', '.join(flags)}"
        return ("NESTED_AGENT", signature, explanation + ".")
    return None


def _finding(
    rule: str, signature: str, explanation: str, path: str,
    line: int, carrier: str, evidence: str,
) -> dict:
    return {
        "rule_id": rule,
        "behavior_signature": signature,
        "capability": {
            "SCHEDULER_WRITE": "Modify scheduled jobs",
            "NESTED_AGENT": "Launch another AI agent",
            "AGENT_CONFIG_WRITE": "Modify AI agent configuration",
        }[rule],
        "file_path": path,
        "line": line,
        "carrier": carrier,
        "evidence": evidence.strip()[:240],
        "explanation": explanation,
        "risk_assessment": "not_assessed_requires_context",
    }


class PythonExtractor(ast.NodeVisitor):
    def __init__(self, source: str, path: str, carrier: str, offset: int = 0):
        self.lines = source.splitlines()
        self.path = path
        self.carrier = carrier
        self.offset = offset
        self.variables: dict[str, str] = {}
        self.findings: list[dict] = []

    def emit(self, node: ast.AST, rule: str, signature: str, explanation: str) -> None:
        line = getattr(node, "lineno", 1)
        snippet = self.lines[line - 1] if 1 <= line <= len(self.lines) else ""
        self.findings.append(_finding(rule, signature, explanation, self.path,
                                      line + self.offset, self.carrier, snippet))

    def visit_Assign(self, node: ast.Assign) -> None:
        self.visit(node.value)
        value = _resolve(node.value, self.variables)
        for target in node.targets:
            if isinstance(target, ast.Name):
                if isinstance(value, str):
                    self.variables[target.id] = value
                else:
                    self.variables.pop(target.id, None)

    def visit_AnnAssign(self, node: ast.AnnAssign) -> None:
        if node.value:
            self.visit(node.value)
        if isinstance(node.target, ast.Name):
            value = _resolve(node.value, self.variables) if node.value else None
            if isinstance(value, str):
                self.variables[node.target.id] = value
            else:
                self.variables.pop(node.target.id, None)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        before = self.variables.copy()
        for statement in node.body:
            self.visit(statement)
        self.variables = before

    visit_AsyncFunctionDef = visit_FunctionDef

    def visit_Call(self, node: ast.Call) -> None:
        name = _dotted(node.func)
        if name in EXEC_CALLS and node.args:
            behavior = _command_behavior(_argv(_resolve(node.args[0], self.variables)))
            if behavior:
                self.emit(node, *behavior)

        # Only a write operation counts. Merely mentioning or reading a path
        # is not an agent-configuration modification.
        if isinstance(node.func, ast.Attribute) and node.func.attr in WRITE_METHODS:
            target = _resolve(node.func.value, self.variables)
            if isinstance(target, str) and CONFIG_PATH.search(target):
                self.emit(node, "AGENT_CONFIG_WRITE", "config-write:" + target,
                          f"Method {node.func.attr} modifies agent path {target}.")
        if name in {"open", "io.open"} and node.args:
            path = _resolve(node.args[0], self.variables)
            mode = _resolve(node.args[1], self.variables) if len(node.args) > 1 else "r"
            for kw in node.keywords:
                if kw.arg == "mode":
                    mode = _resolve(kw.value, self.variables)
            if (isinstance(path, str) and CONFIG_PATH.search(path)
                    and isinstance(mode, str) and any(c in mode for c in "wax+")):
                self.emit(node, "AGENT_CONFIG_WRITE", "config-write:" + path,
                          f"File opened for writing in agent path {path}.")
        if name in COPY_CALLS and len(node.args) >= 2:
            target = _resolve(node.args[1], self.variables)
            if isinstance(target, str) and CONFIG_PATH.search(target):
                self.emit(node, "AGENT_CONFIG_WRITE", "config-write:" + target,
                          f"Copy/move writes agent path {target}.")
        if name in {"os.mkdir", "os.makedirs"} and node.args:
            target = _resolve(node.args[0], self.variables)
            if isinstance(target, str) and CONFIG_PATH.search(target):
                self.emit(node, "AGENT_CONFIG_WRITE", "config-write:" + target,
                          f"Creates agent configuration directory {target}.")
        self.generic_visit(node)


def _python(source: str, path: str, carrier: str, offset: int) -> tuple[list[dict], str | None]:
    try:
        tree = ast.parse(textwrap.dedent(source), filename=path)
    except SyntaxError as exc:
        return [], f"Python syntax not parsed at line {offset + (exc.lineno or 1)}: {exc.msg}"
    extractor = PythonExtractor(source, path, carrier, offset)
    extractor.visit(tree)
    return extractor.findings, None


def _shell(source: str, path: str, carrier: str, offset: int = 0) -> list[dict]:
    findings: list[dict] = []
    for number, original in enumerate(source.splitlines(), start=1):
        line = FILENAME_PROMPT.sub("", original.strip())
        try:
            args = shlex.split(line, comments=True)
        except ValueError:
            continue
        # Do not interpret a comment, quoted prose, or an empty line as a command.
        if not args or args[0].startswith("#"):
            continue
        behavior = _command_behavior(args)
        if behavior:
            findings.append(_finding(*behavior, path, number + offset, carrier, original))
        # Simple shell writes: target must be explicit, not an arbitrary variable.
        command = Path(args[0]).name
        target = None
        if command == "mkdir":
            targets = [a for a in args[1:] if not a.startswith("-")]
            target = targets[-1] if targets else None
        elif command in {"cp", "mv", "tee"}:
            targets = [a for a in args[1:] if not a.startswith("-")]
            target = targets[-1] if targets else None
        if isinstance(target, str) and CONFIG_PATH.search(target):
            findings.append(_finding("AGENT_CONFIG_WRITE", "config-write:" + target,
                                     f"Shell command {command} modifies agent path {target}.",
                                     path, number + offset, carrier, original))
    return findings


def _markdown(source: str, path: str) -> tuple[list[dict], list[dict]]:
    lines = source.splitlines()
    findings: list[dict] = []
    skipped: list[dict] = []
    active: tuple[str, int, str] | None = None
    block: list[str] = []
    for number, line in enumerate(lines, start=1):
        match = FENCE.match(line)
        if active is None:
            if match:
                active = (match.group(1)[0], len(match.group(1)), match.group(2).lower())
                block = []
        elif match and match.group(1)[0] == active[0] and len(match.group(1)) >= active[1]:
            code = "\n".join(block)
            offset = number - len(block) - 1
            language = active[2]
            if language in {"python", "py", "python3"}:
                found, error = _python(code, path, "markdown_code", offset)
                findings.extend(found)
                if error:
                    skipped.append({"file_path": path, "reason": error})
            elif language in {"bash", "sh", "shell", "zsh"}:
                findings.extend(_shell(code, path, "markdown_code", offset))
            elif language == "":
                skipped.append({"file_path": path, "reason": f"Unlabeled code fence at line {offset}"})
            active = None
            block = []
        elif active is not None:
            block.append(line)
    if active is not None:
        skipped.append({"file_path": path, "reason": "Unclosed code fence"})
    return findings, skipped


def scan_skill(root: str | Path, max_bytes: int = 512_000) -> dict:
    root = Path(root)
    if not root.is_dir():
        raise ValueError(f"Not a skill directory: {root}")
    findings: list[dict] = []
    scanned: list[str] = []
    skipped: list[dict] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in SUPPORTED:
            continue
        rel = path.relative_to(root).as_posix()
        if path.is_symlink():
            skipped.append({"file_path": rel, "reason": "symlink not followed"})
            continue
        if path.stat().st_size > max_bytes:
            skipped.append({"file_path": rel, "reason": f"larger than {max_bytes} bytes"})
            continue
        source = path.read_text(encoding="utf-8", errors="replace")
        scanned.append(rel)
        if path.suffix.lower() == ".py":
            found, error = _python(source, rel, "executable_code", 0)
            findings.extend(found)
            if error:
                skipped.append({"file_path": rel, "reason": error})
        elif path.suffix.lower() in {".sh", ".bash"}:
            findings.extend(_shell(source, rel, "executable_code"))
        else:
            found, errors = _markdown(source, rel)
            findings.extend(found)
            skipped.extend(errors)
    # Multiple detection mechanisms may observe the same action on one line.
    unique = {(x["rule_id"], x["file_path"], x["line"], x["behavior_signature"]): x
              for x in findings}
    output = sorted(unique.values(), key=lambda x: (x["file_path"], x["line"], x["rule_id"]))
    return {
        "tool": "SkillGuard prototype v1",
        "root": str(root),
        "findings": output,
        "summary": {
            "findings": len(output),
            "distinct_signatures": len({x["behavior_signature"] for x in output}),
            "files_scanned": len(scanned),
            "coverage_warnings": len(skipped),
        },
        "coverage": {
            "files_scanned": scanned,
            "warnings": skipped,
            "not_analyzed": "Markdown prose, unsupported fences/languages, and dynamic command/path values",
        },
    }


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skill_dir", help="A local skill folder containing SKILL.md")
    parser.add_argument("--json", action="store_true", help="Machine-readable JSON output")
    args = parser.parse_args(argv)
    result = scan_skill(args.skill_dir)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"{result['summary']['findings']} capability finding(s), "
              f"{result['summary']['files_scanned']} files scanned")
        for item in result["findings"]:
            print(f"{item['file_path']}:{item['line']} [{item['rule_id']}] "
                  f"{item['explanation']}")
        print(f"Coverage warnings: {result['summary']['coverage_warnings']}")
        print("Findings describe behavior, not confirmed risks or vulnerabilities.")


if __name__ == "__main__":
    main()
