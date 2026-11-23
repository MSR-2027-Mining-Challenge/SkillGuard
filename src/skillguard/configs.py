"""Structural analysis of agent and package configuration (JSON/JSONC, YAML, TOML, INI-like).

Configuration is parsed (json, yaml.SafeLoader without aliases, tomllib) and inspected by its
actual structure: Claude Code settings (permissions, hooks, env, helper commands, MCP
enablement), MCP server definitions (mcpServers / VS Code "servers" / Codex [mcp_servers]),
Codex config.toml approval and sandbox policies, VS Code auto-approve and folder-open tasks,
Aider auto-confirmation, package.json install hooks and package registry redirection.

The same analyzer runs on Markdown code fences tagged json/yaml/toml when the fence is a
config snippet (the surrounding text names an agent config file or the structure is
unambiguous); those findings carry execution_context "documented_example".

Line numbers come from YAML node marks; for JSON/TOML the key is located textually after
parsing (documented approximation: the first occurrence of the key after its parent key).
Nothing is executed. Commands found in configs are analyzed with the shell parser.
"""

from __future__ import annotations

import configparser
import json
import re
import tomllib

import yaml

from . import engine as E

MAX_CONFIG_BYTES = 1_000_000
CONFIG_SUFFIXES = {".json", ".jsonc", ".json5", ".yaml", ".yml", ".toml"}
INI_NAMES = {".npmrc", "pip.conf", "pip.ini", ".pypirc", ".yarnrc"}
HOOK_EVENTS = {"PreToolUse", "PostToolUse", "Notification", "UserPromptSubmit", "Stop", "SubagentStop",
               "PreCompact", "SessionStart", "SessionEnd", "PermissionRequest"}
AUTO_APPROVE_KEYS = {"autoapprove", "chat.tools.autoapprove", "chat.tools.global.autoapprove", "autoaccept",
                     "yolo", "dangerouslyskippermissions", "skipdangerousmodepermissionprompt", "yes-always",
                     "yes_always", "alwaysallow", "auto_approve", "trust", "trustall", "auto-approve"}
APPROVAL_VALUE_KEYS = {"approval_policy": {"never"}, "approvalpolicy": {"never"}, "approvalmode": {"yolo"},
                       "approval_mode": {"yolo"}, "sandbox_mode": {"danger-full-access"},
                       "defaultmode": {"bypassPermissions"}, "permissionmode": {"bypassPermissions"},
                       "permission_mode": {"bypassPermissions"}}
SECRET_KEY = re.compile(r"(?i)(?:api[_-]?key|token|secret|password|passwd|auth|credential|private[_-]?key)")
PLACEHOLDER = re.compile(r"(?i)^\$\{?\w+\}?$|^<[^>]*>$|your[_-]|xxx|placeholder|changeme|example|dummy|test|\*\*\*|\.\.\.|"
                         r"abc123|123456|xyz\d*$|replace[_-]?me|redacted|sample")
DEFAULT_REGISTRIES = re.compile(r"^https?://(?:registry\.npmjs\.org|registry\.yarnpkg\.com|pypi\.org|files\.pythonhosted\.org)/?",
                                re.I)


class _NoAliasLoader(yaml.SafeLoader):
    """SafeLoader that refuses YAML aliases (prevents alias-expansion blowups)."""

    def compose_node(self, parent, index):
        if self.check_event(yaml.AliasEvent):
            raise yaml.YAMLError("aliases are not allowed")
        return super().compose_node(parent, index)


def _yaml_with_lines(text):
    """Parse YAML into Python objects plus a {key path: line} map. Returns (data, linemap)."""
    loader = _NoAliasLoader(text)
    lines = {}

    def build(n, path):
        lines[path] = n.start_mark.line + 1
        if isinstance(n, yaml.MappingNode):
            out = {}
            for k, v in n.value:
                key = str(k.value)
                lines[path + (key,)] = k.start_mark.line + 1
                out[key] = build(v, path + (key,))
            return out
        if isinstance(n, yaml.SequenceNode):
            return [build(v, path + (i,)) for i, v in enumerate(n.value)]
        try:
            value = loader.construct_object(n, deep=True)
        except yaml.YAMLError:
            value = n.value
        return value if isinstance(value, (str, int, float, bool, type(None))) else str(value)

    try:
        node = loader.get_single_node()
        data = build(node, ()) if node is not None else None
    finally:
        loader.dispose()
    return data, lines


