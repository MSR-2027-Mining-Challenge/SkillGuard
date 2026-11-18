"""Read-only V1 inventory of agent-specific capabilities in skill files.

Usage:
    PYTHONPATH=src python -m skillguard_capabilities /path/to/skill-folder
    PYTHONPATH=src python -m skillguard_capabilities /path/to/skill-folder --json

Carriers analyzed:
  * Python files (``.py``) and Python fenced blocks in Markdown, via ``ast``.
  * Shell files (``.sh``/``.bash``/``.zsh``) and shell fenced blocks in Markdown,
    via ``shlex`` tokenization.

Capability families (agent-specific only):
  * ``nested_agent_invocation``   launching an AI agent CLI (agent, claude, ...)
  * ``scheduler_invocation``      crontab / schtasks / launchctl
  * ``agent_config_modification`` creating, writing, copying into or deleting
                                  paths under .claude/.cursor/... or AGENTS.md
  * ``agent_env_marker_removal``  stripping CLAUDECODE/OPENCODE/... from the
                                  environment, usually to allow nested agents

Python analysis performs scope-local, flow-insensitive constant propagation:
argv lists and paths assigned to variables (in any branch), ``cmd.extend`` /
``cmd.append`` / ``+=``, f-strings, ``Path.home() / ".claude" / name``,
``os.path.join`` and ``joinpath`` are folded into candidate values. Unknown
parts become ``{placeholders}``. The result over-approximates (all branches are
merged), which is intended for an inventory.

This tool never executes skill content. A capability finding is NOT a
vulnerability verdict. Unsupported formats, prose-only Markdown and parse
failures are recorded as coverage limitations.
"""

from __future__ import annotations

import argparse
import ast
import itertools
import json
import re
import shlex
import sys
from collections import Counter, defaultdict
from pathlib import Path

AGENTS = {"agent", "cursor-agent", "claude", "codex", "opencode", "gemini", "cursor", "aider"}
SCHEDULERS = {"crontab", "schtasks", "launchctl"}
TRUST_FLAGS = {
    "--trust",
    "--dangerously-skip-permissions",
    "--dangerously-bypass-approvals-and-sandbox",
    "--yolo",
    "--full-auto",
    "--permission-mode",
    "--force",
    "--allow-all-tools",
}
# Environment variables that agent CLIs use to mark "running inside an agent"
# (or agent credentials). Removing them is how skills defeat nesting guards.
AGENT_ENV = re.compile(
    r"^(?:CLAUDECODE|CLAUDE_CODE_\w+|OPENCODE(?:_\w+)?|CURSOR_\w+|CODEX_\w+"
    r"|GEMINI_CLI\w*|AIDER_\w+)$"
)
CONFIG_PATH = re.compile(
    r"(?:^|[/\\])\.(?:claude|cursor|codex|gemini|opencode|windsurf)(?:[/\\]|$)"
    r"|(?:^|[/\\])(?:AGENTS|CLAUDE|GEMINI)\.md$|(?:^|[/\\])\.cursorrules$",
    re.I,
)
FENCE = re.compile(r"^\s*(`{3,}|~{3,})([^\n]*)$")
PYTHON_TAGS = {"python", "py", "python3"}
SHELL_TAGS = {"bash", "sh", "shell", "zsh", "console", "shell-session"}
SHELL_SUFFIXES = {".sh", ".bash", ".zsh"}
MARKDOWN_SUFFIXES = {".md", ".markdown"}
DATA_SUFFIXES = {".json", ".yaml", ".yml", ".toml", ".csv", ".tsv", ".txt", ".xml", ".lock"}

