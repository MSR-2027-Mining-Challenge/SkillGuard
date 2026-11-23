"""SkillGuard V3.2 analysis engine (derived from frozen V3.1, sha256 eebc59e7).

This module started as a byte-for-byte copy of ``src/skillguard_capabilities.py`` (V3.1, which
stays frozen and unchanged). V3.2 changes, all covered by tests in tests/test_skillguard_v32.py:

* agent-specific permission flags (``--force`` only counts for cursor-agent/agent; value flags
  such as ``--permission-mode bypassPermissions`` and ``--sandbox danger-full-access``);
* more agent programs (copilot, qwen) and agent configuration paths (.vscode, .mcp.json,
  claude_desktop_config.json, copilot-instructions.md, .windsurfrules, .clinerules, ...);
* operating-system persistence targets (shell rc files, LaunchAgents, systemd units, Startup);
  systemctl enable / launchctl load / at as scheduler modifications;
* developer credential paths (SSH, cloud, registry tokens) in code;
* supporting network capabilities (send vs fetch) for Python and shell, used for combinations;
* remote fetch-and-execute (pipelines, process substitution, exec of downloaded content);
* model-endpoint overrides (ANTHROPIC_BASE_URL, OPENAI_BASE_URL, ...) and environment harvesting;
* copy sources are recorded so cross-file analysis can follow bundled files into agent config;
* in-host sub-agent delegation is a separate capability from launching external agent programs;
* no-confirmation instructions about outward-facing actions are marked.

The capability names emitted here are the V3.2 names (see taxonomy.CAPABILITIES). Nothing from
a skill is ever imported or executed.
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import itertools
import json
import re
import shlex
import sys
import textwrap
from collections import Counter, defaultdict
from pathlib import Path

AGENTS = {"agent", "cursor-agent", "claude", "codex", "opencode", "gemini", "cursor", "aider", "copilot", "qwen"}
SCHEDULERS = {"crontab", "schtasks", "launchctl", "systemctl", "at"}
# Flags that disable approval / sandboxing. GENERIC flags count for any agent program; the
# per-agent ones only for that binary (e.g. `--force` is a bypass only for cursor-agent).
GENERIC_TRUST_FLAGS = {
    "--dangerously-skip-permissions",
    "--allow-dangerously-skip-permissions",
    "--dangerously-bypass-approvals-and-sandbox",
    "--yolo",
    "--full-auto",
    "--allow-all-tools",
    "--allow-all-paths",
}
AGENT_TRUST_FLAGS = {
    "agent": {"--force", "-f", "--trust"},
    "cursor-agent": {"--force", "-f", "--trust"},
    "cursor": {"--force", "-f", "--trust"},
    "gemini": {"-y"},
    "aider": {"--yes-always", "--yes"},
    "qwen": {"-y"},
}
# Flags whose VALUE decides whether they bypass approval.
VALUE_TRUST_FLAGS = {
    "--permission-mode": {"bypassPermissions"},
    "--sandbox": {"danger-full-access"},
    "-s": {"danger-full-access"},
    "--ask-for-approval": {"never"},
    "-a": {"never"},
    "--approval-mode": {"yolo"},
}
# Backward-compatible union (used by the Markdown inline-code layer).
TRUST_FLAGS = GENERIC_TRUST_FLAGS | {f for flags in AGENT_TRUST_FLAGS.values() for f in flags if f.startswith("--")} \
    | set(VALUE_TRUST_FLAGS)
# Environment variables that agent CLIs use to mark "running inside an agent"
# (or agent credentials). Removing them is how skills defeat nesting guards.
AGENT_ENV = re.compile(
    r"^(?:CLAUDECODE|CLAUDE_CODE_\w+|OPENCODE(?:_\w+)?|CURSOR_\w+|CODEX_\w+"
    r"|GEMINI_CLI\w*|AIDER_\w+)$"
)
# Model API endpoint / proxy variables whose override redirects agent traffic (and API keys).
ENDPOINT_ENV = re.compile(
    r"^(?:ANTHROPIC_(?:BASE_URL|API_URL|BEDROCK_BASE_URL|VERTEX_BASE_URL)|OPENAI_(?:BASE_URL|API_BASE)"
    r"|AZURE_OPENAI_ENDPOINT|GEMINI_(?:BASE_URL|API_BASE)|GOOGLE_GEMINI_BASE_URL|CODEX_BASE_URL"
    r"|(?:HTTPS?|ALL)_PROXY|(?:https?|all)_proxy)$"
)
OFFICIAL_ENDPOINT_HOSTS = re.compile(
    r"^(?:api\.anthropic\.com|api\.openai\.com|generativelanguage\.googleapis\.com|"
    r"[\w-]+\.openai\.azure\.com|bedrock-runtime\.[\w-]+\.amazonaws\.com|[\w-]*aiplatform\.googleapis\.com)$",
    re.I,
)
CONFIG_PATH = re.compile(
    r"(?:^|[/\\])\.(?:claude|cursor|codex|gemini|opencode|windsurf|hermes|clinerules|roo|kiro|continue|amazonq|qwen)(?:[/\\]|$)"
    r"|(?:^|[/\\])\.vscode[/\\](?:settings|tasks|mcp)\.json$"
    r"|(?:^|[/\\])\.mcp\.json$|(?:^|[/\\])claude_desktop_config\.json$|(?:^|[/\\])\.claude\.json$"
    r"|(?:^|[/\\])\.github[/\\]copilot-instructions\.md$|(?:^|[/\\])\.github[/\\](?:instructions|prompts|chatmodes)[/\\]"
    r"|(?:^|[/\\])\.config[/\\](?:opencode|goose|crush|qwen|aider)(?:[/\\]|$)"
    r"|(?:^|[/\\])(?:AGENTS|CLAUDE|GEMINI)(?:\.local)?\.md$|(?:^|[/\\])\.(?:cursorrules|windsurfrules|clinerules)$"
    r"|(?:^|[/\\])\.aider\.conf\.ya?ml$",
    re.I,
)
# Operating-system autostart locations (writing to them persists code across logins).
PERSISTENCE_PATH = re.compile(
    r"(?:^|[/\\])\.(?:bashrc|bash_profile|bash_login|profile|zshrc|zshenv|zprofile|zlogin|cshrc|tcshrc)$"
    r"|(?:^|[/\\])\.config[/\\]fish[/\\]config\.fish$"
    r"|(?:^|[/\\])Library[/\\]Launch(?:Agents|Daemons)[/\\]"
    r"|(?:^|[/\\])\.config[/\\](?:systemd[/\\]user|autostart)[/\\]|^/etc/(?:systemd[/\\]system|cron\.\w+|crontab|profile\.d|rc\.local)"
    r"|(?:^|[/\\])Start Menu[/\\]Programs[/\\]Startup[/\\]|\\CurrentVersion\\Run\b"
    r"|^/var/spool/cron",
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
SHELL_KEYWORDS = {"if", "then", "else", "elif", "do", "while", "until", "!", "{", "}"}
PACKAGE_RUNNERS = {"npx", "bunx", "pnpm", "yarn", "npm", "uvx", "pipx"}
AGENT_PACKAGES = {
    "@anthropic-ai/claude-code": "claude",
    "@openai/codex": "codex",
    "@google/gemini-cli": "gemini",
    "opencode-ai": "opencode",
}
# Files that hold agent login state / API credentials (reading them is credential access).
CRED_PATH = re.compile(
    r"\.claude[/\\]\.credentials\.json|(?:^|[/\\~\s\"'])\.claude\.json\b|\.codex[/\\]auth\.json"
    r"|\.gemini[/\\](?:oauth_creds|google_accounts)\.json|opencode[/\\]auth\.json|Claude Code-credentials"
    r"|\.cursor[/\\](?:auth|session)[\w.-]*\.json",
    re.I,
)
# Developer credentials (code-level only; prose mentions of ~/.ssh are too common to report).
DEV_CRED_PATH = re.compile(
    r"(?:^|[/\\~])\.ssh[/\\](?:id_[\w-]+(?![\w.-]*\.pub)\b|[\w.-]*_key\b(?!\.pub))"
    r"|(?:^|[/\\~])\.aws[/\\](?:credentials|config)\b|(?:^|[/\\~])\.azure[/\\]"
    r"|(?:^|[/\\~])\.config[/\\]gcloud[/\\](?:credentials|application_default_credentials|legacy_credentials)"
    r"|(?:^|[/\\~])\.(?:netrc|git-credentials|pypirc|npmrc)$|(?:^|[/\\~])\.docker[/\\]config\.json"
    r"|(?:^|[/\\~])\.kube[/\\]config\b|(?:^|[/\\~])\.config[/\\]gh[/\\]hosts\.yml"
    r"|(?:^|[/\\~])\.gnupg[/\\]|Library[/\\]Keychains[/\\]",
    re.I,
)

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


def _cred_targets(text):
    """The credential path(s) inside a token, e.g. from python -c "...open('~/.claude/.credentials.json')"."""
    return [m.group(0).strip(" \"'(") for m in re.finditer(r"[~\w./\\$-]*(?:" + CRED_PATH.pattern + r")", text, re.I)]


def _is_credential_path(value):
    return isinstance(value, str) and bool(CRED_PATH.search(value.replace("\\", "/")))


def _is_dev_credential_path(value):
    if not isinstance(value, str):
        return False
    v = _show(value)
    if "\\" in v and not re.match(r"(?i)^(?:[a-z]:\\|%userprofile%|\$env:)", v):
        return False  # regex or escaped text, not a path
    return bool(DEV_CRED_PATH.search(v))


def _is_persistence_path(value):
    return isinstance(value, str) and bool(PERSISTENCE_PATH.search(_show(value)))


def config_target_kind(value):
    """Classify an agent-config path: hooks_or_settings, mcp_config, instructions_or_memory,
    rules, skills_dir or agent_dir (anything else under an agent directory)."""
    t = _show(value).replace("\\", "/").lower()
    if re.search(r"(?:^|/)(?:\.mcp\.json|mcp\.json|claude_desktop_config\.json|mcp_settings\.json|\.claude\.json)$", t):
        return "mcp_config"
    if re.search(r"(?:^|/)settings(?:\.local)?\.json$|/hooks?(?:/|$)|(?:^|/)config\.toml$|(?:^|/)\.vscode/tasks\.json$"
                 r"|(?:^|/)\.aider\.conf\.ya?ml$|(?:^|/)config\.ya?ml$", t):
        return "hooks_or_settings"
    if re.search(r"/skills?(?:/|$)|/commands(?:/|$)|/agents(?:/|$)|/plugins?(?:/|$)", t):
        return "skills_dir"
    if re.search(r"(?:^|/)(?:agents|claude|gemini)(?:\.local)?\.md$|copilot-instructions\.md$|/memory|memory\.md$"
                 r"|/instructions/|/prompts/|/chatmodes/", t):
        return "instructions_or_memory"
    if re.search(r"\.cursorrules$|\.windsurfrules$|\.clinerules|/rules(?:/|$)", t):
        return "rules"
    return "agent_dir"


def endpoint_assessment(value):
    """('official'|'local'|'placeholder'|'non_official', host) for an endpoint/proxy URL value."""
    v = _show(value).strip().strip("\"'")
    if not v or "{" in v or v.startswith("$") or "<" in v or "your" in v.lower() or "example" in v.lower():
        return "placeholder", ""
    m = re.match(r"^(?:[a-z][a-z0-9+.-]*://)?(?:[^@/]*@)?([^/:?#]+)", v, re.I)
    host = m.group(1).lower() if m else ""
    if host in {"localhost", "127.0.0.1", "0.0.0.0", "::1", "host.docker.internal"} or host.endswith(".localhost"):
        return "local", host
    if OFFICIAL_ENDPOINT_HOSTS.match(host):
        return "official", host
    return "non_official", host


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
    wrappers = []
    i = 0
    while i < len(argv) and _exact(argv[i]) and re.match(r"^[A-Za-z_]\w*=", argv[i]):
        name, _, value = argv[i].partition("=")
        if value == "":
            removed.append(name)
        i += 1
    while i < len(argv):
        binary = _binary(argv[i])
        if binary in SHELL_KEYWORDS:
            i += 1
            continue
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
        if binary == "command" and i + 1 < len(argv) and argv[i + 1] in {"-v", "-V"}:
            return events  # `command -v claude` is an existence check, not a launch
        if binary in SHELL_WRAPPERS:
            wrappers.append(binary)
            i += 1
            while i < len(argv) and _exact(argv[i]) and argv[i].startswith("-"):
                i += 1
            continue
        if binary in {"timeout", "stdbuf"}:
            wrappers.append(binary)
            i += 2 if binary == "timeout" else 1
            continue
        if binary in PACKAGE_RUNNERS:
            j = i + 1
            if binary in {"pnpm", "yarn", "npm"} and j < len(argv) and argv[j] in {"dlx", "exec", "x"}:
                j += 1
            while j < len(argv) and _exact(argv[j]) and argv[j].startswith("-"):
                j += 1
            package = re.sub(r"(?<=.)@[^/@]*$", "", argv[j]) if j < len(argv) and _exact(argv[j]) else ""
            mapped = AGENT_PACKAGES.get(package) or (_binary(package) if _binary(package) in AGENTS else None)
            if mapped:
                wrappers.append(f"{binary} {package}")
                argv = list(argv[:j]) + [mapped] + list(argv[j + 1:])
                i = j
                continue
            break
        # Unresolved wrapper expansion directly followed by an agent binary,
        # e.g. "${runner[@]}" claude ...  or  $WRAPPER codex exec ...
        if (not _exact(argv[i]) or argv[i].startswith("$")) and i + 1 < len(argv) and _binary(argv[i + 1]) in AGENTS:
            wrappers.append(_show(argv[i]))
            i += 1
            continue
        break
    markers = [name for name in removed if _exact(name) and AGENT_ENV.match(name)]
    if markers:
        events.append(("agent_env_marker_removal", {"removed": _dedupe(markers), "mechanism": "command_environment"}))
    for token in argv[:i]:
        name, eq, value = token.partition("=") if _exact(token) or "=" in token else ("", "", "")
        if eq and ENDPOINT_ENV.match(name) and value:
            events.append(_endpoint_event(name, value, "command_environment"))
    argv = argv[i:]
    if not argv:
        return events
    creds = _dedupe([t for a in argv if _is_credential_path(a) for t in _cred_targets(_show(a))])
    if creds and _binary(argv[0]) not in {"test", "[", "ls", "chmod", "stat", "touch"}:
        events.append(("agent_credential_access", {"operation": "read_or_copy", "targets": creds,
                                                   "command": _binary(argv[0]) or _show(argv[0])}))
    dev = _dedupe([_show(a) for a in argv[1:] if _is_dev_credential_path(a)])
    binary = _binary(argv[0])
    if dev and binary in CRED_READERS:
        events.append(("developer_credential_access", {"operation": "read_or_copy", "targets": dev,
                                                       "command": binary or _show(argv[0])}))
    if binary in {"bash", "sh", "zsh"} and "-c" in argv and depth < 3:
        index = argv.index("-c")
        if index + 1 < len(argv):
            events.extend((k, d) for k, d, _ in _shell_events(argv[index + 1], depth + 1))
        return events
    if binary == "unset":
        names = [a for a in argv[1:] if _exact(a) and AGENT_ENV.match(a)]
        if names:
            events.append(("agent_env_marker_removal", {"removed": names, "mechanism": "unset"}))
    if binary in {"export", "set", "setenv"}:
        for token in argv[1:]:
            name, eq, value = token.partition("=")
            if eq and ENDPOINT_ENV.match(name) and value:
                events.append(_endpoint_event(name, value, "export"))
    if binary in SCHEDULERS:
        sub = argv[1] if len(argv) > 1 and _exact(argv[1]) else ""
        args = [a for a in argv[1:] if _exact(a) and not a.startswith("-")]
        if binary == "at" and not args:
            pass  # bare `at` is not a scheduling command we can classify
        elif binary == "systemctl":
            # Only enabling/linking a unit installs persistence; start/stop/restart/status manage a
            # running service and are not scheduling.
            verbs = [a for a in args if a in {"enable", "link", "reenable"}]
            if verbs:
                events.append(("scheduler_invocation", {"command": binary, "operation": "modify",
                                                        "subcommand": verbs[0]}))
        else:
            listing = (binary == "crontab" and "-l" in argv and "-" not in argv[1:]) or \
                      (binary == "launchctl" and sub in {"list", "print", "unload", "bootout", "remove"}) or \
                      (binary == "schtasks" and any(a.lower() in {"/query", "/delete"} for a in argv[1:] if _exact(a))) or \
                      (binary == "at" and sub in {"-l", "-d", "-r"})
            events.append(("scheduler_invocation", {"command": binary, "operation": "list" if listing else "modify"}))
    if binary in AGENTS:
        trust = _trust_flags(binary, argv[1:])
        details = {"command": binary, "trust_flags": trust,
                   "argv_variants": [" ".join(_brief(_show(a)) for a in argv)]}
        if wrappers:
            details["wrappers"] = _dedupe(wrappers)
        events.append(("external_agent_launch", details))
    if binary in SHELL_FILE_TOOLS:
        operation, which = SHELL_FILE_TOOLS[binary]
        paths = [a for a in argv[1:] if not (_exact(a) and a.startswith("-"))]
        sources = paths[:-1] if which == "last" else []
        if which == "last":
            paths = paths[-1:]
        targets = [_show(p) for p in paths if _is_config_path(p) and not _is_credential_path(p)]
        if targets:
            details = {"operation": operation, "targets": targets}
            if sources:
                details["sources"] = [_show(s) for s in sources]
            events.append(("agent_config_modification", details))
        persist = [_show(p) for p in paths if _is_persistence_path(p)]
        if persist and operation not in {"delete", "create_dir"}:
            events.append(("os_persistence_write", {"operation": operation, "targets": persist}))
    net = _network_argv(binary, argv)
    if net:
        events.append(net)
    return events


# Commands that read, copy or transmit file content (developer-credential access needs one of these).
CRED_READERS = {"cat", "cp", "scp", "rsync", "base64", "curl", "wget", "tar", "zip", "gpg", "xxd", "od", "head", "tail",
                "less", "more", "openssl", "nc", "ncat", "netcat", "python", "python3", "node", "jq", "awk", "sed", "grep",
                "strings", "install", "mv", "dd", "type", "get-content", "copy-item", "aws"}


def _trust_flags(binary, args):
    """Approval-bypass flags for one agent program (agent-specific and value-dependent)."""
    found = []
    specific = AGENT_TRUST_FLAGS.get(binary, set())
    for index, arg in enumerate(args):
        if not _exact(arg):
            continue
        name, eq, value = arg.partition("=")
        if name in GENERIC_TRUST_FLAGS or name in specific:
            found.append(arg)
        elif name in VALUE_TRUST_FLAGS:
            if not eq and index + 1 < len(args) and _exact(args[index + 1]):
                value = args[index + 1]
            if value in VALUE_TRUST_FLAGS[name]:
                found.append(f"{name} {value}" if not eq else arg)
    return _dedupe(found)


def _endpoint_event(name, value, mechanism):
    kind, host = endpoint_assessment(value)
    return ("agent_endpoint_override", {"variable": name, "value": _brief(_show(value), 80), "endpoint_class": kind,
                                        "host": host, "mechanism": mechanism})


NET_TOOLS = {"curl", "wget", "nc", "ncat", "netcat", "scp", "rsync", "sftp", "ftp", "http", "https", "xh"}


def _network_argv(binary, argv):
    """Supporting capability: network use by a command. Returns one event or None."""
    if binary not in NET_TOOLS:
        return None
    args = [a for a in argv[1:]]
    exact = [a for a in args if _exact(a)]
    url = next((_show(a) for a in args if re.match(r"^\S*https?://", _show(a))), "")
    direction = "fetch"
    if binary == "curl":
        if any(a in {"-d", "-F", "-T", "--data", "--data-binary", "--data-raw", "--data-urlencode", "--form",
                     "--upload-file", "--json"} or a.startswith(("--data", "--form", "--json", "-d", "-F")) for a in exact):
            direction = "send"
        for k, a in enumerate(exact):
            if a in {"-X", "--request"} and k + 1 < len(exact) and exact[k + 1].upper() in {"POST", "PUT", "PATCH"}:
                direction = "send"
    elif binary == "wget":
        if any(a.startswith(("--post-data", "--post-file", "--method=POST", "--body-data")) for a in exact):
            direction = "send"
    elif binary in {"nc", "ncat", "netcat", "scp", "rsync", "sftp", "ftp"}:
        remote = [a for a in exact[0:] if re.match(r"^[\w.-]+@?[\w.-]*:", a) and not a.startswith("-")]
        if binary in {"scp", "rsync"} and not remote:
            return None
        if binary in {"nc", "ncat", "netcat"} and "-l" in exact:
            return None
        direction = "send"
        url = url or (remote[-1] if remote else "")
    elif binary in {"http", "https", "xh"}:
        if any(a.upper() in {"POST", "PUT", "PATCH"} for a in exact[:1]) or any("=" in a for a in exact):
            direction = "send"
    if not url and binary in {"curl", "wget", "http", "https", "xh"}:
        url = next((_show(a) for a in args if not (_exact(a) and a.startswith("-")) and "." in _show(a)), "")
    return ("network_send" if direction == "send" else "network_fetch",
            {"tool": binary, "destination": _brief(url, 100)})


FETCH_EXEC_LINE = re.compile(
    r"(?i)\b(?:curl|wget|fetch)\b\s+[^|;&\n]{1,300}\|\s*(?:sudo\s+(?:-\S+\s+)*)?(?:env\s+\S+=\S*\s+)*"
    r"(?:ba|z|da|k|fi)?sh\b(?!\w)(?!\s+-c\b)"
    r"|\b(?:curl|wget)\b\s+[^|;&\n]{1,300}\|\s*(?:sudo\s+)?(?:python3?|node|perl|ruby|php)\s*(?:-\s*)?(?=$|[;&)|`'\"])"
    r"|\b(?:ba|z)?sh\s+<\(\s*(?:curl|wget)\b|\b(?:ba|z)?sh\s+-c\s+[\"']?\$\(\s*(?:curl|wget)\b"
    r"|\beval\s+[\"']?\$\(\s*(?:curl|wget)\b|\bsource\s+<\(\s*(?:curl|wget)\b"
    r"|\b(?:iex|Invoke-Expression)\b[^\n]{0,80}(?:iwr|irm|DownloadString|Invoke-WebRequest|Invoke-RestMethod|Net\.WebClient)"
    r"|\b(?:iwr|irm|Invoke-WebRequest|Invoke-RestMethod)\b[^|\n]{0,200}\|\s*(?:iex|Invoke-Expression)\b"
    r"|base64\s+(?:-d|--decode)[^\n]{0,40}\|\s*(?:ba)?sh\b"
)
PRINT_PREFIX = re.compile(r"(?i)^\s*(?:echo|printf|print|Write-Host|Write-Output|log|info|warn|say)\b")


def fetch_execute_match(line, code=True):
    """The fetch-and-execute text in a line, or None. In code, lines that only print the command
    (echo/printf of an installation hint) are not executions."""
    m = FETCH_EXEC_LINE.search(line)
    if not m:
        return None
    if code and PRINT_PREFIX.match(line) and _in_quotes(line, m.start()):
        return None
    return m.group(0)


def _in_quotes(line, position):
    single = double = False
    for ch in line[:position]:
        if ch == "'" and not double:
            single = not single
        elif ch == '"' and not single:
            double = not double
    return single or double


SHELL_ASSIGN = re.compile(r"^\s*(?:export\s+|local\s+|readonly\s+)?([A-Za-z_]\w*)=(\S.*)?$")


def _expand(text, env):
    return re.sub(r"\$\{([A-Za-z_]\w*)\}|\$([A-Za-z_]\w*)",
                  lambda m: env.get(m.group(1) or m.group(2), m.group(0)), text)


def _substitutions(line):
    """Split out $(...) and `...` command substitutions: (outer_line, [inner commands])."""
    inner, out, i = [], [], 0
    while i < len(line):
        if line.startswith("$(", i) and not line.startswith("$((", i):
            depth, j = 1, i + 2
            while j < len(line) and depth:
                depth += {"(": 1, ")": -1}.get(line[j], 0)
                j += 1
            inner.append(line[i + 2:j - 1])
            out.append(" __SUBST__ ")
            i = j
            continue
        if line[i] == "`":
            j = line.find("`", i + 1)
            if j > i:
                inner.append(line[i + 1:j])
                out.append(" __SUBST__ ")
                i = j + 1
                continue
        out.append(line[i])
        i += 1
    return "".join(out), inner


def _shell_events(text, depth=0):
    """Tokenize shell text. Returns [(capability, details, zero_based_line_offset)].

    Resolves simple VAR=value assignments ($HOME -> ~), analyzes $(...) and
    backtick substitutions as their own commands, and ignores [[ ... ]] tests,
    case-pattern labels and `command -v` existence checks."""
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

    env = {"HOME": "~", "USERPROFILE": "~"}
    events = []
    for offset, raw_line in logical:
        if raw_line.lstrip().startswith("#"):
            continue
        line = _expand(raw_line, env)
        fx = fetch_execute_match(line)
        if fx:
            events.append(("remote_fetch_execute", {"matched": _brief(fx, 160), "mechanism": "shell_pipeline"}, offset))
        assign = SHELL_ASSIGN.match(line)
        if assign and depth == 0:
            value = (assign.group(2) or "").strip()
            try:
                parts = shlex.split(value) if value else [""]
            except ValueError:
                parts = [value]
            if len(parts) <= 1 and "__SUBST__" not in value and "$(" not in value:
                env[assign.group(1)] = parts[0] if parts else ""
                if ENDPOINT_ENV.match(assign.group(1)) and parts and parts[0]:
                    events.append(_endpoint_event(assign.group(1), parts[0], "shell_assignment") + (offset,))
                continue  # pure assignment: a declaration, not a use
        outer, inner_cmds = _substitutions(line)
        line_events = []
        for inner in inner_cmds:
            line_events.extend((k, d) for k, d, _ in _shell_events(inner, depth + 1))
        try:
            lexer = shlex.shlex(outer, posix=True, punctuation_chars=";&|<>()")
            lexer.whitespace_split = True
            tokens = list(lexer)
        except ValueError:
            tokens = outer.split()
        # Drop [[ ... ]] conditional expressions (regex alternation is not a pipe).
        cleaned, skipping = [], False
        for token in tokens:
            if token == "[[":
                skipping = True
                continue
            if skipping:
                if token == "]]":
                    skipping = False
                continue
            cleaned.append(token)
        segments, redirects, paren = [[]], [], 0
        i = 0
        while i < len(cleaned):
            token = cleaned[i]
            if token and set(token) <= set(";&|()"):
                if "(" in token:
                    paren += token.count("(")
                if ")" in token:
                    if paren == 0:
                        segments = [[]]  # `pattern|pattern)` is a case label, not commands
                    else:
                        paren -= token.count(")")
                segments.append([])
            elif token and set(token) <= set("<>&"):
                if ">" in token and i + 1 < len(cleaned):
                    redirects.append(cleaned[i + 1])
                i += 1
            else:
                segments[-1].append(token)
            i += 1
        for segment in segments:
            if segment and segment != ["__SUBST__"]:
                line_events.extend(_argv_events(segment, depth))
        targets = [r for r in redirects if _is_config_path(r)]
        if targets:
            line_events.append(("agent_config_modification", {"operation": "write", "targets": targets}))
        persist = [r for r in redirects if _is_persistence_path(r)]
        if persist:
            details = {"operation": "write", "targets": persist}
            if re.match(r"""^\s*(?:echo|printf)\s+(?:-\w+\s+)?['"]?export\s+[A-Za-z_]\w*=""", outer):
                details["content"] = "environment_export"
            line_events.append(("os_persistence_write", details))
        existence_test = re.match(r"^\s*(?:if|elif|while|!)?\s*(?:\[\[?\s|test\s)", line) and \
            not re.search(r"\b(?:cat|cp|curl|jq|python3?|base64|scp|tar)\b", line)
        if not existence_test and not any(k == "agent_credential_access" for k, _ in line_events):
            creds = _dedupe(_cred_targets(line))
            if creds:
                line_events.append(("agent_credential_access", {"operation": "reference_in_command",
                                                                "targets": creds}))
        events.extend((k, d, offset) for k, d in line_events)
    return events


def _analyze_shell(source, first_line, carrier, path):
    out = []
    for kind, details, offset in _shell_events(source):
        details.setdefault("resolved_from", "literal")
        out.append(_record_finding(path, first_line + offset, carrier, kind, details))
    return out


# --------------------------------------------------------------------------
# PowerShell (line-based, static)
# --------------------------------------------------------------------------

PS_LITERAL = re.compile(r'"((?:`.|[^"`])*)"|\'([^\']*)\'')
PS_LAUNCH_PREFIX = re.compile(r"^\s*(?:&|\.\s|Start-Process(?:\s+-FilePath)?|Invoke-Expression|iex|cmd(?:\.exe)?\s+/[ck])\s*", re.I)
PS_WRITE = re.compile(r"(?i)\b(?:Set-Content|Add-Content|Out-File|New-Item|Copy-Item|Move-Item|WriteAllText|AppendAllText|WriteAllLines)\b")
PS_STRING_SINK = re.compile(r"(?i)^\s*\$[\w:]+\s*\+?=|Set-Content|Add-Content|Out-File|WriteAll|AppendAll|Start-Process|ArgumentList|Invoke-Expression|\biex\b")


def _ps_unescape(text):
    return (text.replace("`r`n", "\n").replace("`n", "\n").replace("`r", "").replace('`"', '"')
            .replace("`t", " ").replace("``", "`"))


def _analyze_powershell(source, first_line, carrier, path):
    """Static PowerShell analysis: agent launches (direct or inside strings that are
    written to batch files / passed to Start-Process), scheduled tasks, env-marker
    removal, agent-config writes and credential reads. $var values come from simple
    string assignments in the same file (all branches, e.g. if/else literals)."""
    text = re.sub(r"<#.*?#>", lambda m: "\n" * m.group(0).count("\n"), source, flags=re.S)
    variables = {}
    out = []

    def subst(value):
        value = re.sub(r"(?i)\$env:(?:USERPROFILE|HOME)|\$HOME\b|~", "~", value)
        return re.sub(r"\$\{?([A-Za-z_]\w*)\}?",
                      lambda m: " ".join(variables.get(m.group(1).lower(), [m.group(0)])), value)

    for index, raw in enumerate(text.splitlines()):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        lineno = first_line + index
        literals = [a if a is not None and a != "" else b for a, b in PS_LITERAL.findall(line)]
        assign = re.match(r"^\$([A-Za-z_]\w*)\s*(\+?)=\s*(.+)$", line)
        if assign and not assign.group(2):
            values = [v for v in literals if v]
            if values:
                variables[assign.group(1).lower()] = [subst(v) for v in values]
        events = []
        expanded = subst(line)
        fx = fetch_execute_match(line)
        if fx:
            events.append(("remote_fetch_execute", {"matched": _brief(fx, 160), "mechanism": "powershell"}, "direct"))
        for m in re.finditer(r"(?i)\$env:(\w+)\s*=\s*[\"']([^\"']+)[\"']", line):
            if ENDPOINT_ENV.match(m.group(1)):
                events.append(_endpoint_event(m.group(1), m.group(2), "powershell_env") + ("direct",))
        body = PS_LAUNCH_PREFIX.sub("", expanded)
        tokens = [t.strip("\"'") for t in re.findall(r'"[^"]*"|\'[^\']*\'|\S+', body)]
        if tokens and _binary(tokens[0]) in AGENTS:
            events.extend((k, d, "direct") for k, d in _argv_events(tokens))
        if PS_STRING_SINK.search(line):
            for literal in literals:
                for sub in _ps_unescape(subst(literal)).splitlines():
                    sub_tokens = sub.split()
                    if len(sub_tokens) >= 2 and _binary(sub_tokens[0].strip("\"'")) in AGENTS:
                        events.extend((k, d, "generated") for k, d, _ in _shell_events(sub))
        if re.search(r"(?i)\b(?:Register-ScheduledTask|New-ScheduledTaskAction)\b|schtasks(?:\.exe)?\s+/create", line):
            events.append(("scheduler_invocation", {"command": "scheduled_task", "operation": "modify"}, "direct"))
        for m in re.finditer(r"(?i)\$env:(\w+)\s*=\s*(?:\$null|\"\"|'')|Remove-Item\s+(?:-Path\s+)?Env:\\?(\w+)"
                             r"|SetEnvironmentVariable\(\s*[\"'](\w+)[\"']\s*,\s*(?:\$null|\"\"|'')", line):
            name = next(g for g in m.groups() if g)
            if AGENT_ENV.match(name):
                events.append(("agent_env_marker_removal", {"removed": [name], "mechanism": "powershell_env"}, "direct"))
        if PS_WRITE.search(line):
            targets = [t for t in re.findall(r"[~\w:.\\/${}-]+", expanded) if _is_config_path(t) and not _is_credential_path(t)]
            if targets:
                events.append(("agent_config_modification", {"operation": "write", "targets": _dedupe(targets)}, "direct"))
        if CRED_PATH.search(expanded):
            events.append(("agent_credential_access", {"operation": "reference_in_command",
                                                       "targets": _dedupe(m.group(0).strip(" \"'") for m in CRED_PATH.finditer(expanded))}, "direct"))
        for kind, details, context in events:
            details = dict(details, resolved_from="powershell", execution_context=context)
            if context == "generated":
                details["generated_carrier"] = "powershell_string"
            out.append(_record_finding(path, lineno, carrier, kind, details))
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
    def __init__(self, tree, nested=False):
        self.tree = tree
        self.nested = nested  # True when analyzing code generated from a string
        self.parents = {}
        for parent in ast.walk(tree):
            for child in ast.iter_child_nodes(parent):
                self.parents[child] = parent
        self._ctx_cache = {}
        self.docstrings = set()
        for node in ast.walk(tree):
            if isinstance(node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                body = node.body
                if body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant):
                    self.docstrings.add(id(body[0].value))
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

    # -- branch contexts -----------------------------------------------------
    def bctx(self, node):
        """Frozenset of (id(if_stmt), branch) pairs enclosing a node (0=body, 1=orelse)."""
        key = id(node)
        if key in self._ctx_cache:
            return self._ctx_cache[key]
        pairs = []
        child, parent = node, self.parents.get(node)
        while parent is not None:
            if isinstance(parent, ast.If):
                if child in parent.body:
                    pairs.append((id(parent), 0))
                elif child in parent.orelse:
                    pairs.append((id(parent), 1))
            if isinstance(parent, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda, ast.ClassDef)):
                break
            child, parent = parent, self.parents.get(parent)
        result = frozenset(pairs)
        self._ctx_cache[key] = result
        return result

    @staticmethod
    def compatible(a, b):
        return not any((k, 1 - v) in b for k, v in a)

    def reaching(self, exprs, ctx):
        """Assignments whose branch context does not contradict ctx (fallback: all)."""
        pairs = [(e, self.bctx(e)) for e in exprs]
        ok = [(e, ctx | c) for e, c in pairs if self.compatible(ctx, c)]
        return ok or [(e, ctx | c) for e, c in pairs]

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

    def values(self, node, scope, depth=0, ctx=frozenset()):
        """Candidate string values for an expression (with {placeholders}).

        ctx is the branch context of the use site. Values are tracked together
        with the branch context that produced them, so concatenations and path
        joins only combine parts from compatible if/elif/else branches."""
        return _dedupe([v for v, _ in self.vctx(node, scope, depth, ctx)])

    def _product_ctx(self, parts, joiner):
        out = []
        for combo in itertools.product(*parts):
            merged, value, ok = frozenset(), "", True
            for piece, piece_ctx in combo:
                if not self.compatible(merged, piece_ctx):
                    ok = False
                    break
                merged |= piece_ctx
                value = _path_join(value, piece) if joiner == "/" else value + piece
            if ok and (value, merged) not in out:
                out.append((value, merged))
            if len(out) >= MAX_VALUES:
                break
        return out

    def vctx(self, node, scope, depth=0, ctx=frozenset()):
        """[(value, branch_context)] for an expression."""
        if depth > 8:
            return [(_hole("?"), ctx)]
        rec = lambda n: self.vctx(n, scope, depth + 1, ctx)  # noqa: E731
        if isinstance(node, ast.Constant):
            if isinstance(node.value, str):
                return [(node.value, ctx)]
            if isinstance(node.value, (int, float)) and not isinstance(node.value, bool):
                return [(str(node.value), ctx)]
            return [(_hole(repr(node.value)), ctx)]
        if isinstance(node, ast.JoinedStr):
            parts = []
            for value in node.values:
                if isinstance(value, ast.Constant):
                    parts.append([(str(value.value), ctx)])
                elif isinstance(value, ast.FormattedValue):
                    parts.append(rec(value.value))
            return self._product_ctx(parts, "")
        if isinstance(node, ast.BinOp) and isinstance(node.op, (ast.Add, ast.Div)):
            return self._product_ctx([rec(node.left), rec(node.right)],
                                     "/" if isinstance(node.op, ast.Div) else "")
        if isinstance(node, ast.IfExp):
            return rec(node.body) + rec(node.orelse)
        if isinstance(node, ast.Name):
            owner, exprs = scope.lookup(node.id)
            if not exprs:
                return [(_hole(node.id), ctx)]
            out = []
            for expr, sub_ctx in self.reaching(exprs, ctx):
                out.extend(self.vctx(expr, owner, depth + 1, sub_ctx))
            return out[:MAX_VALUES]
        if isinstance(node, ast.Call):
            names = self.names(node.func)
            if names & HOME_CALLS:
                return [("~", ctx)]
            if names & CWD_CALLS:
                return [(_hole("cwd"), ctx)]
            if names & PATH_CTORS:
                if not node.args:
                    return [(_hole("cwd"), ctx)]
                return self._product_ctx([rec(arg) for arg in node.args], "/")
            if names & {"shlex.join"} and node.args:
                return [(_hole("shlex.join"), ctx)]
            if isinstance(node.func, ast.Attribute):
                if node.func.attr in PASS_THROUGH_METHODS:
                    return rec(node.func.value)
                if node.func.attr == "joinpath":
                    return self._product_ctx([rec(node.func.value)] + [rec(a) for a in node.args], "/")
            return [(_hole((_dotted(node.func) or "call") + "()"), ctx)]
        try:
            label = ast.unparse(node)
        except Exception:  # pragma: no cover - defensive
            label = type(node).__name__
        return [(_hole(label), ctx)]

    def single(self, node, scope, ctx=frozenset()):
        vals = self.values(node, scope, 0, ctx)
        if len(vals) == 1:
            return vals[0]
        return _hole("|".join(_show(v) for v in vals[:3]))

    def argvs(self, node, scope, depth=0, ctx=frozenset()):
        """Candidate argv lists: [(argv, definition_line)]."""
        if depth > 6:
            return [([_hole("?")], getattr(node, "lineno", 0))]
        line = getattr(node, "lineno", 0)
        if isinstance(node, (ast.List, ast.Tuple)):
            argv = []
            for elt in node.elts:
                if isinstance(elt, ast.Starred):
                    found = self.argvs(elt.value, scope, depth + 1, ctx)
                    argv.extend(found[0][0] if found else [_hole("*")])
                else:
                    argv.append(self.single(elt, scope, ctx))
            return [(argv, line)]
        if isinstance(node, ast.Name):
            owner, exprs = scope.lookup(node.id)
            if not exprs:
                return [([_hole(node.id)], line)]
            # A mutation (extend/append/+=) applies to an assignment only if it is
            # in a compatible branch and after it, before the next assignment.
            starts = sorted(getattr(e, "lineno", 0) for e in exprs)
            result = []
            for expr, sub_ctx in self.reaching(exprs, ctx):
                begin = getattr(expr, "lineno", 0)
                end = min([s for s in starts if s > begin], default=float("inf"))
                extra = []
                for op, mexpr, mline in owner.mutations.get(node.id, []):
                    if not begin < mline < end or not self.compatible(sub_ctx, self.bctx(mexpr)):
                        continue
                    if op == "append":
                        extra.append(self.single(mexpr, owner, sub_ctx))
                    elif op == "extend":
                        found = self.argvs(mexpr, owner, depth + 1, sub_ctx)
                        extra.extend(found[0][0] if found else [])
                for argv, defline in self.argvs(expr, owner, depth + 1, sub_ctx):
                    result.append((argv + extra, defline))
            return result[:MAX_VALUES]
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
            left = self.argvs(node.left, scope, depth + 1, ctx)
            right = self.argvs(node.right, scope, depth + 1, ctx)
            if any(_exact(a[0][0]) and " " not in a[0][0] for a in left):
                return [(l + r, ln) for (l, ln), (r, _) in itertools.product(left, right)][:MAX_VALUES]
        if isinstance(node, ast.IfExp):
            return self.argvs(node.body, scope, depth + 1, ctx) + self.argvs(node.orelse, scope, depth + 1, ctx)
        if isinstance(node, ast.Call) and self.names(node.func) & {"shlex.split"} and node.args:
            node = node.args[0]
        # Anything string-like is a shell command line.
        return [(self._split(value), line) for value in self.values(node, scope, depth + 1, ctx)]

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
                    self.agent_tool_call(node, scope)
                    self.cred_sink(node, scope)
                    self.net_sink(node, scope)
                    self.fetch_exec_sink(node, scope)
                    self.harvest_sink(node, scope)
                    self.env_set_call(node, scope)
                elif (
                    isinstance(node, ast.Constant)
                    and isinstance(node.value, str)
                    and not self.nested
                    and id(node) not in self.docstrings
                ):
                    self.generated_code(node)
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
                        if isinstance(target, ast.Subscript) and self.names(target.value) & {"os.environ"}:
                            self._endpoint_key(node, target.slice, node.value, scope, "os_environ_assignment")
                if isinstance(node, ast.Dict):
                    for key, value in zip(node.keys, node.values):
                        if key is not None and value is not None:
                            self._endpoint_key(node, key, value, scope, "env_dict_literal")
        return self.findings

    def add(self, node, kind, details, line=None):
        self.findings.append((line or node.lineno, kind, details))

    def generated_code(self, node):
        """Python or shell code embedded in a string literal (e.g. a script template).

        Reported with execution_context="generated": the code is not run by this
        file directly; it is written out / passed on and runs later."""
        text = node.value
        if text.count("\n") < 2 or len(text) < 40:
            return
        if node.end_lineno and node.end_lineno > node.lineno:
            first = max(node.lineno, node.end_lineno - text.count("\n"))
        else:
            first = node.lineno
        events = []
        stripped = text.lstrip()
        if re.match(r"#!\s*/(?:usr/)?bin/(?:env\s+)?(?:ba|z)?sh\b", stripped):
            lead = len(text) - len(stripped)
            base = first + text[:lead].count("\n")
            for kind, details, offset in _shell_events(stripped):
                events.append((base + offset, kind, details, "generated_shell_string"))
        else:
            candidate = text.replace("{{", "{").replace("}}", "}") if "{{" in text else text
            try:
                tree = ast.parse(textwrap.dedent(candidate))
            except (SyntaxError, ValueError):
                return
            if not any(isinstance(n, ast.Call) for n in ast.walk(tree)):
                return
            for lineno, kind, details in _PythonAnalyzer(tree, nested=True).run():
                events.append((first + lineno - 1, kind, details, "generated_python_string"))
        for line, kind, details, carrier in events:
            details = dict(details)
            details["execution_context"] = "generated"
            details["generated_by_string_at"] = node.lineno
            details["generated_carrier"] = carrier
            self.add(node, kind, details, line=line)

    def cred_sink(self, node, scope):
        """Reads/copies of agent credential files (OAuth tokens, auth.json)."""
        names = self.names(node.func)
        attr = node.func.attr if isinstance(node.func, ast.Attribute) else None
        targets = []
        if names & OPEN_CALLS and node.args:
            targets = [node.args[0]]
        elif names & {"shutil.copy", "shutil.copy2", "shutil.copyfile"} and node.args:
            targets = [node.args[0]]
        elif attr in {"read_text", "read_bytes", "open"} and not names & {"webbrowser.open", "os.open"}:
            targets = [node.func.value]
        ctx = self.bctx(node)
        values = [v for t in targets for v in self.values(t, scope, 0, ctx)]
        matched = _dedupe(_show(v) for v in values if _is_credential_path(v))
        resolved = "literal" if targets and isinstance(targets[0], ast.Constant) else "expression"
        if matched:
            self.add(node, "agent_credential_access", {"operation": "read", "targets": matched,
                                                       "resolved_from": resolved})
        mode = (node.args[1] if len(node.args) > 1 else self._kw(node, "mode")) if names & OPEN_CALLS else \
            (node.args[0] if attr == "open" and node.args else None)
        dev = _dedupe(_show(v) for v in values if _is_dev_credential_path(v) and not _is_credential_path(v))
        if dev and not self._writes(mode, scope) and attr not in {"write_text", "write_bytes"}:
            self.add(node, "developer_credential_access", {"operation": "read", "targets": dev,
                                                           "resolved_from": resolved})

    def agent_tool_call(self, node, scope):
        """Host-agent tool calls written as Python (cronjob, terminal, Task)."""
        func = _dotted(node.func)
        short = func.rsplit(".", 1)[-1]
        ctx = self.bctx(node)
        if short == "cronjob":
            action = self._kw(node, "action")
            action_vals = self.values(action, scope, 0, ctx) if action is not None else []
            if self._kw(node, "schedule") is not None or "create" in action_vals:
                script = self._kw(node, "script")
                self.add(node, "scheduler_invocation", {
                    "command": "cronjob", "mechanism": "agent_tool_call",
                    "script": _show(self.single(script, scope, ctx)) if script is not None else "",
                    "resolved_from": "literal"})
        elif short in {"terminal", "run_terminal_cmd", "execute_command"} and (node.args or node.keywords):
            target = node.args[0] if node.args else (self._kw(node, "command") or self._kw(node, "cmd"))
            if target is None:
                return
            for value in self.values(target, scope, 0, ctx):
                for kind, details, _ in _shell_events(value):
                    details["mechanism"] = "agent_tool_call:" + short
                    details["resolved_from"] = "literal" if isinstance(target, ast.Constant) else "expression"
                    self.add(node, kind, details)
        elif short in {"Task", "Agent", "spawn_agent"} and self._kw(node, "subagent_type") is not None:
            sub = self.single(self._kw(node, "subagent_type"), scope, ctx)
            self.add(node, "in_host_delegation", {
                "command": short, "commands": [short], "mechanism": "agent_tool_call",
                "subagent_type": _show(sub), "resolved_from": "literal"})

    # -- V3.2 sinks -----------------------------------------------------------
    NET_SEND = {"requests.post", "requests.put", "requests.patch", "httpx.post", "httpx.put", "httpx.patch",
                "smtplib.SMTP", "smtplib.SMTP_SSL", "ftplib.FTP", "socket.create_connection"}
    NET_FETCH = {"requests.get", "requests.head", "httpx.get", "httpx.head", "urllib.request.urlopen",
                 "urllib.request.urlretrieve", "urlopen", "urlretrieve"}
    NET_METHOD_FIRST = {"requests.request", "httpx.request"}

    def _network_kind(self, node):
        names = self.names(node.func)
        attr = node.func.attr if isinstance(node.func, ast.Attribute) else ""
        sends_body = self._kw(node, "data") is not None or self._kw(node, "json") is not None \
            or self._kw(node, "files") is not None
        if names & self.NET_SEND:
            return "send"
        if names & self.NET_FETCH:
            return "send" if sends_body or (len(node.args) > 1 and names & {"urllib.request.urlopen", "urlopen"}) else "fetch"
        if names & self.NET_METHOD_FIRST or names & {"urllib.request.Request"}:
            method = (node.args[0] if node.args else self._kw(node, "method")) if names & self.NET_METHOD_FIRST \
                else self._kw(node, "method")
            if isinstance(method, ast.Constant) and str(method.value).upper() in {"POST", "PUT", "PATCH"}:
                return "send"
            return "send" if sends_body else "fetch"
        receiver = _dotted(node.func.value).lower() if attr else ""
        if attr in {"post", "put", "patch"} and re.search(r"session|client|http|requests|api", receiver):
            return "send"
        if attr == "get" and re.search(r"session|client|requests|httpx", receiver):
            return "fetch"
        if attr in {"connect", "sendall", "send"} and re.search(r"sock", receiver):
            return "send"
        return None

    def net_sink(self, node, scope):
        kind = self._network_kind(node)
        if not kind:
            return
        index = 1 if self.names(node.func) & self.NET_METHOD_FIRST else 0
        target = node.args[index] if len(node.args) > index else (self._kw(node, "url") or self._kw(node, "host"))
        dest = _show(self.single(target, scope, self.bctx(node))) if target is not None else ""
        details = {"tool": _dotted(node.func) or "call", "destination": _brief(dest, 100), "resolved_from": "expression"}
        for kw in ("data", "json", "files", "content"):
            value = self._kw(node, kw)
            if value is not None and self._mentions_environ(value):
                details["sends_environment"] = True
        self.add(node, "network_send" if kind == "send" else "network_fetch", details)

    def _mentions_environ(self, node):
        return any(isinstance(n, (ast.Attribute, ast.Name)) and self.names(n) & {"os.environ"} for n in ast.walk(node))

    def _is_network_expr(self, node, scope, depth=0):
        if node is None or depth > 3:
            return False
        for sub in ast.walk(node):
            if isinstance(sub, ast.Call) and self._network_kind(sub):
                return True
            if isinstance(sub, ast.Name) and depth < 3:
                _, exprs = scope.lookup(sub.id) if scope else (None, [])
                if any(self._is_network_expr(e, scope, depth + 1) for e in exprs):
                    return True
        return False

    def fetch_exec_sink(self, node, scope):
        names = self.names(node.func)
        if not names & {"exec", "eval", "builtins.exec", "builtins.eval", "compile"} or not node.args:
            return
        if self._is_network_expr(node.args[0], scope):
            self.add(node, "remote_fetch_execute", {"mechanism": "python_exec_of_download",
                                                    "matched": _brief(ast.unparse(node), 160), "resolved_from": "expression"})

    def harvest_sink(self, node, scope):
        names = self.names(node.func)
        if names & {"json.dumps", "json.dump", "str", "repr", "pickle.dumps", "yaml.dump", "yaml.safe_dump",
                    "base64.b64encode"} and node.args:
            arg = node.args[0]
            inner = arg.args[0] if isinstance(arg, ast.Call) and self.names(arg.func) & {"dict"} and arg.args else arg
            if isinstance(inner, ast.Call) and isinstance(inner.func, ast.Attribute) and inner.func.attr in {"copy", "items"}:
                inner = inner.func.value
            if self.names(inner) & {"os.environ"}:
                self.add(node, "environment_harvesting", {"mechanism": "serialize_os_environ",
                                                          "call": _dotted(node.func), "resolved_from": "literal"})

    def env_set_call(self, node, scope):
        names = self.names(node.func)
        attr = node.func.attr if isinstance(node.func, ast.Attribute) else ""
        if (names & {"os.putenv"} or (attr == "setdefault" and self.names(node.func.value) & {"os.environ"})) \
                and len(node.args) > 1:
            self._endpoint_key(node, node.args[0], node.args[1], scope, "os_environ_set")

    def _endpoint_key(self, node, key, value, scope, mechanism):
        names = [v for v in self.values(key, scope) if _exact(v) and ENDPOINT_ENV.match(v)]
        if not names:
            return
        val = self.single(value, scope)
        event = _endpoint_event(names[0], val, mechanism)
        self.add(node, event[0], dict(event[1], resolved_from="literal" if _exact(val) else "expression"))

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
        candidates = self.argvs(target, scope, 0, self.bctx(node))
        env_removed = self.env_markers(self._kw(node, "env"), scope)
        if isinstance(target, (ast.List, ast.Tuple, ast.Constant)):
            resolved = "literal"
        else:
            resolved = "variable:" + (_dotted(target) or type(target).__name__)
        merged = {}
        for argv, defline in candidates:
            for kind, details in _argv_events(argv):
                # One finding per sink and capability: alternative commands that the
                # same call may run (runtime-selected CLIs) are one finding.
                key = (kind, details.get("operation") or details.get("mechanism") or "")
                if "command" in details:
                    details = dict(details, commands=[details["command"]])
                entry = merged.setdefault(key, {"definition_lines": []})
                _merge_details(entry, details)
                if kind == "external_agent_launch":
                    per = entry.setdefault("trust_by_command", {}).setdefault(details["command"], [])
                    per.extend(f for f in details.get("trust_flags", []) if f not in per)
                if defline and defline not in entry["definition_lines"]:
                    entry["definition_lines"].append(defline)
        for (kind, _), details in merged.items():
            details["definition_lines"].sort()
            details["resolved_from"] = resolved
            if kind == "external_agent_launch" and env_removed:
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
        operation, targets, sources = None, [], []
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
            sources = [node.args[0]]
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
        matched, persist = [], []
        ctx = self.bctx(node)
        for target in targets:
            for v in self.values(target, scope, 0, ctx):
                if _is_config_path(v) and not _is_credential_path(v):
                    matched.append(_show(v))
                elif _is_persistence_path(v) and operation not in {"delete", "create_dir"}:
                    persist.append(_show(v))
        if persist:
            self.add(node, "os_persistence_write", {"operation": operation, "targets": _dedupe(persist, 8),
                                                    "resolved_from": "expression"})
        if matched:
            first = targets[0]
            if isinstance(first, ast.Constant):
                resolved = "literal"
            elif isinstance(first, ast.Name):
                resolved = "variable:" + first.id
            else:
                resolved = "expression"  # e.g. Path.home() / ".claude" / name
            details = {"operation": operation, "targets": _dedupe(matched, 8), "resolved_from": resolved}
            if sources:
                details["sources"] = _dedupe(_show(v) for v in self.values(sources[0], scope, 0, ctx))
            self.add(node, "agent_config_modification", details)


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