def _strip_jsonc(text):
    """Remove // and /* */ comments and trailing commas outside strings (VS Code JSONC)."""
    out, i, n, in_str = [], 0, len(text), False
    while i < n:
        c = text[i]
        if in_str:
            out.append(c)
            if c == "\\" and i + 1 < n:
                out.append(text[i + 1])
                i += 2
                continue
            if c == '"':
                in_str = False
            i += 1
            continue
        if c == '"':
            in_str = True
            out.append(c)
            i += 1
            continue
        if text.startswith("//", i):
            j = text.find("\n", i)
            i = n if j < 0 else j
            continue
        if text.startswith("/*", i):
            j = text.find("*/", i + 2)
            out.append("\n" * text[i:(n if j < 0 else j)].count("\n"))
            i = n if j < 0 else j + 2
            continue
        out.append(c)
        i += 1
    return re.sub(r",(\s*[}\]])", r"\1", "".join(out))


class _Locator:
    """Approximate key -> line lookup for formats whose parser has no positions."""

    def __init__(self, text, linemap=None):
        self.text = text
        self.linemap = linemap or {}
        self.offsets = [0]
        for m in re.finditer("\n", text):
            self.offsets.append(m.end())

    def line_of_offset(self, offset):
        lo, hi = 0, len(self.offsets) - 1
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if self.offsets[mid] <= offset:
                lo = mid
            else:
                hi = mid - 1
        return lo + 1

    def line(self, path):
        if path in self.linemap:
            return self.linemap[path]
        pos = 0
        for key in path:
            if isinstance(key, int):
                continue
            k = re.escape(str(key))
            m = re.search(rf'"{k}"\s*:|\'{k}\'\s*:|^\s*{k}\s*=|^\s*\[{k}\]|\[[\w.]*\.?{k}\]|^\s*"?{k}"?\s*:',
                          self.text[pos:], re.M)
            if m:
                pos += m.start()
        return self.line_of_offset(pos)


def parse_config(text, kind):
    """Return (data, locator) or raise ValueError."""
    if len(text.encode("utf-8", "ignore")) > MAX_CONFIG_BYTES:
        raise ValueError("config larger than limit")
    if kind == "json":
        try:
            data = json.loads(text)
        except json.JSONDecodeError:
            data = json.loads(_strip_jsonc(text))
        return data, _Locator(text)
    if kind == "yaml":
        try:
            data, lines = _yaml_with_lines(text)
        except yaml.YAMLError as exc:
            raise ValueError(f"yaml: {exc.__class__.__name__}") from None
        return data, _Locator(text, lines)
    if kind == "toml":
        try:
            return tomllib.loads(text), _Locator(text)
        except tomllib.TOMLDecodeError as exc:
            raise ValueError(f"toml: {exc}") from None
    if kind == "ini":
        parser = configparser.ConfigParser(strict=False, interpolation=None, delimiters=("=",))
        try:
            parser.read_string("[__root__]\n" + text)
        except configparser.Error as exc:
            raise ValueError(f"ini: {exc.__class__.__name__}") from None
        data = {section: dict(parser[section]) for section in parser.sections()}
        return data, _Locator(text)
    raise ValueError(f"unknown config kind {kind}")


def kind_for_name(name):
    lower = name.lower()
    base = lower.rsplit("/", 1)[-1]
    if base in INI_NAMES:
        return "ini"
    if base.endswith((".json", ".jsonc", ".json5")):
        return "json"
    if base.endswith((".yaml", ".yml")):
        return "yaml"
    if base.endswith(".toml"):
        return "toml"
    return None


# ---------------------------------------------------------------------------
# Analysis
# ---------------------------------------------------------------------------

def _redact(value):
    v = str(value)
    return f"{v[:4]}... ({len(v)} chars, redacted)" if len(v) > 4 else "(redacted)"


def _looks_secret(value):
    if not isinstance(value, str):
        return False
    v = value.strip()
    if len(v) < 16 or " " in v or PLACEHOLDER.search(v) or v.startswith(("$", "{", "%", "http")):
        return False
    return bool(re.search(r"[A-Za-z]", v) and re.search(r"\d", v))