SUBPROCESS_CALLS = {
    "subprocess.run",
    "subprocess.Popen",
    "subprocess.call",
    "subprocess.check_call",
    "subprocess.check_output",
    "pexpect.spawn",
    "pty.spawn",
}
SHELL_STRING_CALLS = {
    "os.system",
    "os.popen",
    "subprocess.getoutput",
    "subprocess.getstatusoutput",
    "asyncio.create_subprocess_shell",
}
EXECV_CALLS = {"os.execv", "os.execve", "os.execvp", "os.execvpe"}
SPREAD_EXEC_CALLS = {"asyncio.create_subprocess_exec", "os.execl", "os.execlp"}
HOME_CALLS = {"pathlib.Path.home", "Path.home"}
CWD_CALLS = {"pathlib.Path.cwd", "Path.cwd", "os.getcwd"}
PATH_CTORS = {
    "pathlib.Path",
    "Path",
    "pathlib.PurePath",
    "PurePath",
    "pathlib.PosixPath",
    "os.path.join",
    "os.path.expanduser",
    "os.path.abspath",
    "os.path.realpath",
    "os.path.normpath",
    "os.fspath",
    "str",
}
PASS_THROUGH_METHODS = {"expanduser", "resolve", "absolute", "as_posix"}
OPEN_CALLS = {"open", "builtins.open", "io.open", "codecs.open"}
MKDIR_CALLS = {"os.makedirs", "os.mkdir"}
DELETE_CALLS = {"os.remove", "os.unlink", "os.rmdir", "os.removedirs", "shutil.rmtree"}
DEST_CALLS = {
    "shutil.copy",
    "shutil.copy2",
    "shutil.copyfile",
    "shutil.copytree",
    "shutil.move",
    "os.rename",
    "os.replace",
    "os.symlink",
    "os.link",
}
SHELL_FILE_TOOLS = {
    "mkdir": ("create_dir", "all"),
    "touch": ("write", "all"),
    "tee": ("write", "all"),
    "rm": ("delete", "all"),
    "rmdir": ("delete", "all"),
    "cp": ("copy", "last"),
    "mv": ("move", "last"),
    "ln": ("link", "last"),
    "install": ("copy", "last"),
    "rsync": ("copy", "last"),
}
SHELL_WRAPPERS = {"sudo", "nohup", "exec", "command", "time", "nice", "xargs"}

HOLE = "\x00"
MAX_VALUES = 16


def _hole(label):
    label = re.sub(r"[\x00/\\]", "", label)[:40] or "?"
    return f"{HOLE}{label}{HOLE}"


def _exact(value):
    return isinstance(value, str) and HOLE not in value


def _show(value):
    return re.sub(r"\x00([^\x00]*)\x00", r"{\1}", value)


def _brief(token, limit=48):
    token = " ".join(token.split())
    return token if len(token) <= limit else token[: limit - 3] + "..."


def _is_config_path(value):
    return bool(CONFIG_PATH.search(value.replace("\\", "/")))


def _binary(token):
    if not _exact(token) or not token:
        return ""
    name = token.replace("\\", "/").rsplit("/", 1)[-1].lower()
    return name[:-4] if name.endswith(".exe") else name


def _dotted(node):
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        parent = _dotted(node.value)
        return parent + "." + node.attr if parent else ""
    return ""


def _dedupe(items, limit=MAX_VALUES):
    out = []
    for item in items:
        if item not in out:
            out.append(item)
        if len(out) >= limit:
            break
    return out


def _path_join(left, right):
    if right.startswith("/"):
        return right
    if not left:
        return right
    return left.rstrip("/") + "/" + right


# --------------------------------------------------------------------------
# Shell-level classification (shared by shell carriers and Python argv sinks)
# --------------------------------------------------------------------------