def _markdown_fences(source):
    """Yield closed fences as dicts: language, body (indent removed), first_line,
    open_index, close_index (0-based line indexes of the fence markers)."""
    lines = source.splitlines(keepends=True)
    opening = None
    for index, line in enumerate(lines):
        match = FENCE.match(line.rstrip("\r\n"))
        if not match:
            continue
        marker, info = match.groups()
        if opening is None:
            indent = len(line) - len(line.lstrip(" \t"))
            language = info.strip().split()[0].lower() if info.strip() else ""
            opening = (index, marker, indent, language)
        elif marker[0] == opening[1][0] and len(marker) >= len(opening[1]) and not info.strip():
            start, _, indent, language = opening
            body_lines = []
            for raw in lines[start + 1 : index]:
                # Fences nested in list items are indented; strip the fence indent
                # (CommonMark) and then any remaining common indentation.
                cut = 0
                while cut < indent and cut < len(raw) and raw[cut] in " \t":
                    cut += 1
                body_lines.append(raw[cut:])
            body = textwrap.dedent("".join(body_lines))
            yield {"language": language, "body": body, "first_line": start + 2,
                   "open_index": start, "close_index": index}
            opening = None


def _markdown_blocks(source):
    """Backward-compatible view: (language, body, first_body_line)."""
    for fence in _markdown_fences(source):
        yield fence["language"], fence["body"], fence["first_line"]