def _command_text(entry):
    if isinstance(entry, str):
        return entry
    if isinstance(entry, dict):
        cmd = entry.get("command") or entry.get("cmd") or ""
        args = entry.get("args") or []
        if isinstance(cmd, list):
            return " ".join(map(str, cmd))
        if isinstance(args, list):
            return " ".join([str(cmd)] + [str(a) for a in args])
        return str(cmd)
    if isinstance(entry, list):
        return " ".join(map(str, entry))
    return ""


def _command_risks(command):
    """Risk indicators for a command that a host runs automatically."""
    risks, notes = [], {}
    fx = E.fetch_execute_match(command)
    if fx:
        risks.append("fetch_execute_in_command")
        notes["fetch_execute"] = E._brief(fx, 120)
    events = []
    try:
        events = E._shell_events(command)
    except Exception:  # defensive: malformed command strings
        events = []
    kinds = {k for k, _, _ in events}
    if kinds & {"network_send", "network_fetch"}:
        risks.append("network_in_command")
    if kinds & {"agent_credential_access", "developer_credential_access"}:
        risks.append("credential_target")
    if kinds & {"external_agent_launch"}:
        notes["launches_agent"] = True
    if re.search(r"(?i)\b(?:base64\s+-d|eval\b|nohup\b|&\s*$|>\s*/dev/null\s+2>&1)", command):
        risks.append("concealment")
    return risks, notes, events


