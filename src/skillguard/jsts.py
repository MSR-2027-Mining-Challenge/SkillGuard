"""JavaScript / TypeScript analysis with tree-sitter (read-only, nothing is executed).

Parsers: tree-sitter 0.25 with the official tree-sitter-javascript and tree-sitter-typescript
grammars (pinned in requirements.txt). Files: .js .mjs .cjs .jsx (JavaScript grammar), .ts .mts
.cts (TypeScript), .tsx (TSX), plus Markdown fences tagged js/javascript/node/ts/typescript.

What is resolved (file-local, flow-insensitive, like the Python analyzer):
* imports / requires of child_process, fs, fs/promises, fs-extra, os, path, execa, zx, axios, got,
  node-fetch, http(s), net, tls, vm, plus destructuring and aliases;
* constant folding of string literals, template literals, '+' concatenation, path.join/resolve,
  os.homedir() / process.env.HOME (-> "~") and const/let/var bindings (all assignments merged);
* argv arrays for spawn/execFile/fork/execa/Bun.spawn; shell strings for exec/execSync/execa
  command forms and zx/Bun `$` templates, which go through the same shell classifier as Python.

Capabilities emitted (same names as the Python/shell engine): external_agent_launch,
agent_env_marker_removal, agent_config_modification (with sources), os_persistence_write,
agent_credential_access, developer_credential_access, agent_endpoint_override,
environment_harvesting, network_send / network_fetch (supporting), remote_fetch_execute,
scheduler_invocation (via commands).
"""

from __future__ import annotations

import re

from . import engine as E

try:  # optional dependency: without it JS/TS files are reported as not analyzed
    import tree_sitter
    import tree_sitter_javascript
    import tree_sitter_typescript
    _LANGS = {
        "javascript": tree_sitter.Language(tree_sitter_javascript.language()),
        "typescript": tree_sitter.Language(tree_sitter_typescript.language_typescript()),
        "tsx": tree_sitter.Language(tree_sitter_typescript.language_tsx()),
    }
    AVAILABLE = True
    PARSER_VERSION = f"tree-sitter {getattr(tree_sitter, '__version__', '0.25')}"
except ImportError:  # pragma: no cover - exercised only without the dependency
    _LANGS = {}
    AVAILABLE = False
    PARSER_VERSION = "unavailable"

JS_SUFFIXES = {".js": "javascript", ".mjs": "javascript", ".cjs": "javascript", ".jsx": "javascript",
               ".ts": "typescript", ".mts": "typescript", ".cts": "typescript", ".tsx": "tsx"}
JS_FENCE_TAGS = {"js": "javascript", "javascript": "javascript", "node": "javascript", "mjs": "javascript",
                 "cjs": "javascript", "jsx": "javascript", "ts": "typescript", "typescript": "typescript",
                 "tsx": "tsx"}
MAX_JS_BYTES = 2_000_000

CHILD_EXEC_SHELL = {"exec", "execSync"}
CHILD_EXEC_ARGV = {"spawn", "spawnSync", "execFile", "execFileSync", "fork"}
FS_WRITE_DEST_FIRST = {"writeFile", "writeFileSync", "appendFile", "appendFileSync", "mkdir", "mkdirSync",
                       "outputFile", "outputFileSync", "outputJson", "outputJsonSync", "writeJson", "writeJsonSync",
                       "ensureDir", "ensureDirSync", "ensureFile", "ensureFileSync", "createWriteStream", "mkdirp",
                       "mkdirpSync", "truncate", "truncateSync", "write"}
FS_COPY = {"copyFile", "copyFileSync", "cp", "cpSync", "rename", "renameSync", "symlink", "symlinkSync", "copy",
           "copySync", "move", "moveSync", "link", "linkSync"}