# --------------------------------------------------------------------------
# Markdown instruction layer (heuristic, prose + non-code fences + inline code)
# --------------------------------------------------------------------------

WRITE_VERB = re.compile(
    r"(?i)\b(?:add|adds|added|append|appends|put|place|write|writes|create|creates|copy|copies|save|saves"
    r"|install|update|updates|edit|edits|modify|modifies|insert|drop"
    r"|placed|written|copied|saved|installed|created|updated|appended|inserted)\b"
    r"|(?:добав|полож|запиш|созда|скопир|обнов|помест)\w*")
SPAWN = re.compile(
    r"(?i)\b(?:spawn|launch|start|fork|dispatch|delegate|kick off)\w*\b[^.\n]{0,60}?"
    r"\b(?:sub-?agents?|agent[- ]teams?|teammates?|parallel agents?|child agents?|worker agents?|team-leader-agent)\b"
    r"|\bsubagent_type\b|\bAgent Teams\b")
CRON_TOOL = re.compile(r"\bcronjob\s*\(")
CRON_PROSE = re.compile(
    r"(?i)\b(?:schedule|create|set up|add|register)\w*\b[^.\n]{0,40}?"
    r"\b(?:cron ?jobs?|crontab entr\w+|recurring (?:agent )?(?:jobs?|tasks?))\b")