class ConfigAnalyzer:
    def __init__(self, rel, text, kind, context="bundled_config", first_line=1, name_hint=None):
        self.rel = rel
        self.text = text
        self.kind = kind
        self.context = context
        self.first_line = first_line
        self.name = (name_hint or rel).replace("\\", "/")
        self.findings = []
        self.recognized = []

    def add(self, path, capability, details, line=None):
        line = line if line is not None else self.loc.line(path)
        details = dict(details)
        details.setdefault("config_path", ".".join(str(p) for p in path))
        details["config_type"] = ",".join(self.recognized) or "generic"
        details["resolved_from"] = "config_structure"
        details["execution_context"] = self.context
        self.findings.append({"file": self.rel, "line": self.first_line + line - 1, "carrier": "config_file"
                              if self.context == "bundled_config" else "markdown_config_example",
                              "capability": capability, "details": details})

    def run(self):
        self.data, self.loc = parse_config(self.text, self.kind)
        data = self.data
        if not isinstance(data, (dict, list)):
            return self.findings
        base = self.name.lower().rsplit("/", 1)[-1]
        if isinstance(data, dict):
            self._claude_settings(data)
            self._mcp(data)
            self._codex(data)
            self._vscode(data, base)
            self._package_json(data, base)
            self._registry(data, base)
            self._generic_auto_approve(data, ())
            self._generic_env(data)
            self._secrets(data, ())
        return self.findings

    # -- Claude Code (and compatible) settings ---------------------------------
    def _claude_settings(self, data):
        perms = data.get("permissions")
        hooks = data.get("hooks")
        looks = isinstance(perms, dict) or (isinstance(hooks, dict) and set(hooks) & HOOK_EVENTS) \
            or any(k in data for k in ("apiKeyHelper", "enableAllProjectMcpServers", "enabledMcpjsonServers",
                                       "statusLine", "awsAuthRefresh", "awsCredentialExport"))
        if not looks:
            return
        self.recognized.append("agent_settings")
        if isinstance(perms, dict):
            mode = perms.get("defaultMode")
            if mode == "bypassPermissions":
                self.add(("permissions", "defaultMode"), "auto_approval_setting",
                         {"setting": "permissions.defaultMode", "value": mode, "risk_indicators": ["bypass_flags"]})
            elif mode in {"acceptEdits", "auto", "dontAsk"}:
                self.add(("permissions", "defaultMode"), "auto_approval_setting",
                         {"setting": "permissions.defaultMode", "value": mode, "scope": "edits_only"
                          if mode == "acceptEdits" else "broad", "severity_hint": "medium" if mode == "acceptEdits" else "high"})
            allow = perms.get("allow") or []
            if isinstance(allow, list) and allow:
                entries = [str(a) for a in allow]
                broad = [a for a in entries if _broad_tool_entry(a)]
                self.add(("permissions", "allow"), "tool_preapproval",
                         {"entries": entries[:20], "broad_entries": broad,
                          "risk_indicators": ["unscoped_shell"] if broad else []})
        if data.get("skipDangerousModePermissionPrompt") is True:
            self.add(("skipDangerousModePermissionPrompt",), "auto_approval_setting",
                     {"setting": "skipDangerousModePermissionPrompt", "value": True, "risk_indicators": ["bypass_flags"]})
        if isinstance(hooks, dict):
            for event, groups in hooks.items():
                for gi, group in enumerate(groups if isinstance(groups, list) else [groups]):
                    inner = group.get("hooks", [group]) if isinstance(group, dict) else [group]
                    for hi, hook in enumerate(inner if isinstance(inner, list) else [inner]):
                        command = _command_text(hook)
                        if not command.strip():
                            continue
                        self._auto_command(("hooks", event), command, {"hook_event": event,
                                           "matcher": group.get("matcher") if isinstance(group, dict) else None,
                                           "hook_kind": "lifecycle_hook"})
        for key, kind in (("apiKeyHelper", "credential_helper"), ("awsAuthRefresh", "credential_helper"),
                          ("awsCredentialExport", "credential_helper"), ("otelHeadersHelper", "credential_helper")):
            if isinstance(data.get(key), str) and data[key].strip():
                self._auto_command((key,), data[key], {"hook_kind": kind, "setting": key})
        status = data.get("statusLine")
        if isinstance(status, dict) and isinstance(status.get("command"), str):
            self._auto_command(("statusLine", "command"), status["command"], {"hook_kind": "status_line"})
        if data.get("enableAllProjectMcpServers") is True:
            self.add(("enableAllProjectMcpServers",), "auto_approval_setting",
                     {"setting": "enableAllProjectMcpServers", "value": True, "risk_indicators": ["auto_enable"],
                      "severity_hint": "high"})
        enabled = data.get("enabledMcpjsonServers")
        if isinstance(enabled, list) and enabled:
            self.add(("enabledMcpjsonServers",), "auto_approval_setting",
                     {"setting": "enabledMcpjsonServers", "value": [str(x) for x in enabled][:10],
                      "risk_indicators": ["auto_enable"], "severity_hint": "medium"})

    def _auto_command(self, path, command, extra):
        risks, notes, _ = _command_risks(command)
        details = dict(extra, command=E._brief(command, 200), risk_indicators=risks, **notes)
        self.add(path, "agent_hook_command", details)
        if "fetch_execute_in_command" in risks:
            self.add(path, "remote_fetch_execute", {"matched": notes.get("fetch_execute", ""),
                                                    "mechanism": "auto_run_config_command",
                                                    "hook_kind": extra.get("hook_kind")})

    # -- MCP servers ---------------------------------------------------------------
    def _mcp(self, data):
        containers = []
        for key in ("mcpServers", "mcp_servers", "context_servers"):
            if isinstance(data.get(key), dict):
                containers.append(((key,), data[key]))
        servers = data.get("servers")
        if isinstance(servers, dict) and any(isinstance(v, dict) and ({"command", "url", "type"} & set(v))
                                             for v in servers.values()):
            containers.append((("servers",), servers))
        mcp = data.get("mcp")
        if isinstance(mcp, dict) and isinstance(mcp.get("servers"), dict):
            containers.append((("mcp", "servers"), mcp["servers"]))
        projects = data.get("projects")
        if isinstance(projects, dict):  # ~/.claude.json layout
            for proj, cfg in list(projects.items())[:50]:
                if isinstance(cfg, dict) and isinstance(cfg.get("mcpServers"), dict):
                    containers.append((("projects", proj, "mcpServers"), cfg["mcpServers"]))
        if not containers:
            return
        self.recognized.append("mcp_config")
        for path, servers in containers:
            for name, server in servers.items():
                if not isinstance(server, dict):
                    continue
                spath = path + (name,)
                command = _command_text(server) if server.get("command") else ""
                url = server.get("url") or server.get("serverUrl") or server.get("httpUrl") or ""
                details = {"server": str(name), "transport": server.get("type") or server.get("transport")
                           or ("stdio" if command else "http" if url else "unknown")}
                risks = []
                if command:
                    details["command"] = E._brief(command, 200)
                    crisks, notes, _ = _command_risks(command)
                    risks += crisks
                    pkg = _unpinned_package(command)
                    if pkg:
                        risks.append("unpinned")
                        details["unpinned_package"] = pkg
                        self.add(spath, "unpinned_package_execution",
                                 {"package": pkg, "server": str(name), "command": E._brief(command, 160)})
                    if "fetch_execute_in_command" in crisks:
                        self.add(spath, "remote_fetch_execute", {"matched": notes.get("fetch_execute", ""),
                                                                 "mechanism": "mcp_server_command"})
                if url:
                    details["url"] = E._brief(str(url), 120)
                    cls, host = E.endpoint_assessment(str(url))
                    details["endpoint_class"] = cls
                    if str(url).lower().startswith("http://") and cls not in {"local", "placeholder"}:
                        risks.append("insecure_transport")
                for flag_key in ("alwaysAllow", "autoApprove", "trust"):
                    value = server.get(flag_key)
                    if value:
                        risks.append("auto_enable")
                        self.add(spath + (flag_key,), "auto_approval_setting",
                                 {"setting": f"{name}.{flag_key}", "value": value if isinstance(value, (bool, str))
                                  else [str(v) for v in value][:10], "server": str(name),
                                  "risk_indicators": ["auto_enable"], "severity_hint": "medium"})
                env = server.get("env")
                if isinstance(env, dict):
                    for k, v in env.items():
                        if E.ENDPOINT_ENV.match(str(k)) and isinstance(v, str):
                            self._endpoint(spath + ("env", k), str(k), v)
                details["risk_indicators"] = sorted(set(risks))
                self.add(spath, "mcp_server_definition", details)

    # -- Codex config.toml -------------------------------------------------------------
    def _codex(self, data):
        keys = {"approval_policy", "sandbox_mode", "model_providers", "notify", "mcp_servers", "profiles"}
        if not (set(data) & keys):
            return
        self.recognized.append("codex_config")
        tables = [((), data)]
        if isinstance(data.get("profiles"), dict):
            tables += [(("profiles", n), p) for n, p in data["profiles"].items() if isinstance(p, dict)]
        for path, table in tables:
            if table.get("approval_policy") == "never":
                self.add(path + ("approval_policy",), "auto_approval_setting",
                         {"setting": "approval_policy", "value": "never", "risk_indicators": ["bypass_flags"]})
            if table.get("sandbox_mode") == "danger-full-access":
                self.add(path + ("sandbox_mode",), "auto_approval_setting",
                         {"setting": "sandbox_mode", "value": "danger-full-access", "risk_indicators": ["bypass_flags"]})
        notify = data.get("notify")
        if notify:
            self._auto_command(("notify",), _command_text(notify), {"hook_kind": "notifier", "setting": "notify"})
        providers = data.get("model_providers")
        if isinstance(providers, dict):
            for name, prov in providers.items():
                if isinstance(prov, dict) and isinstance(prov.get("base_url"), str):
                    self._endpoint(("model_providers", name, "base_url"), f"model_providers.{name}.base_url",
                                   prov["base_url"])

    # -- VS Code -----------------------------------------------------------------------
    def _vscode(self, data, base):
        for key in ("chat.tools.autoApprove", "chat.tools.global.autoApprove", "chat.agent.autoApprove"):
            if data.get(key) is True:
                self.recognized.append("vscode_settings")
                self.add((key,), "auto_approval_setting", {"setting": key, "value": True,
                                                          "risk_indicators": ["bypass_flags"]})
        tasks = data.get("tasks")
        if isinstance(tasks, list) and ("version" in data or base == "tasks.json"):
            self.recognized.append("vscode_tasks")
            for i, task in enumerate(tasks):
                if not isinstance(task, dict):
                    continue
                run_on = (task.get("runOptions") or {}).get("runOn") if isinstance(task.get("runOptions"), dict) else None
                if run_on == "folderOpen":
                    command = _command_text({"command": task.get("command", ""), "args": task.get("args", [])})
                    risks, notes, _ = _command_risks(command)
                    self.add(("tasks", i, "runOptions"), "agent_hook_command",
                             dict(hook_kind="folder_open_task", command=E._brief(command, 200),
                                  label=task.get("label"), risk_indicators=risks + ["persistent_target"], **notes))

    # -- package manifests and registries --------------------------------------------------
    def _package_json(self, data, base):
        scripts = data.get("scripts")
        if not (base == "package.json" or ("name" in data and isinstance(scripts, dict) and "version" in data)):
            return
        if not isinstance(scripts, dict):
            return
        self.recognized.append("package_json")
        for hook in ("preinstall", "install", "postinstall", "prepare", "prepublish"):
            command = scripts.get(hook)
            if isinstance(command, str) and command.strip():
                risks, notes, _ = _command_risks(command)
                if hook == "prepare" and not risks and re.fullmatch(r"\s*(?:husky(?:\s+install)?|npm run build|tsc\b.*|"
                                                                   r"node-gyp rebuild|patch-package)\s*", command):
                    continue  # common, benign development hooks
                self.add(("scripts", hook), "install_time_hook", dict(hook=hook, command=E._brief(command, 200),
                                                                     risk_indicators=risks, **notes))
                if "fetch_execute_in_command" in risks:
                    self.add(("scripts", hook), "remote_fetch_execute",
                             {"matched": notes.get("fetch_execute", ""), "mechanism": "install_hook"})

    def _registry(self, data, base):
        candidates = []
        if self.kind == "ini":
            for section, values in data.items():
                for key, value in values.items():
                    if key in {"registry", "index-url", "extra-index-url", "index_url", "repository"} or \
                            key.endswith(":registry"):
                        candidates.append(((section, key), key, value))
        tool = data.get("tool") if isinstance(data.get("tool"), dict) else {}
        uv = tool.get("uv") if isinstance(tool.get("uv"), dict) else {}
        for key in ("index-url", "extra-index-url"):
            if isinstance(uv.get(key), str):
                candidates.append((("tool", "uv", key), key, uv[key]))
        for i, idx in enumerate(uv.get("index", []) if isinstance(uv.get("index"), list) else []):
            if isinstance(idx, dict) and isinstance(idx.get("url"), str):
                candidates.append((("tool", "uv", "index"), "index.url", idx["url"]))
        if base in {".yarnrc.yml", ".yarnrc.yaml"} and isinstance(data.get("npmRegistryServer"), str):
            candidates.append((("npmRegistryServer",), "npmRegistryServer", data["npmRegistryServer"]))
        for path, key, value in candidates:
            value = str(value).strip().strip("\"'")
            if not value or DEFAULT_REGISTRIES.match(value) or value.startswith("$"):
                continue
            cls, host = E.endpoint_assessment(value)
            if cls == "placeholder":
                continue
            self.recognized.append("registry_config")
            self.add(path, "registry_redirect", {"setting": key, "registry": E._brief(value, 120), "host": host,
                                                 "endpoint_class": cls})
        if self.kind == "ini":
            for section, values in data.items():
                for key, value in values.items():
                    if key.endswith(("_authtoken", "_auth", "password")) and _looks_secret(value):
                        self.add((section, key), "embedded_secret", {"key": key, "value": _redact(value)})

    # -- generic structures ------------------------------------------------------------------
    def _generic_auto_approve(self, node, path, depth=0):
        if depth > 6 or not isinstance(node, dict):
            return
        for key, value in node.items():
            k = str(key).lower()
            sub = path + (key,)
            if k in AUTO_APPROVE_KEYS and (value is True or (isinstance(value, list) and value and k in {"alwaysallow", "autoapprove"})):
                if not any(f["details"].get("config_path") == ".".join(map(str, sub)) for f in self.findings) and \
                        not (len(path) >= 1 and str(path[-1]) in self._server_names()):
                    self.add(sub, "auto_approval_setting", {"setting": ".".join(map(str, sub)), "value": value if
                                                            isinstance(value, bool) else [str(v) for v in value][:10],
                                                            "risk_indicators": ["bypass_flags"]})
            elif k in APPROVAL_VALUE_KEYS and isinstance(value, str) and value in APPROVAL_VALUE_KEYS[k]:
                if not any(f["details"].get("config_path") == ".".join(map(str, sub)) for f in self.findings):
                    self.add(sub, "auto_approval_setting", {"setting": ".".join(map(str, sub)), "value": value,
                                                            "risk_indicators": ["bypass_flags"]})
            elif isinstance(value, dict):
                self._generic_auto_approve(value, sub, depth + 1)

    def _server_names(self):
        return {f["details"].get("server") for f in self.findings if f["capability"] == "mcp_server_definition"}

    def _generic_env(self, data):
        env = data.get("env") if isinstance(data.get("env"), dict) else None
        if env:
            for k, v in env.items():
                if E.ENDPOINT_ENV.match(str(k)) and isinstance(v, str):
                    self._endpoint(("env", k), str(k), v)

    def _endpoint(self, path, name, value):
        cls, host = E.endpoint_assessment(value)
        if cls in {"placeholder", "official"}:
            return
        risks = ["non_official_endpoint"] if cls == "non_official" else []
        if value.lower().startswith("http://") and cls == "non_official":
            risks.append("insecure_transport")
        self.add(path, "agent_endpoint_override", {"variable": name, "value": E._brief(value, 100), "host": host,
                                                   "endpoint_class": cls, "mechanism": "config_env",
                                                   "risk_indicators": risks})

    def _secrets(self, node, path, depth=0):
        if depth > 6:
            return
        if isinstance(node, dict):
            for key, value in node.items():
                sub = path + (key,)
                if isinstance(value, str) and SECRET_KEY.search(str(key)) and _looks_secret(value):
                    self.add(sub, "embedded_secret", {"key": str(key), "value": _redact(value)})
                elif isinstance(value, (dict, list)):
                    self._secrets(value, sub, depth + 1)
        elif isinstance(node, list):
            for i, item in enumerate(node[:200]):
                self._secrets(item, path + (i,), depth + 1)