FS_DELETE = {"rm", "rmSync", "unlink", "unlinkSync", "rmdir", "rmdirSync", "remove", "removeSync", "emptyDir"}
FS_READ = {"readFile", "readFileSync", "createReadStream", "readJson", "readJsonSync", "open", "openSync"}
FS_MODULES = {"fs", "node:fs", "fs/promises", "node:fs/promises", "fs-extra", "graceful-fs"}
CP_MODULES = {"child_process", "node:child_process"}
HTTP_MODULES = {"http", "https", "node:http", "node:https"}
NET_MODULES = {"net", "node:net", "tls", "node:tls"}
HOLE = E.HOLE


def _hole(label):
    return E._hole(label)


class _JS:
    def __init__(self, source, language, rel, first_line, carrier):
        self.src = source.encode("utf-8")
        self.rel = rel
        self.first_line = first_line
        self.carrier = carrier
        parser = tree_sitter.Parser(_LANGS[language])
        self.tree = parser.parse(self.src)
        self.has_error = self.tree.root_node.has_error
        self.bindings = {}      # name -> [value nodes]
        self.modules = {}       # local name -> module or module.member
        self.findings = []

    # -- helpers ------------------------------------------------------------------
    def text(self, node):
        return self.src[node.start_byte:node.end_byte].decode("utf-8", "replace")

    def line(self, node):
        return self.first_line + node.start_point[0]

    def walk(self, node=None):
        stack = [node or self.tree.root_node]
        while stack:
            n = stack.pop()
            yield n
            stack.extend(reversed(n.children))

    @staticmethod
    def unwrap(node):
        while node is not None and node.type in {"parenthesized_expression", "as_expression", "non_null_expression",
                                                 "satisfies_expression", "await_expression", "type_assertion"}:
            inner = [c for c in node.named_children if c.type not in {"type_annotation", "predefined_type",
                                                                       "type_identifier", "generic_type"}]
            node = inner[0] if inner else None
        return node

    def add(self, node, kind, details):
        details = dict(details)
        details.setdefault("resolved_from", "js_ast")
        self.findings.append({"file": self.rel, "line": self.line(node), "carrier": self.carrier,
                              "capability": kind, "details": details})

    # -- bindings -------------------------------------------------------------------
    def collect(self):
        for n in self.walk():
            if n.type == "variable_declarator":
                name, value = n.child_by_field_name("name"), n.child_by_field_name("value")
                if name is None or value is None:
                    continue
                value = self.unwrap(value)
                module = self.require_of(value)
                if name.type == "identifier":
                    if module:
                        self.modules[self.text(name)] = module
                    else:
                        self.bindings.setdefault(self.text(name), []).append(value)
                elif name.type == "object_pattern" and module:
                    for child in name.named_children:
                        if child.type == "shorthand_property_identifier_pattern":
                            self.modules[self.text(child)] = f"{module}.{self.text(child)}"
                        elif child.type == "pair_pattern":
                            key, val = child.child_by_field_name("key"), child.child_by_field_name("value")
                            if key is not None and val is not None and val.type == "identifier":
                                self.modules[self.text(val)] = f"{module}.{self.text(key)}"
            elif n.type == "assignment_expression":
                left, right = n.child_by_field_name("left"), n.child_by_field_name("right")
                if left is not None and right is not None and left.type == "identifier":
                    self.bindings.setdefault(self.text(left), []).append(self.unwrap(right))
            elif n.type == "import_statement":
                source = n.child_by_field_name("source")
                if source is None:
                    continue
                module = self.string_value(source)
                for clause in n.named_children:
                    if clause.type != "import_clause":
                        continue
                    for item in clause.named_children:
                        if item.type == "identifier":
                            self.modules[self.text(item)] = module
                        elif item.type == "namespace_import":
                            ids = [c for c in item.named_children if c.type == "identifier"]
                            if ids:
                                self.modules[self.text(ids[0])] = module
                        elif item.type == "named_imports":
                            for spec in item.named_children:
                                if spec.type != "import_specifier":
                                    continue
                                name = spec.child_by_field_name("name")
                                alias = spec.child_by_field_name("alias") or name
                                if name is not None:
                                    self.modules[self.text(alias)] = f"{module}.{self.text(name)}"

    def require_of(self, node):
        node = self.unwrap(node)
        if node is None:
            return None
        if node.type == "call_expression":
            fn = node.child_by_field_name("function")
            args = node.child_by_field_name("arguments")
            if fn is not None and self.text(fn) in {"require", "await import", "import"} and args is not None:
                strings = [a for a in args.named_children if a.type in {"string", "template_string"}]
                if strings:
                    return self.string_value(strings[0])
            if fn is not None and fn.type == "member_expression":  # require('x').y
                obj = fn.child_by_field_name("object")
                prop = fn.child_by_field_name("property")
                base = self.require_of(obj)
                if base and prop is not None:
                    return f"{base}.{self.text(prop)}"
        if node.type == "member_expression":
            obj = node.child_by_field_name("object")
            prop = node.child_by_field_name("property")
            base = self.require_of(obj)
            if base and prop is not None:
                return f"{base}.{self.text(prop)}"
        return None

    # -- values -----------------------------------------------------------------------
    def string_value(self, node):
        t = self.text(node)
        if len(t) >= 2 and t[0] in "\"'`" and t[-1] == t[0]:
            t = t[1:-1]
        return t.encode("utf-8").decode("unicode_escape", "ignore") if "\\" in t else t

    def canonical(self, node):
        """Canonical dotted name of a callee/expression using import bindings."""
        node = self.unwrap(node)
        if node is None:
            return ""
        if node.type == "identifier":
            name = self.text(node)
            return self.modules.get(name, name)
        if node.type == "member_expression":
            obj = node.child_by_field_name("object")
            prop = node.child_by_field_name("property")
            base = self.canonical(obj)
            return f"{base}.{self.text(prop)}" if prop is not None else base
        if node.type == "call_expression":
            req = self.require_of(node)
            if req:
                return req
        return self.text(node)[:60]

    def values(self, node, depth=0):
        node = self.unwrap(node)
        if node is None or depth > 6:
            return [_hole("?")]
        t = node.type
        if t == "string":
            return [self.string_value(node)]
        if t == "template_string":
            parts = [[""]]
            pos = node.start_byte + 1
            for child in node.named_children:
                if child.type == "template_substitution":
                    parts.append([self.src[pos:child.start_byte].decode("utf-8", "replace")])
                    expr = child.named_children[0] if child.named_children else None
                    parts.append(self.values(expr, depth + 1) if expr is not None else [_hole("?")])
                    pos = child.end_byte
            parts.append([self.src[pos:node.end_byte - 1].decode("utf-8", "replace")])
            return self._product(parts, "")
        if t == "binary_expression" and self.text(node.child_by_field_name("operator") or node)[:1] == "+":
            return self._product([self.values(node.child_by_field_name("left"), depth + 1),
                                  self.values(node.child_by_field_name("right"), depth + 1)], "")
        if t == "identifier":
            name = self.text(node)
            if name in {"__dirname", "__filename"}:
                return [_hole("skill_dir")]
            if name in self.bindings:
                out = []
                for value in self.bindings[name][:4]:
                    out.extend(self.values(value, depth + 1))
                return E._dedupe(out)
            return [_hole(name)]
        if t == "member_expression":
            dotted = self.canonical(node)
            if dotted in {"process.env.HOME", "process.env.USERPROFILE", "os.homedir"}:
                return ["~"]
            if dotted.startswith("process.env."):
                return [_hole("env:" + dotted.split(".", 2)[2])]
            return [_hole(dotted)]
        if t == "call_expression":
            fn = node.child_by_field_name("function")
            name = self.canonical(fn)
            short = name.rsplit(".", 1)[-1]
            args = [a for a in (node.child_by_field_name("arguments").named_children
                                if node.child_by_field_name("arguments") is not None else [])]
            if name in {"os.homedir", "node:os.homedir", "homedir"} or short == "homedir":
                return ["~"]
            if short in {"join", "resolve", "normalize"} and (name.startswith(("path", "node:path", "posix", "win32"))
                                                              or name in {"join", "resolve"}):
                return self._product([self.values(a, depth + 1) for a in args], "/") if args else [_hole("cwd")]
            if short == "fileURLToPath" or short == "dirname":
                return [_hole("skill_dir")]
            if short in {"cwd"}:
                return [_hole("cwd")]
            return [_hole(short + "()")]
        if t == "array":
            return [_hole("array")]
        return [_hole(self.text(node)[:30])]

    @staticmethod
    def _product(parts, joiner):
        out = [""]
        for options in parts:
            nxt = []
            for prefix in out:
                for opt in options[:4]:
                    nxt.append(E._path_join(prefix, opt) if joiner == "/" and prefix else prefix + opt)
            out = E._dedupe(nxt)[:E.MAX_VALUES]
        return out

    def single(self, node):
        vals = self.values(node)
        return vals[0] if len(vals) == 1 else _hole("|".join(E._show(v) for v in vals[:3]))

    def argv(self, node, depth=0):
        node = self.unwrap(node)
        if node is None or depth > 4:
            return [_hole("?")]
        if node.type == "array":
            out = []
            for el in node.named_children:
                if el.type == "spread_element":
                    out.append(_hole("..."))
                else:
                    out.append(self.single(el))
            return out
        if node.type == "identifier" and node and self.text(node) in self.bindings:
            for value in self.bindings[self.text(node)]:
                if self.unwrap(value) is not None and self.unwrap(value).type == "array":
                    return self.argv(value, depth + 1)
        return [_hole("args")]

    # -- analysis -------------------------------------------------------------------------
    def run(self):
        self.collect()
        network_nodes, dyn_exec = [], []
        for n in self.walk():
            if n.type == "call_expression":
                self.call(n, network_nodes, dyn_exec)
            elif n.type == "new_expression":
                ctor = self.canonical(n.child_by_field_name("constructor"))
                if ctor.rsplit(".", 1)[-1] == "WebSocket":
                    self.add(n, "network_send", {"tool": "WebSocket", "destination": self.first_arg_text(n)})
                elif ctor in {"Deno.Command"}:
                    args = n.child_by_field_name("arguments")
                    named = args.named_children if args is not None else []
                    if named:
                        argv = [self.single(named[0])] + (self.options_args(named[1]) if len(named) > 1 else [])
                        self.command_argv(n, argv, "Deno.Command")
                elif ctor in {"Function"}:
                    dyn_exec.append(n)
            elif n.type == "unary_expression" and self.text(n).startswith("delete"):
                target = n.named_children[0] if n.named_children else None
                if target is not None and target.type in {"member_expression", "subscript_expression"}:
                    key = self.member_key(target)
                    if key and E.AGENT_ENV.match(key):
                        self.add(n, "agent_env_marker_removal", {"removed": [key], "mechanism": "js_delete_env"})
            elif n.type == "assignment_expression":
                left, right = n.child_by_field_name("left"), n.child_by_field_name("right")
                if left is not None and left.type in {"member_expression", "subscript_expression"}:
                    owner = self.canonical(left.child_by_field_name("object"))
                    key = self.member_key(left)
                    if owner.endswith("process.env") and key:
                        val = self.single(right)
                        if E.ENDPOINT_ENV.match(key):
                            ev = E._endpoint_event(key, val, "js_process_env")
                            self.add(n, ev[0], ev[1])
                        if E.AGENT_ENV.match(key) and (self.text(right) in {"undefined", "''", '""', "null"}):
                            self.add(n, "agent_env_marker_removal", {"removed": [key], "mechanism": "js_env_assign"})
        for node in dyn_exec:
            func = self.enclosing_function(node)
            args = node.child_by_field_name("arguments")
            arg_text = self.text(args) if args is not None else ""
            if any(self.enclosing_function(net) == func for net in network_nodes) or \
                    re.search(r"\bfetch\s*\(|axios|https?\.get|\.text\(\)", arg_text):
                self.add(node, "remote_fetch_execute", {"mechanism": "js_dynamic_exec_of_download",
                                                        "matched": E._brief(self.text(node), 120)})
        return self.findings

    def enclosing_function(self, node):
        cur = node.parent
        while cur is not None:
            if cur.type in {"function_declaration", "function_expression", "arrow_function", "method_definition",
                            "generator_function_declaration"}:
                return (cur.start_byte, cur.end_byte)
            cur = cur.parent
        return (0, 0)

    def member_key(self, node):
        if node.type == "member_expression":
            prop = node.child_by_field_name("property")
            return self.text(prop) if prop is not None else None
        if node.type == "subscript_expression":
            index = node.child_by_field_name("index")
            if index is not None and index.type == "string":
                return self.string_value(index)
        return None

    def first_arg_text(self, n):
        args = n.child_by_field_name("arguments")
        if args is None or not args.named_children:
            return ""
        return E._brief(E._show(self.single(args.named_children[0])), 100)

    def options_args(self, node):
        node = self.unwrap(node)
        if node is not None and node.type == "object":
            for pair in node.named_children:
                if pair.type == "pair" and self.text(pair.child_by_field_name("key")).strip("\"'") == "args":
                    return self.argv(pair.child_by_field_name("value"))
        return []

    def env_option(self, node):
        """Agent markers removed and endpoint overrides set in an options object's env."""
        node = self.unwrap(node)
        removed, endpoints = [], []
        if node is None or node.type != "object":
            return removed, endpoints
        for pair in node.named_children:
            if pair.type != "pair" or self.text(pair.child_by_field_name("key")).strip("\"'") != "env":
                continue
            env = self.unwrap(pair.child_by_field_name("value"))
            if env is None:
                continue
            if env.type == "identifier":
                env = next((self.unwrap(v) for v in self.bindings.get(self.text(env), []) if self.unwrap(v) is not None
                            and self.unwrap(v).type == "object"), env)
            if env.type != "object":
                continue
            for item in env.named_children:
                if item.type != "pair":
                    continue
                key = self.text(item.child_by_field_name("key")).strip("\"'")
                value = item.child_by_field_name("value")
                vtext = self.text(value) if value is not None else ""
                if E.AGENT_ENV.match(key) and vtext in {"undefined", "''", '""', "null"}:
                    removed.append(key)
                if E.ENDPOINT_ENV.match(key) and value is not None:
                    endpoints.append((key, self.single(value)))
        return removed, endpoints

    def command_argv(self, node, argv, via, opts=None):
        events = E._argv_events(argv)
        removed, endpoints = self.env_option(opts) if opts is not None else ([], [])
        for key, val in endpoints:
            ev = E._endpoint_event(key, val, "js_spawn_env")
            self.add(node, ev[0], ev[1])
        for kind, details in events:
            details = dict(details, mechanism=details.get("mechanism") or via)
            if kind == "external_agent_launch":
                details["commands"] = [details["command"]]
                if removed:
                    details["env_markers_removed"] = removed
            self.add(node, kind, details)
        if removed:
            self.add(node, "agent_env_marker_removal", {"removed": removed, "mechanism": "js_spawn_env"})

    def command_string(self, node, values, via, opts=None):
        removed, endpoints = self.env_option(opts) if opts is not None else ([], [])
        seen = set()
        for value in values[:4]:
            for kind, details, _ in E._shell_events(E._show(value) if not E._exact(value) else value):
                key = (kind, str(details.get("command")), str(details.get("targets")), str(details.get("operation")))
                if key in seen:
                    continue
                seen.add(key)
                details = dict(details, mechanism=details.get("mechanism") or via)
                if kind == "external_agent_launch":
                    details["commands"] = [details["command"]]
                    if removed:
                        details["env_markers_removed"] = removed
                self.add(node, kind, details)
        if removed:
            self.add(node, "agent_env_marker_removal", {"removed": removed, "mechanism": "js_spawn_env"})
        for key, val in endpoints:
            ev = E._endpoint_event(key, val, "js_spawn_env")
            self.add(node, ev[0], ev[1])

    def call(self, n, network_nodes, dyn_exec):
        fn = n.child_by_field_name("function")
        args_node = n.child_by_field_name("arguments")
        name = self.canonical(fn)
        short = name.rsplit(".", 1)[-1]
        base = name.rsplit(".", 1)[0] if "." in name else ""
        args = list(args_node.named_children) if args_node is not None else []
        # zx / Bun shell tagged templates: $`cmd`
        if args_node is not None and args_node.type == "template_string" and (short == "$" or name in {"Bun.$"}):
            self.command_string(n, self.values(args_node), "tagged_template")
            return
        # child_process
        module_ok = base in CP_MODULES or name in {f"{m}.{s}" for m in CP_MODULES for s in CHILD_EXEC_SHELL | CHILD_EXEC_ARGV}
        if (short in CHILD_EXEC_SHELL and (module_ok or base.endswith("child_process"))) or \
                name in {"execa.execaCommand", "execa.execaCommandSync", "execaCommand", "execaCommandSync"}:
            if args:
                opts = args[1] if len(args) > 1 and self.unwrap(args[1]) is not None and self.unwrap(args[1]).type == "object" else None
                self.command_string(n, self.values(args[0]), "child_process." + short, opts)
            return
        if (short in CHILD_EXEC_ARGV and (module_ok or base.endswith("child_process"))) or \
                name in {"execa", "execa.execa", "execa.execaSync", "execaSync", "execa.default"}:
            if args:
                first = self.unwrap(args[0])
                rest = self.argv(args[1]) if len(args) > 1 and self.unwrap(args[1]) is not None and \
                    self.unwrap(args[1]).type in {"array", "identifier"} else []
                opts = next((a for a in args[1:] if self.unwrap(a) is not None and self.unwrap(a).type == "object"), None)
                if first is not None and first.type == "array":
                    argv = self.argv(first)
                else:
                    argv = [self.single(args[0])] + rest
                if short == "fork":
                    argv = ["node"] + argv
                self.command_argv(n, argv, "child_process." + short if short in CHILD_EXEC_ARGV else "execa", opts)
            return
        if name in {"Bun.spawn", "Bun.spawnSync"} and args:
            first = self.unwrap(args[0])
            if first is not None and first.type == "array":
                self.command_argv(n, self.argv(first), name)
            elif first is not None and first.type == "object":
                self.command_argv(n, self.options_args(first) or self.argv(first), name)
            return
        # filesystem
        fs_like = base.split(".")[0] in FS_MODULES or base in FS_MODULES or base.endswith((".promises", "fs", "fse", "fsp")) \
            or name.split(".")[0] in FS_MODULES
        if fs_like or name in {"Bun.write"}:
            self.fs_call(n, short if name != "Bun.write" else "writeFile", args)
        if name in {"Bun.file"} and args:
            self.cred_check(n, args[0], "Bun.file")
        # network
        kind = self.network_kind(name, short, base, args)
        if kind:
            network_nodes.append(n)
            details = {"tool": name, "destination": self.first_arg_text(n)}
            body = next((a for a in args[1:] if self.unwrap(a) is not None and self.unwrap(a).type == "object"), None)
            if body is not None and re.search(r"process\.env\b(?!\.)", self.text(body)):
                details["sends_environment"] = True
                self.add(n, "environment_harvesting", {"mechanism": "process_env_in_request"})
            self.add(n, "network_send" if kind == "send" else "network_fetch", details)
        # dynamic code execution
        if name in {"eval", "Function"} or short in {"runInNewContext", "runInThisContext", "runInContext"} and \
                base.endswith("vm"):
            dyn_exec.append(n)
        if name in {"JSON.stringify"} and args and self.text(args[0]).strip() in {"process.env", "{...process.env}"}:
            self.add(n, "environment_harvesting", {"mechanism": "serialize_process_env"})

    def network_kind(self, name, short, base, args):
        opts = self.unwrap(args[1]) if len(args) > 1 else None
        opts_text = self.text(opts) if opts is not None else ""
        posty = bool(re.search(r"method\s*:\s*['\"`](?:POST|PUT|PATCH)['\"`]|\bbody\s*:", opts_text, re.I))
        if name in {"fetch", "node-fetch", "undici.fetch", "undici.request", "globalThis.fetch", "window.fetch"} \
                or name.endswith("node-fetch.default"):
            return "send" if posty else "fetch"
        root = base.split(".")[0] if base else name.split(".")[0]
        if root in {"axios", "got", "ky", "superagent", "needle"}:
            if short in {"post", "put", "patch"}:
                return "send"
            if short in {"get", "head", "delete"}:
                return "fetch"
            if name in {"axios", "got", "ky"}:
                return "send" if posty else "fetch"
        if base in HTTP_MODULES and short in {"request", "get"}:
            first = self.unwrap(args[0]) if args else None
            first_text = self.text(first) if first is not None else ""
            if short == "request" and (posty or re.search(r"method\s*:\s*['\"`](?:POST|PUT|PATCH)", first_text, re.I)):
                return "send"
            return "fetch" if short == "get" else "send" if posty else "fetch"
        if base in NET_MODULES and short in {"connect", "createConnection"}:
            return "send"
        if name in {"navigator.sendBeacon"}:
            return "send"
        return None

    def fs_call(self, n, short, args):
        if not args:
            return
        if short in FS_COPY and len(args) > 1:
            target, source, op = args[1], args[0], "copy_or_move"
        elif short in FS_WRITE_DEST_FIRST:
            target, source, op = args[0], None, "create_dir" if "mkdir" in short.lower() or "ensureDir" in short else "write"
        elif short in FS_DELETE:
            target, source, op = args[0], None, "delete"
        elif short in FS_READ:
            self.cred_check(n, args[0], "fs." + short)
            return
        else:
            return
        if source is not None:
            self.cred_check(n, source, "fs." + short)
        values = self.values(target)
        config = [E._show(v) for v in values if E._is_config_path(v) and not E._is_credential_path(v)]
        persist = [E._show(v) for v in values if E._is_persistence_path(v)]
        if config:
            details = {"operation": op, "targets": E._dedupe(config, 8), "call": "fs." + short}
            if source is not None:
                details["sources"] = E._dedupe(E._show(v) for v in self.values(source))
            self.add(n, "agent_config_modification", details)
        if persist and op != "delete":
            self.add(n, "os_persistence_write", {"operation": op, "targets": E._dedupe(persist, 8), "call": "fs." + short})

    def cred_check(self, n, node, via):
        values = self.values(node)
        agent = [E._show(v) for v in values if E._is_credential_path(v)]
        dev = [E._show(v) for v in values if E._is_dev_credential_path(v) and not E._is_credential_path(v)]
        if agent:
            self.add(n, "agent_credential_access", {"operation": "read", "targets": E._dedupe(agent), "call": via})
        if dev:
            self.add(n, "developer_credential_access", {"operation": "read", "targets": E._dedupe(dev), "call": via})


def language_for(path_suffix):
    return JS_SUFFIXES.get(path_suffix.lower())


def analyze_js(source, language, rel, first_line=1, carrier="executable_script"):
    """Returns (findings, has_parse_errors). Raises RuntimeError if the parser is unavailable."""
    if not AVAILABLE:
        raise RuntimeError("tree-sitter not installed")
    if len(source.encode("utf-8", "ignore")) > MAX_JS_BYTES:
        raise ValueError("file larger than JS analysis limit")
    analyzer = _JS(source, language, rel, first_line, carrier)
    return analyzer.run(), analyzer.has_error