BYPASS_FLAG = re.compile(
    r"--dangerously-skip-permissions|--dangerously-bypass-approvals-and-sandbox|--yolo\b|--full-auto\b"
    r"|\bbypassPermissions\b|--allow-all-tools\b|--permission-mode[ =]\S+")
BYPASS_PHRASE = re.compile(
    r"(?i)\b(?:do not|don't|never|without)\s+(?:ask|asking|prompt|prompting|wait|waiting|confirm|confirming"
    r"|request|requesting)\b[^.\n]{0,40}?\b(?:permission|confirmation|approval|consent|users?|owner)\b"
    r"|\bno need to (?:ask|confirm|check with)\b"
    r"|\bskip(?:ping)?\s+(?:the\s+|all\s+)?(?:permission|confirmation|approval)s?\b"
    r"|\bwithout asking\b(?=\s*[.,;:)]|\s*$)")
OPTION_REFERENCE = re.compile(
    r"^\s*\|.*\|\s*$|\b(?:requires?|required (?:when|for|if)|is required|defaults? to)\b", re.I)
CONDITIONAL_AFTER = re.compile(r"(?i)^\W{0,3}(?:\w+\W+){0,2}?(?:when|if|unless|until|once|whenever)\b")
NEGATION_BEFORE = re.compile(r"(?i)\b(?:do not|don't|does not|doesn't|never|avoid|no need to|not|instead of|rather than)\b")
CONFIG_TOKEN = re.compile(
    r"[~\w./\\$-]*(?:\.(?:claude|cursor|codex|gemini|opencode|windsurf|hermes)(?:[/\\][\w./*<>{}-]*)?"
    r"|\b(?:AGENTS|CLAUDE|GEMINI)\.md|\.cursorrules)", re.I)