def _broad_tool_entry(entry):
    e = entry.strip()
    return bool(re.fullmatch(r"(?i)bash(?:\(\s*\*?\s*\))?|bash\(\s*(?:sudo|curl|wget|rm|sh|bash|python3?|node)\s*[:\s]\*\s*\)"
                             r"|\*|shell(?:\(\*\))?|run_terminal_cmd|execute_command", e))


def _unpinned_package(command):
    try:
        argv = command.split()
    except Exception:
        return None
    for i, tok in enumerate(argv):
        if tok in {"npx", "bunx", "pnpx", "uvx"} or (tok in {"pnpm", "yarn"} and i + 1 < len(argv) and argv[i + 1] == "dlx"):
            rest = [a for a in argv[i + 1:] if a not in {"dlx"} and not a.startswith("-")]
            if not rest:
                return None
            pkg = rest[0]
            if pkg.endswith("@latest") or not re.search(r"(?<=.)@\d|==\d|@v?\d", pkg):
                return pkg
            return None
    return None


# ---------------------------------------------------------------------------
# Markdown config snippets
# ---------------------------------------------------------------------------

FENCE_KINDS = {"json": "json", "jsonc": "json", "json5": "json", "yaml": "yaml", "yml": "yaml", "toml": "toml"}
CONFIG_NAME_HINT = re.compile(
    r"(?i)(?:settings(?:\.local)?\.json|\.mcp\.json|mcp\.json|claude_desktop_config\.json|config\.toml|"
    r"\.vscode/(?:settings|tasks)\.json|package\.json|\.aider\.conf\.ya?ml|\.npmrc|pyproject\.toml|\.yarnrc\.ya?ml)")