def _argv_events(argv, depth=0):
    """Classify one command argv. Returns [(capability, details)]."""
    events = []
    removed = []
    i = 0
    while i < len(argv) and _exact(argv[i]) and re.match(r"^[A-Za-z_]\w*=", argv[i]):
        name, _, value = argv[i].partition("=")
        if value == "":
            removed.append(name)
        i += 1
    while i < len(argv):
        binary = _binary(argv[i])
        if binary == "env":
            i += 1
            while i < len(argv) and _exact(argv[i]):
                token = argv[i]
                if token in {"-u", "--unset"} and i + 1 < len(argv):
                    removed.append(argv[i + 1])
                    i += 2
                    continue
                if token.startswith("--unset="):
                    removed.append(token.split("=", 1)[1])
                elif re.match(r"^[A-Za-z_]\w*=$", token):
                    removed.append(token[:-1])
                elif not (token.startswith("-") or re.match(r"^[A-Za-z_]\w*=", token)):
                    break
                i += 1
            continue
        if binary in SHELL_WRAPPERS:
            i += 1
            while i < len(argv) and _exact(argv[i]) and argv[i].startswith("-"):
                i += 1
            continue
        if binary == "timeout":
            i += 2
            continue
        break
    markers = [name for name in removed if _exact(name) and AGENT_ENV.match(name)]
    if markers:
        events.append(
            (
                "agent_env_marker_removal",
                {"removed": _dedupe(markers), "mechanism": "command_environment"},
            )
        )
    argv = argv[i:]
    if not argv:
        return events
    binary = _binary(argv[0])
    if binary in {"bash", "sh", "zsh"} and "-c" in argv and depth < 3:
        index = argv.index("-c")
        if index + 1 < len(argv):
            inner = argv[index + 1]
            events.extend((k, d) for k, d, _ in _shell_events(inner, depth + 1))
        return events
    if binary == "unset":
        names = [a for a in argv[1:] if _exact(a) and AGENT_ENV.match(a)]
        if names:
            events.append(("agent_env_marker_removal", {"removed": names, "mechanism": "unset"}))
    if binary in SCHEDULERS:
        events.append(("scheduler_invocation", {"command": binary}))
    if binary in AGENTS:
        trust = [
            a for a in argv[1:] if _exact(a) and a.split("=", 1)[0] in TRUST_FLAGS
        ]
        events.append(
            (
                "nested_agent_invocation",
                {
                    "command": binary,
                    "trust_flags": _dedupe(trust),
                    "argv_variants": [" ".join(_brief(_show(a)) for a in argv)],
                },
            )
        )
    if binary in SHELL_FILE_TOOLS:
        operation, which = SHELL_FILE_TOOLS[binary]
        paths = [a for a in argv[1:] if not (_exact(a) and a.startswith("-"))]
        if which == "last":
            paths = paths[-1:]
        targets = [_show(p) for p in paths if _is_config_path(p)]
        if targets:
            events.append(
                ("agent_config_modification", {"operation": operation, "targets": targets})
            )
    return events


def _shell_events(text, depth=0):
    """Tokenize shell text. Returns [(capability, details, zero_based_line_offset)]."""
    logical = []
    buffer, start = "", None
    for index, raw in enumerate(text.splitlines()):
        line = raw.rstrip()
        if start is None:
            start = index
            stripped = line.lstrip()
            if stripped.startswith("$ "):
                line = stripped[2:]
        if line.endswith("\\"):
            buffer += line[:-1] + " "
            continue
        logical.append((start, buffer + line))
        buffer, start = "", None
    if buffer:
        logical.append((start, buffer))

    events = []
    for offset, line in logical:
        try:
            lexer = shlex.shlex(line, posix=True, punctuation_chars=";&|<>()")
            lexer.whitespace_split = True
            tokens = list(lexer)
        except ValueError:
            tokens = line.split()
        segments, redirects = [[]], []
        i = 0
        while i < len(tokens):
            token = tokens[i]
            if token and set(token) <= set(";&|()"):
                segments.append([])
            elif token and set(token) <= set("<>&"):
                if ">" in token and i + 1 < len(tokens):
                    redirects.append(tokens[i + 1])
                i += 1
            else:
                segments[-1].append(token)
            i += 1
        for segment in segments:
            if segment:
                events.extend((k, d, offset) for k, d in _argv_events(segment, depth))
        targets = [r for r in redirects if _is_config_path(r)]
        if targets:
            events.append(
                ("agent_config_modification", {"operation": "write", "targets": targets}, offset)
            )
    return events


def _analyze_shell(source, first_line, carrier, path):
    out = []
    for kind, details, offset in _shell_events(source):
        details.setdefault("resolved_from", "literal")
        out.append(_record_finding(path, first_line + offset, carrier, kind, details))
    return out


# --------------------------------------------------------------------------
# Python analysis
# --------------------------------------------------------------------------


class _Scope:
    def __init__(self, parent=None):
        self.parent = parent
        self.assigns = defaultdict(list)
        self.mutations = defaultdict(list)

    def lookup(self, name):
        scope = self
        while scope is not None:
            if name in scope.assigns:
                return scope, scope.assigns[name]
            scope = scope.parent
        return None, []