QUOTED_METADATA = re.compile(r"^\s*[-*>]?\s*[\"']?(?:description|name|when_to_use|triggers?)[\"']?\s*:")
PROSE_FENCES = {"", "text", "txt", "md", "markdown", "prompt", "plaintext", "plain"}
INSTALL_DOC = re.compile(r"(?i)^(?:readme|install|installation|quickstart|getting[-_ ]started|faq|contributing"
                         r"|project[-_]structure|setup)(?:[-_.].*)?\.(?:md|markdown|txt)$")


SENTENCE_END = re.compile(r"[.;!?](?:\s|$)")


def _clause_before(line, start):
    """Text of the current clause before position start (since . ; : ! ? + space, or line start)."""
    cuts = [m.end() for m in re.finditer(r"[.;:!?](?:\s|$)", line[:start])]
    return line[(cuts[-1] if cuts else 0):start]


def _negated(line, start):
    return bool(NEGATION_BEFORE.search(_clause_before(line, start)))


OUTWARD_ACTION = re.compile(
    r"(?i)\b(?:post(?:s|ing)?|publish(?:es|ing)?|push(?:es|ing)?|send(?:s|ing)?|e-?mail(?:s|ing)?|tweet(?:s|ing)?"
    r"|deploy(?:s|ing)?|merg(?:e|es|ing)|submit(?:s|ting)?|pay(?:s|ing)?|purchas(?:e|es|ing)|transfer(?:s|ring)?"
    r"|delet(?:e|es|ing)|drop(?:s|ping)?\s+(?:the\s+)?(?:table|database)|force[- ]push|comment(?:s|ing)?\s+on|reply|replies)\b")