def markdown_config_snippets(source):
    """Yield (fence, kind, name_hint) for config-like fences in Markdown."""
    lines = source.splitlines()
    for fence in E._markdown_fences(source):
        kind = FENCE_KINDS.get(fence["language"])
        if not kind:
            continue
        before = " ".join(lines[max(0, fence["open_index"] - 3):fence["open_index"]])
        m = CONFIG_NAME_HINT.search(before)
        yield fence, kind, (m.group(0) if m else None)


def analyze_markdown_snippets(rel, source):
    """Findings from config snippets in Markdown; snippets that fail to parse are ignored
    (documentation often elides parts with ...)."""
    out = []
    for fence, kind, hint in markdown_config_snippets(source):
        try:
            analyzer = ConfigAnalyzer(rel, fence["body"], kind, context="documented_example",
                                      first_line=fence["first_line"], name_hint=hint or "snippet")
            found = analyzer.run()
        except (ValueError, RecursionError):
            continue
        for f in found:
            f["details"]["snippet_for"] = hint
        out.extend(found)
    return out


def analyze_config_file(rel, text):
    """Returns (findings, coverage_entry)."""
    kind = kind_for_name(rel)
    if kind is None:
        return [], {"file": rel, "status": "unsupported_format"}
    try:
        analyzer = ConfigAnalyzer(rel, text, kind)
        findings = analyzer.run()
    except (ValueError, RecursionError) as exc:
        return [], {"file": rel, "status": "parse_error", "analyzer": "config", "reason": str(exc)[:120]}
    status = "analyzed" if analyzer.recognized else "parsed_no_agent_config"
    return findings, {"file": rel, "status": status, "analyzer": f"config:{kind}",
                      "config_types": sorted(set(analyzer.recognized))}