def _own_nodes(roots):
    """Nodes belonging to this scope; nested defs are yielded but not entered."""
    stack = list(reversed(roots))
    while stack:
        node = stack.pop()
        yield node
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Lambda)):
            continue
        stack.extend(reversed(list(ast.iter_child_nodes(node))))


class _PythonAnalyzer:
    def __init__(self, tree):
        self.tree = tree
        self.aliases = {}
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.asname:
                        self.aliases[alias.asname] = alias.name
            elif isinstance(node, ast.ImportFrom) and node.module and not node.level:
                for alias in node.names:
                    self.aliases[alias.asname or alias.name] = f"{node.module}.{alias.name}"
        self.findings = []

    # -- name resolution ---------------------------------------------------
    def names(self, func):
        raw = _dotted(func)
        if not raw:
            return set()
        head, _, rest = raw.partition(".")
        canonical = self.aliases.get(head, head) + ("." + rest if rest else "")
        return {raw, canonical}

    def build_scopes(self, roots, parent, out):
        scope = _Scope(parent)
        nodes = list(_own_nodes(roots))
        for node in nodes:
            self.record(node, scope)
        out.append((scope, nodes))
        for node in nodes:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                self.build_scopes(node.body, scope, out)
            elif isinstance(node, ast.Lambda):
                self.build_scopes([node.body], scope, out)

    @staticmethod
    def record(node, scope):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    scope.assigns[target.id].append(node.value)
        elif isinstance(node, ast.AnnAssign) and node.value is not None:
            if isinstance(node.target, ast.Name):
                scope.assigns[node.target.id].append(node.value)
        elif isinstance(node, ast.NamedExpr):
            scope.assigns[node.target.id].append(node.value)
        elif isinstance(node, ast.AugAssign) and isinstance(node.op, ast.Add):
            if isinstance(node.target, ast.Name):
                scope.mutations[node.target.id].append(("extend", node.value, node.lineno))
        elif (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and isinstance(node.func.value, ast.Name)
            and node.args
        ):
            if node.func.attr in {"extend", "append", "pop"}:
                scope.mutations[node.func.value.id].append(
                    (node.func.attr, node.args[0], node.lineno)
                )
        elif isinstance(node, ast.Delete):
            for target in node.targets:
                if isinstance(target, ast.Subscript) and isinstance(target.value, ast.Name):
                    scope.mutations[target.value.id].append(("pop", target.slice, node.lineno))

    # -- value folding -------------------------------------------------------
    def _product(self, parts, joiner):
        out = []
        for combo in itertools.product(*parts):
            value = ""
            for piece in combo:
                value = _path_join(value, piece) if joiner == "/" else value + piece
            out.append(value)
            if len(out) >= MAX_VALUES:
                break
        return _dedupe(out)

    def values(self, node, scope, depth=0):
        """Candidate string values for an expression (with {placeholders})."""
        if depth > 8:
            return [_hole("?")]
        if isinstance(node, ast.Constant):
            if isinstance(node.value, str):
                return [node.value]
            if isinstance(node.value, (int, float)) and not isinstance(node.value, bool):
                return [str(node.value)]
            return [_hole(repr(node.value))]
        if isinstance(node, ast.JoinedStr):
            parts = []
            for value in node.values:
                if isinstance(value, ast.Constant):
                    parts.append([str(value.value)])
                elif isinstance(value, ast.FormattedValue):
                    parts.append(self.values(value.value, scope, depth + 1))
            return self._product(parts, "")
        if isinstance(node, ast.BinOp) and isinstance(node.op, (ast.Add, ast.Div)):
            parts = [
                self.values(node.left, scope, depth + 1),
                self.values(node.right, scope, depth + 1),
            ]
            return self._product(parts, "/" if isinstance(node.op, ast.Div) else "")
        if isinstance(node, ast.IfExp):
            return _dedupe(
                self.values(node.body, scope, depth + 1)
                + self.values(node.orelse, scope, depth + 1)
            )
        if isinstance(node, ast.Name):
            owner, exprs = scope.lookup(node.id)
            if not exprs:
                return [_hole(node.id)]
            out = []
            for expr in exprs:
                out.extend(self.values(expr, owner, depth + 1))
            return _dedupe(out)
        if isinstance(node, ast.Call):
            names = self.names(node.func)
            if names & HOME_CALLS:
                return ["~"]
            if names & CWD_CALLS:
                return [_hole("cwd")]
            if names & PATH_CTORS:
                if not node.args:
                    return [_hole("cwd")]
                parts = [self.values(arg, scope, depth + 1) for arg in node.args]
                return self._product(parts, "/")
            if names & {"shlex.join"} and node.args:
                return [_hole("shlex.join")]
            if isinstance(node.func, ast.Attribute):
                if node.func.attr in PASS_THROUGH_METHODS:
                    return self.values(node.func.value, scope, depth + 1)
                if node.func.attr == "joinpath":
                    parts = [self.values(node.func.value, scope, depth + 1)]
                    parts += [self.values(arg, scope, depth + 1) for arg in node.args]
                    return self._product(parts, "/")
            return [_hole((_dotted(node.func) or "call") + "()")]
        try:
            label = ast.unparse(node)
        except Exception:  # pragma: no cover - defensive
            label = type(node).__name__
        return [_hole(label)]

    def single(self, node, scope):
        vals = self.values(node, scope)
        if len(vals) == 1:
            return vals[0]
        return _hole("|".join(_show(v) for v in vals[:3]))

    def argvs(self, node, scope, depth=0):
        """Candidate argv lists: [(argv, definition_line)]."""
        if depth > 6:
            return [([_hole("?")], getattr(node, "lineno", 0))]
        line = getattr(node, "lineno", 0)
        if isinstance(node, (ast.List, ast.Tuple)):
            argv = []
            for elt in node.elts:
                if isinstance(elt, ast.Starred):
                    found = self.argvs(elt.value, scope, depth + 1)
                    argv.extend(found[0][0] if found else [_hole("*")])
                else:
                    argv.append(self.single(elt, scope))
            return [(argv, line)]
        if isinstance(node, ast.Name):
            owner, exprs = scope.lookup(node.id)
            if not exprs:
                return [([_hole(node.id)], line)]
            # Attach each extend/append/+= to the nearest preceding assignment of
            # the same name (source order), so per-branch flags stay per-branch.
            starts = sorted(getattr(e, "lineno", 0) for e in exprs)
            result = []
            for expr in exprs:
                begin = getattr(expr, "lineno", 0)
                end = min([s for s in starts if s > begin], default=float("inf"))
                extra = []
                for op, mexpr, mline in owner.mutations.get(node.id, []):
                    if not begin < mline < end:
                        continue
                    if op == "append":
                        extra.append(self.single(mexpr, owner))
                    elif op == "extend":
                        found = self.argvs(mexpr, owner, depth + 1)
                        extra.extend(found[0][0] if found else [])
                for argv, defline in self.argvs(expr, owner, depth + 1):
                    result.append((argv + extra, defline))
            return result[:MAX_VALUES]
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
            left = self.argvs(node.left, scope, depth + 1)
            right = self.argvs(node.right, scope, depth + 1)
            if any(_exact(a[0][0]) and " " not in a[0][0] for a in left):
                return [(l + r, ln) for (l, ln), (r, _) in itertools.product(left, right)][
                    :MAX_VALUES
                ]
        if isinstance(node, ast.IfExp):
            return self.argvs(node.body, scope, depth + 1) + self.argvs(
                node.orelse, scope, depth + 1
            )
        if isinstance(node, ast.Call) and self.names(node.func) & {"shlex.split"} and node.args:
            node = node.args[0]
        # Anything string-like is a shell command line.
        out = []
        for value in self.values(node, scope, depth + 1):
            out.append((value, line))
        return [(self._split(value), ln) for value, ln in out]

    @staticmethod
    def _split(value):
        try:
            return shlex.split(value)
        except ValueError:
            return value.split()

    def env_markers(self, node, scope, depth=0):
        """Agent env markers removed by an env= expression (dict comp / pop / del)."""
        if node is None or depth > 6:
            return []
        if isinstance(node, ast.Name):
            owner, exprs = scope.lookup(node.id)
            found = []
            for expr in exprs:
                found.extend(self.env_markers(expr, owner, depth + 1))
            if owner is not None:
                for op, expr, _ in owner.mutations.get(node.id, []):
                    if op == "pop":
                        found.extend(
                            v for v in self.values(expr, owner) if _exact(v) and AGENT_ENV.match(v)
                        )
            return _dedupe(found)
        if isinstance(node, ast.DictComp):
            return [n for n in self._dictcomp_removed(node, scope)[0] if AGENT_ENV.match(n)]
        return []

    def _dictcomp_removed(self, node, scope):
        """Names excluded by `{k: v for k, v in os.environ.items() if k not in (...)}`."""
        if len(node.generators) != 1:
            return [], False
        gen = node.generators[0]
        source = gen.iter
        if isinstance(source, ast.Call) and isinstance(source.func, ast.Attribute):
            if source.func.attr in {"items", "keys"}:
                source = source.func.value
        from_environ = bool(self.names(source) & {"os.environ"})
        if not from_environ:
            return [], False
        removed = []
        for cond in gen.ifs:
            for compare in [n for n in ast.walk(cond) if isinstance(n, ast.Compare)]:
                for op, comparator in zip(compare.ops, compare.comparators):
                    if isinstance(op, ast.NotIn) and isinstance(
                        comparator, (ast.Tuple, ast.List, ast.Set, ast.Name)
                    ):
                        if isinstance(comparator, ast.Name):
                            owner, exprs = scope.lookup(comparator.id)
                            elts = [e for x in exprs if isinstance(x, (ast.Tuple, ast.List, ast.Set)) for e in x.elts]
                            sub_scope = owner
                        else:
                            elts, sub_scope = comparator.elts, scope
                        for elt in elts:
                            removed.extend(v for v in self.values(elt, sub_scope) if _exact(v))
                    elif isinstance(op, ast.NotEq):
                        removed.extend(v for v in self.values(comparator, scope) if _exact(v))
        return _dedupe(removed, 64), True

    # -- sinks ---------------------------------------------------------------
    def run(self):
        scopes = []
        self.build_scopes(self.tree.body, None, scopes)
        for scope, nodes in scopes:
            for node in nodes:
                if isinstance(node, ast.Call):
                    self.exec_sink(node, scope)
                    self.file_sink(node, scope)
                    self.env_call(node, scope)
                elif isinstance(node, ast.DictComp):
                    removed, from_environ = self._dictcomp_removed(node, scope)
                    markers = [n for n in removed if AGENT_ENV.match(n)]
                    if from_environ and markers:
                        self.add(
                            node,
                            "agent_env_marker_removal",
                            {
                                "removed": markers,
                                "mechanism": "filtered_os_environ_copy",
                                "inherits_remaining_environment": True,
                                "resolved_from": "literal",
                            },
                        )
                elif isinstance(node, ast.Delete):
                    for target in node.targets:
                        if isinstance(target, ast.Subscript):
                            self._marker_key(node, target.slice, scope, "del")
                elif isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Subscript) and "" in self.values(
                            node.value, scope
                        ):
                            self._marker_key(node, target.slice, scope, "set_empty")
        return self.findings

    def add(self, node, kind, details):
        self.findings.append((node.lineno, kind, details))

    def _marker_key(self, node, key, scope, mechanism):
        markers = [v for v in self.values(key, scope) if _exact(v) and AGENT_ENV.match(v)]
        if markers:
            self.add(
                node,
                "agent_env_marker_removal",
                {"removed": markers, "mechanism": mechanism, "resolved_from": "literal"},
            )

    def env_call(self, node, scope):
        names = self.names(node.func)
        if names & {"os.unsetenv"} and node.args:
            self._marker_key(node, node.args[0], scope, "unsetenv")
        elif isinstance(node.func, ast.Attribute) and node.func.attr == "pop" and node.args:
            self._marker_key(node, node.args[0], scope, "pop")

    @staticmethod
    def _kw(node, name):
        for keyword in node.keywords:
            if keyword.arg == name:
                return keyword.value
        return None

    def exec_sink(self, node, scope):
        names = self.names(node.func)
        target = None
        if names & SUBPROCESS_CALLS:
            target = node.args[0] if node.args else self._kw(node, "args")
        elif names & SHELL_STRING_CALLS:
            target = node.args[0] if node.args else self._kw(node, "cmd")
        elif names & EXECV_CALLS:
            target = node.args[1] if len(node.args) > 1 else None
        elif names & SPREAD_EXEC_CALLS and node.args:
            target = ast.List(elts=list(node.args), ctx=ast.Load())
            ast.copy_location(target, node)
        if target is None:
            return
        candidates = self.argvs(target, scope)
        env_removed = self.env_markers(self._kw(node, "env"), scope)
        if isinstance(target, (ast.List, ast.Tuple, ast.Constant)):
            resolved = "literal"
        else:
            resolved = "variable:" + (_dotted(target) or type(target).__name__)
        merged = {}
        for argv, defline in candidates:
            for kind, details in _argv_events(argv):
                key = (kind, details.get("command") or details.get("operation") or details.get("mechanism"))
                entry = merged.setdefault(key, {"definition_lines": []})
                _merge_details(entry, details)
                if defline and defline not in entry["definition_lines"]:
                    entry["definition_lines"].append(defline)
        for (kind, _), details in merged.items():
            details["definition_lines"].sort()
            details["resolved_from"] = resolved
            if kind == "nested_agent_invocation" and env_removed:
                details["env_markers_removed"] = env_removed
            self.add(node, kind, details)

    def _writes(self, mode_node, scope):
        if mode_node is None:
            return False
        for value in self.values(mode_node, scope):
            if _exact(value) and value and set(value) <= set("rwxabt+") and set(value) & set("wxa+"):
                return True
        return False

    def file_sink(self, node, scope):
        names = self.names(node.func)
        attr = node.func.attr if isinstance(node.func, ast.Attribute) else None
        receiver = node.func.value if attr else None
        operation, targets = None, []
        if names & OPEN_CALLS:
            mode = node.args[1] if len(node.args) > 1 else self._kw(node, "mode")
            if node.args and self._writes(mode, scope):
                operation, targets = "write", [node.args[0]]
        elif names & MKDIR_CALLS and node.args:
            operation, targets = "create_dir", [node.args[0]]
        elif names & DELETE_CALLS and node.args:
            operation, targets = "delete", [node.args[0]]
        elif names & DEST_CALLS and len(node.args) > 1:
            operation, targets = "copy_or_move", [node.args[1]]
        elif attr in {"write_text", "write_bytes", "touch"}:
            operation, targets = "write", [receiver]
        elif attr == "mkdir":
            operation, targets = "create_dir", [receiver]
        elif attr in {"unlink", "rmdir"}:
            operation, targets = "delete", [receiver]
        elif attr in {"symlink_to", "hardlink_to"}:
            operation, targets = "link", [receiver]
        elif attr == "open" and not (names & {"webbrowser.open", "os.open"}):
            mode = node.args[0] if node.args else self._kw(node, "mode")
            if self._writes(mode, scope):
                operation, targets = "write", [receiver]
        if not operation:
            return
        matched = []
        for target in targets:
            matched.extend(_show(v) for v in self.values(target, scope) if _is_config_path(v))
        if matched:
            first = targets[0]
            if isinstance(first, ast.Constant):
                resolved = "literal"
            elif isinstance(first, ast.Name):
                resolved = "variable:" + first.id
            else:
                resolved = "expression"  # e.g. Path.home() / ".claude" / name
            self.add(
                node,
                "agent_config_modification",
                {"operation": operation, "targets": _dedupe(matched, 8), "resolved_from": resolved},
            )