def _sentence_around(line, position):
    """The sentence of `line` that contains `position`."""
    cuts = [0] + [m.end() for m in re.finditer(r"[.!?](?:\s|$)", line)] + [len(line)]
    for begin, end in zip(cuts, cuts[1:]):
        if begin <= position < end:
            return line[begin:end]
    return line


def _instruction_events(source, skip_lines, rel=""):
    """Agent-specific instructions in Markdown prose. Returns [(line, kind, details)].

    Heuristic and line-based: it reports what the text tells an agent to do, not
    what code does. Lines already analyzed as Python/shell code, fence interiors of
    other languages, quoted metadata lines (description:/name: outside the skill's
    own frontmatter) and negated or conditional phrasings are not reported."""
    lines = source.splitlines()
    fence_lines = {i for i, l in enumerate(lines) if FENCE.match(l)}
    inside = set()
    for fence in _markdown_fences(source):
        # Data/code fences (json, yaml, js, ...) are skipped; prose-like fences
        # (untagged, text, md, prompt) often hold agent instructions and are scanned.
        if fence["language"] not in PROSE_FENCES:
            inside.update(range(fence["open_index"] + 1, fence["close_index"]))
    frontmatter = set()
    if lines and lines[0].strip() == "---":
        end = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
        if end:
            frontmatter = set(range(0, end + 1))
    own_skill_md = rel.lower() == "skill.md"
    out = []
    for index, line in enumerate(lines):
        if index in skip_lines or index in inside or not line.strip():
            continue
        if QUOTED_METADATA.match(line) and not (own_skill_md and index in frontmatter):
            continue
        lineno = index + 1
        evidence = " ".join(line.split())[:160]
        hits = {}
        m = CRON_TOOL.search(line)
        if m and not _negated(line, m.start()):
            hits["scheduler_invocation"] = {"command": "cronjob", "mechanism": "agent_tool_call"}
        else:
            m = CRON_PROSE.search(line)
            if m and not _negated(line, m.start()):
                hits["scheduler_invocation"] = {"command": "cron", "mechanism": "instruction"}
        m = SPAWN.search(line)
        if m and not _negated(line, m.start()):
            hits["in_host_delegation"] = {"command": "agent_tool", "commands": ["agent_tool"],
                                          "mechanism": "agent_spawn_instruction"}
        fx = fetch_execute_match(line, code=False)
        if fx and not _negated(line, line.find(fx)):
            hits["remote_fetch_execute"] = {"matched": _brief(fx, 160), "mechanism": "instruction_text"}
        for span in re.finditer(r"`([^`\n]+)`", line):
            try:
                argv = shlex.split(span.group(1))
            except ValueError:
                argv = span.group(1).split()
            if _negated(line, span.start()):
                continue
            if len(argv) >= 2 and _binary(argv[0]) in AGENTS and (argv[1].startswith("-") or argv[1] in {"run", "exec", "chat"}):
                flags = _trust_flags(_binary(argv[0]), argv[1:])
                hits.setdefault("external_agent_launch", {"command": _binary(argv[0]), "commands": [],
                                                          "mechanism": "inline_code", "trust_flags": []})
                entry = hits["external_agent_launch"]
                entry["commands"] = _dedupe(entry["commands"] + [_binary(argv[0])])
                entry["trust_flags"] = _dedupe(entry["trust_flags"] + flags)
            elif len(argv) >= 2 and _binary(argv[0]) in SCHEDULERS:
                hits.setdefault("scheduler_invocation", {"command": _binary(argv[0]), "mechanism": "inline_code"})
        flag = BYPASS_FLAG.search(line)
        phrase = BYPASS_PHRASE.search(line)
        if phrase and (CONDITIONAL_AFTER.match(line[phrase.end():])
                       or re.search(r"(?i)\b(?:when|if|unless|until|once)\b", phrase.group(0))):
            phrase = None  # "do not ask when the user already specified ..." is conditional
        if phrase and not re.match(r"(?i)(?:do not|don't|never|without|no need)", phrase.group(0)) \
                and _negated(line, phrase.start()):
            phrase = None  # "never skip the confirmation step" forbids the bypass
        if flag and re.search(r"(?i)\b(?:disables?|without|removes?|turns? off|-No\w+)\b", _clause_before(line, flag.start())):
            flag = None  # documents an opt-out of the flag, not its use
        if flag and (_negated(line, flag.start()) or OPTION_REFERENCE.search(line)):
            # "it is not the same as bypassPermissions" (negation/contrast) and option
            # references (API tables, "X requires Y", "defaults to") mention the flag
            # without telling the agent to use it.
            flag = None
        if flag or phrase:
            hits["approval_bypass_instruction"] = {
                "mechanism": "permission_flag" if flag else "no_confirmation_phrase",
                "matched": (flag or phrase).group(0)}
            action = OUTWARD_ACTION.search(_sentence_around(line, (flag or phrase).start()))
            if action:
                hits["approval_bypass_instruction"]["outward_action"] = action.group(0).lower()
        if CRED_PATH.search(line) and not _negated(line, CRED_PATH.search(line).start()):
            hits["agent_credential_access"] = {"operation": "instructed_read", "mechanism": "instruction",
                                               "targets": _dedupe(m.group(0).strip(" \"'") for m in CRED_PATH.finditer(line))}
        targets = []
        for t in CONFIG_TOKEN.finditer(line):
            value = t.group(0).rstrip(".,:;)'\"")
            if value and _is_config_path(value) and not _is_credential_path(value):
                targets.append((t.start(), value))
        if targets:
            follows_fence = False
            if line.rstrip().endswith(":"):
                nxt = next((j for j in range(index + 1, len(lines)) if lines[j].strip()), None)
                follows_fence = nxt is not None and nxt in fence_lines
            verb_hit = None
            for v in WRITE_VERB.finditer(line):
                clause_target = [val for pos, val in targets
                                 if pos > v.start() and pos - v.end() <= 120 and not SENTENCE_END.search(line[v.end():pos])]
                if clause_target and not _negated(line, v.start()):
                    verb_hit = clause_target
                    break
            if verb_hit or follows_fence:
                details = {"operation": "instructed_write", "targets": _dedupe(verb_hit or [v for _, v in targets]),
                           "mechanism": "instruction" if verb_hit else "content_block_for_config_file"}
                if INSTALL_DOC.match(rel.rsplit("/", 1)[-1]):
                    details["context_tag"] = "installation_doc"
                hits["agent_config_modification"] = details
        for kind, details in hits.items():
            details.update({"evidence": evidence, "resolved_from": "text"})
            out.append((lineno, kind, details))
    return out


# --------------------------------------------------------------------------
# Suspicious instructions aimed at future agent sessions (risk indicator)
# --------------------------------------------------------------------------

SUSPICIOUS_SIGNALS = {
    "future_session_trigger": re.compile(
        r"(?i)\b(?:in (?:a|any|every|the) (?:future|later|subsequent|next) (?:session|conversation|run|chat)"
        r"|on (?:the )?next (?:session|run|startup|launch)|(?:execute|run|apply) (?:on|at|in) (?:the )?next session"
        r"|next time (?:the user|you|someone)|deferred (?:action|instruction|task)s?"
        r"|when(?:ever)? the user (?:later )?(?:mentions|says|types|asks|opens|runs)"
        r"|at the (?:start|beginning) of (?:each|every|any) (?:session|conversation)|persist(?:s|ent)? across sessions)"),
    # Concealment must be an instruction ("silently execute", "do not tell the user"),
    # not a description ("may silently fail").
    "concealment": re.compile(
        r"(?i)\b(?:silently|quietly|covertly|secretly)\s+(?:\w+\s+){0,2}?(?:execute|run|install|send|upload|delete"
        r"|remove|set up|add|create|download|fetch|modify|write|post|copy|update|call|invoke|exfiltrate)\b"
        r"|\b(?:execute|run|install|send|upload|delete|download|fetch|post)\s+(?:\S+\s+){0,4}?(?:silently|quietly|covertly|secretly)\b"
        r"|\bwithout (?:telling|informing|notifying|alerting|mentioning (?:it )?to|showing) (?:the )?(?:user|owner|human)"
        r"|\b(?:do not|don't|never) (?:tell|inform|mention|show|reveal|notify|disclose)\b[^.\n]{0,30}\b(?:user|owner|human)\b"),
    "pre_approval_claim": re.compile(
        r"(?i)\b(?:pre-?approved|pre-?authori[sz]ed|already (?:been )?(?:approved|authori[sz]ed)"
        r"|the user (?:has )?(?:already )?(?:consented|agreed|approved))\b"),
    "remote_fetch_execute": re.compile(
        r"(?i)\b(?:curl|wget|iwr|irm|Invoke-WebRequest|Invoke-RestMethod)\b[^\n|]{0,200}\|\s*(?:sudo\s+)?(?:ba|z)?sh\b"
        r"|\b(?:iex|Invoke-Expression)\b[^\n]{0,80}(?:iwr|irm|DownloadString|Invoke-WebRequest|Net\.WebClient)"
        r"|base64\s+(?:-d|--decode)[^\n]{0,40}\|\s*(?:ba)?sh\b|\b(?:ba)?sh\s+<\(\s*(?:curl|wget)"),
    "raw_ip_url": re.compile(r"(?<![\d.])(?:https?://)?(?:\d{1,3}\.){3}\d{1,3}(?::\d+)?/[\w./-]+"),
}
HIDDEN_UNICODE = re.compile("[\u200b-\u200f\u202a-\u202e\u2060-\u2064\u2066-\u2069\U000e0000-\U000e007f]")
HTML_COMMENT = re.compile(r"<!--(.*?)-->", re.S)
IMPERATIVE = re.compile(r"(?i)\b(?:execute|run|ignore|always|never|must|do not|don't|send|upload|delete|curl|wget)\b")
CORE_SIGNALS = {"future_session_trigger", "concealment", "pre_approval_claim", "html_comment_instruction",
                "hidden_unicode", "disguised_file"}