def _merge_details(entry, details):
    for key, value in details.items():
        if isinstance(value, list):
            current = entry.setdefault(key, [])
            for item in value:
                if item not in current:
                    current.append(item)
        else:
            entry.setdefault(key, value)


def _record_finding(path, line, carrier, kind, details):
    return {
        "file": path,
        "line": line,
        "carrier": carrier,
        "capability": kind,
        "details": details,
        "assessment": "needs_context",
    }


def _analyze_python(source, first_line, carrier, path):
    analyzer = _PythonAnalyzer(ast.parse(source))
    return [
        _record_finding(path, first_line + lineno - 1, carrier, kind, details)
        for lineno, kind, details in analyzer.run()
    ]


# --------------------------------------------------------------------------
# Carriers and folder scan
# --------------------------------------------------------------------------


def _markdown_blocks(source):
    """Yield (language, body, first_body_line, fence_language) for fenced blocks."""
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
            yield language, "".join(lines[opening[0] + 1 : index]), opening[0] + 2
            opening = None


def _code_blocks(path, source, skipped):
    """Yield (analyzer, source, first_line, carrier); count skipped fence languages."""
    suffix = path.suffix.lower()
    if suffix == ".py":
        yield _analyze_python, source, 1, "executable_script"
        return
    if suffix in SHELL_SUFFIXES:
        yield _analyze_shell, source, 1, "executable_script"
        return
    for language, body, first_line in _markdown_blocks(source):
        if language in PYTHON_TAGS:
            yield _analyze_python, body, first_line, "markdown_python_example"
        elif language in SHELL_TAGS:
            yield _analyze_shell, body, first_line, "markdown_shell_example"
        else:
            skipped[language or "untagged"] += 1