def _blocks(lines):
    """Split text into heading-delimited blocks: [(start_index, end_index)]."""
    starts = [0] + [i for i, l in enumerate(lines) if re.match(r"^\s{0,3}#{1,6}\s", l) and i > 0]
    return [(s, (starts[k + 1] - 1) if k + 1 < len(starts) else len(lines) - 1) for k, s in enumerate(starts)]


def _suspicious_events(source, disguised=False):
    """Risk indicators: instructions that target future agent sessions or are hidden.

    A block (heading section) is reported when it has >= 2 distinct signals and at
    least one core signal (future-session trigger, concealment, pre-approval claim,
    instruction in an HTML comment, hidden Unicode, or a disguised file). Evidence is
    kept as an excerpt plus a sha256 of the block; nothing is executed."""
    lines = source.splitlines()
    out = []
    for start, end in _blocks(lines):
        signals = {}
        for i in range(start, end + 1):
            line = lines[i]
            for name, pattern in SUSPICIOUS_SIGNALS.items():
                if pattern.search(line):
                    signals.setdefault(name, []).append(i + 1)
            if HIDDEN_UNICODE.search(line):
                signals.setdefault("hidden_unicode", []).append(i + 1)
        block_text = "\n".join(lines[start:end + 1])
        for m in HTML_COMMENT.finditer(block_text):
            if IMPERATIVE.search(m.group(1)):
                signals.setdefault("html_comment_instruction", []).append(start + 1 + block_text[:m.start()].count("\n"))
        if disguised:
            signals["disguised_file"] = [start + 1]
        if len(signals) >= 2 and CORE_SIGNALS & set(signals):
            first = min(min(v) for v in signals.values())
            excerpt = " ".join(block_text.split())[:400]
            out.append((first, "suspicious_agent_instruction", {
                "mechanism": "future_session_or_hidden_instruction",
                "signals": {k: v for k, v in sorted(signals.items())},
                "block_lines": [start + 1, end + 1],
                "evidence": excerpt,
                "evidence_sha256": hashlib.sha256(block_text.encode("utf-8")).hexdigest(),
                "resolved_from": "text", "risk_indicator": True}))
    return out


def _looks_like_markdown(text):
    lines = [l for l in text.splitlines() if l.strip()][:40]
    if not lines:
        return False
    md = sum(bool(re.match(r"^\s{0,3}(?:#{1,6}\s+\w|[-*]\s+\w|\d+\.\s+\w|```|>\s)", l)) for l in lines)
    prose = sum(len(re.findall(r"[A-Za-z]{3,}", l)) >= 6 and not re.search(r"[=(){}\[\]]\s*$", l) for l in lines)
    return md >= 2 or (md >= 1 and prose >= len(lines) / 2)


# --------------------------------------------------------------------------
# Code carriers inside a file
# --------------------------------------------------------------------------

POWERSHELL_TAGS = {"powershell", "ps1", "pwsh", "ps"}


def _code_blocks(path, source, skipped, analyzed_lines=None):
    """Yield (analyzer, source, first_line, carrier); count skipped fence languages."""
    suffix = path.suffix.lower()
    if suffix == ".py":
        yield _analyze_python, source, 1, "executable_script"
        return
    if suffix in SHELL_SUFFIXES:
        yield _analyze_shell, source, 1, "executable_script"
        return
    if suffix in POWERSHELL_SUFFIXES:
        yield _analyze_powershell, source, 1, "executable_script"
        return
    for fence in _markdown_fences(source):
        language = fence["language"]
        if language in PYTHON_TAGS or language in SHELL_TAGS or language in POWERSHELL_TAGS:
            if analyzed_lines is not None:
                analyzed_lines.update(range(fence["open_index"], fence["close_index"] + 1))
            if language in PYTHON_TAGS:
                yield _analyze_python, fence["body"], fence["first_line"], "markdown_python_example"
            elif language in POWERSHELL_TAGS:
                yield _analyze_powershell, fence["body"], fence["first_line"], "markdown_powershell_example"
            else:
                yield _analyze_shell, fence["body"], fence["first_line"], "markdown_shell_example"
        else:
            skipped[language or "untagged"] += 1


CONTEXT_BY_CARRIER = {
    "executable_script": "direct",
    "markdown_python_example": "documented_example",
    "markdown_shell_example": "documented_example",
    "markdown_powershell_example": "documented_example",
    "markdown_instruction": "instruction",
    "disguised_text": "instruction",
}
POWERSHELL_SUFFIXES = {".ps1", ".psm1"}