def scan(folder):
    root = Path(folder)
    if not root.is_dir():
        raise ValueError(f"Not a skill folder: {root}")
    results = {
        "schema_version": 2,
        "root": str(root),
        "python_parser": f"{sys.version_info.major}.{sys.version_info.minor}",
        "findings": [],
        "coverage": [],
    }
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(root).as_posix()
        suffix = path.suffix.lower()
        if suffix in DATA_SUFFIXES:
            results["coverage"].append({"file": rel, "status": "data_file_not_analyzed"})
            continue
        if suffix not in {".py"} | SHELL_SUFFIXES | MARKDOWN_SUFFIXES:
            results["coverage"].append({"file": rel, "status": "unsupported_format"})
            continue
        try:
            source = path.read_text(encoding="utf-8")
        except (UnicodeError, OSError) as exc:
            results["coverage"].append(
                {"file": rel, "status": "unreadable", "reason": type(exc).__name__}
            )
            continue
        skipped = Counter()
        blocks = list(_code_blocks(path, source, skipped))
        if not blocks:
            entry = {"file": rel, "status": "markdown_without_supported_code"}
            if skipped:
                entry["skipped_fences"] = dict(sorted(skipped.items()))
            results["coverage"].append(entry)
        for analyzer, block, first_line, carrier in blocks:
            try:
                results["findings"].extend(analyzer(block, first_line, carrier, rel))
            except SyntaxError as exc:
                results["coverage"].append(
                    {
                        "file": rel,
                        "status": "parse_error",
                        "line": first_line + (exc.lineno or 1) - 1,
                        "carrier": carrier,
                    }
                )
                continue
            results["coverage"].append(
                {"file": rel, "status": "analyzed", "first_line": first_line, "carrier": carrier}
            )
        if blocks and skipped:
            results["coverage"].append(
                {"file": rel, "status": "analyzed_with_skipped_fences", "skipped_fences": dict(sorted(skipped.items()))}
            )
    results["findings"].sort(key=lambda f: (f["file"], f["line"], f["capability"]))
    return results


def limitations(result):
    """Coverage entries that represent content SkillGuard did not analyze."""
    return [c for c in result["coverage"] if c["status"] not in {"analyzed", "analyzed_with_skipped_fences"}]


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("skill_folder")
    parser.add_argument("--json", action="store_true", help="print structured results")
    args = parser.parse_args(argv)
    result = scan(args.skill_folder)
    if args.json:
        print(json.dumps(result, indent=2))
        return
    for hit in result["findings"]:
        print(f'{hit["file"]}:{hit["line"]} [{hit["carrier"]}] {hit["capability"]}: {hit["details"]}')
    limits = limitations(result)
    for item in limits:
        print(f'  limitation: {item["file"]}: {item["status"]}{" " + str(item["skipped_fences"]) if "skipped_fences" in item else ""}')
    by_status = Counter(item["status"] for item in limits)
    breakdown = ", ".join(f"{k}={v}" for k, v in sorted(by_status.items()))
    print(
        f'{len(result["findings"])} capabilities; {len(limits)} coverage limitations'
        + (f" ({breakdown})" if breakdown else "")
        + f'; python parser {result["python_parser"]}'
    )


if __name__ == "__main__":
    main()
