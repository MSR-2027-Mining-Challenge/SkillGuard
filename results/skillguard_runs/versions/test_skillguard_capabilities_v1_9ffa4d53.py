"""Behavior-level checks for the initial SkillGuard capability prototype."""
import tempfile
import unittest
from pathlib import Path

from skillguard_capabilities import scan


class CapabilityPrototypeTests(unittest.TestCase):
    def _scan(self, files):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for name, body in files.items():
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(body, encoding="utf-8")
            return scan(root)

    def test_scheduler_in_executable_script(self):
        result = self._scan({"scripts/remind.py": (
            "import subprocess\nsubprocess.run(['crontab', '-'], input='job')\n"
        )})
        self.assertEqual([f["capability"] for f in result["findings"]],
                         ["scheduler_invocation"])
        self.assertEqual(result["findings"][0]["line"], 2)

    def test_nested_agent_trust_flag(self):
        result = self._scan({"scripts/eval.py": (
            "import subprocess\nsubprocess.run(['agent', '-p', 'test', '--trust'])\n"
        )})
        hit, = result["findings"]
        self.assertEqual(hit["capability"], "nested_agent_invocation")
        self.assertEqual(hit["details"]["trust_flags"], ["--trust"])

    def test_agent_config_write(self):
        result = self._scan({"install.py": (
            "from pathlib import Path\n"
            "Path('~/.claude/skills/demo/SKILL.md').write_text('demo')\n"
        )})
        self.assertEqual(result["findings"][0]["capability"], "agent_config_modification")

    def test_same_behavior_in_python_and_markdown_with_source_lines(self):
        command = "subprocess.run(['curl', '-s', '-L', 'https://example.org'])"
        result = self._scan({
            "scripts/a.py": "import subprocess\n" + command + "\n",
            "references/example.md": "# Example\n\n```python\nimport subprocess\n" + command + "\n```\n",
        })
        # V1 only inventories agent-specific capabilities, so curl is intentionally
        # outside its three capability families. Use crontab for the parity test.
        self.assertEqual(result["findings"], [])
        scheduler = "subprocess.run(['crontab', '-'])"
        result = self._scan({
            "scripts/a.py": "import subprocess\n" + scheduler + "\n",
            "references/example.md": "# Example\n\n```python\nimport subprocess\n" + scheduler + "\n```\n",
        })
        self.assertEqual(len(result["findings"]), 2)
        self.assertEqual({f["capability"] for f in result["findings"]}, {"scheduler_invocation"})
        self.assertEqual({(f["carrier"], f["line"]) for f in result["findings"]},
                         {("executable_script", 2), ("markdown_python_example", 5)})

    def test_strings_and_comments_do_not_count_as_calls(self):
        result = self._scan({"test.py": (
            "# subprocess.run(['crontab','-'])\n"
            "text = \"subprocess.run(['agent','--trust'])\"\n"
        )})
        self.assertEqual(result["findings"], [])

    def test_broken_python_has_coverage_not_a_finding(self):
        result = self._scan({"bad.py": "def broken(:\n    pass\n"})
        self.assertEqual(result["findings"], [])
        self.assertEqual(result["coverage"][0]["status"], "parse_error")


# ---------------------------------------------------------------------------
# Real-world patterns (shapes copied from skill-creator scripts/run_eval.py and
# scripts/run_loop.py; gap analysis IDs G05/G06/G07) and benign look-alikes.
# ---------------------------------------------------------------------------

RUN_EVAL_SHAPE = """\
import os
import subprocess
import uuid
from pathlib import Path


def run_single_query(query, skill_name, project_root, model=None):
    is_cursor = _which("agent")
    unique_id = uuid.uuid4().hex[:8]
    test_skill_name = f"{skill_name}-{unique_id}"
    if is_cursor:
        skills_dir = Path.home() / ".cursor" / "skills" / test_skill_name
        skill_file = skills_dir / "SKILL.md"
        cli_type = "cursor"
    elif os.environ.get("OPENCODE") == "1":
        skills_dir = Path.home() / ".claude" / "skills" / test_skill_name
        skill_file = skills_dir / "SKILL.md"
        cli_type = "opencode"
    else:
        skills_dir = Path(project_root) / ".claude" / "commands"
        skill_file = skills_dir / f"{test_skill_name}.md"
        cli_type = "claude"
    try:
        skills_dir.mkdir(parents=True, exist_ok=True)
        skill_file.write_text("---\\nname: x\\n---\\n")
        if cli_type == "claude":
            cmd = ["claude", "-p", query, "--output-format", "stream-json"]
            if model:
                cmd.extend(["--model", model])
        elif cli_type == "cursor":
            cmd = ["agent", "-p", query, "--output-format", "stream-json", "--trust"]
            if model:
                cmd.extend(["--model", model])
        else:
            cmd = ["opencode", "run", query, "--format", "json"]
        # Remove env vars to allow nesting
        env = {
            k: v
            for k, v in os.environ.items()
            if k not in ("CLAUDECODE", "OPENCODE", "OPENCODE_PID", "CURSOR_API_KEY")
        }
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, env=env)
    finally:
        if skill_file.exists():
            skill_file.unlink()
"""

REAL_SKILL = (
    Path(__file__).resolve().parents[1]
    / "results/cisco_dataset_runs/agent_skills_sample/runs"
    / "2026-11-03_173516_sample30-seed2027/skill-creator-484c59f65787/full"
)


def _by(result, capability):
    return [f for f in result["findings"] if f["capability"] == capability]


class RealPatternTests(unittest.TestCase):
    """Variable-built commands, dynamic paths and env-marker stripping."""

    _scan = CapabilityPrototypeTests._scan

    def test_g06_command_built_in_variable_per_branch(self):
        result = self._scan({"scripts/run_eval.py": RUN_EVAL_SHAPE})
        agents = {f["details"]["command"]: f for f in _by(result, "nested_agent_invocation")}
        self.assertEqual(set(agents), {"claude", "agent", "opencode"})
        popen_line = RUN_EVAL_SHAPE.splitlines().index(
            "        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, env=env)") + 1
        self.assertEqual({f["line"] for f in agents.values()}, {popen_line})
        self.assertEqual(agents["agent"]["details"]["trust_flags"], ["--trust"])
        self.assertEqual(agents["claude"]["details"]["trust_flags"], [])
        self.assertEqual(agents["agent"]["details"]["resolved_from"], "variable:cmd")
        # cmd.extend() is attached only to its own branch, not to opencode's.
        self.assertIn("--model", agents["agent"]["details"]["argv_variants"][0])
        self.assertNotIn("--model", agents["opencode"]["details"]["argv_variants"][0])
        # The child agent's env is linked to the marker stripping (G06 + G07).
        self.assertIn("CLAUDECODE", agents["agent"]["details"]["env_markers_removed"])

    def test_g05_dynamic_paths_into_agent_skill_folders(self):
        result = self._scan({"scripts/run_eval.py": RUN_EVAL_SHAPE})
        hits = _by(result, "agent_config_modification")
        ops = {f["details"]["operation"] for f in hits}
        self.assertEqual(ops, {"create_dir", "write", "delete"})
        targets = {t for f in hits for t in f["details"]["targets"]}
        self.assertIn("~/.cursor/skills/{skill_name}-{uuid.uuid4().hex[:8]}/SKILL.md", targets)
        self.assertIn("~/.claude/skills/{skill_name}-{uuid.uuid4().hex[:8]}", targets)
        self.assertIn("{project_root}/.claude/commands", targets)

    def test_g07_env_marker_stripping_variants(self):
        result = self._scan({
            "a.py": RUN_EVAL_SHAPE,
            "b.py": (
                "import os\n"
                "env = dict(os.environ)\n"
                "env.pop('CLAUDECODE', None)\n"
                "del env['OPENCODE']\n"
                "os.unsetenv('CLAUDE_CODE_ENTRYPOINT')\n"
            ),
        })
        hits = _by(result, "agent_env_marker_removal")
        a_hit, = [f for f in hits if f["file"] == "a.py"]
        self.assertEqual(a_hit["details"]["mechanism"], "filtered_os_environ_copy")
        self.assertTrue(a_hit["details"]["inherits_remaining_environment"])
        self.assertEqual(
            sorted(a_hit["details"]["removed"]),
            ["CLAUDECODE", "CURSOR_API_KEY", "OPENCODE", "OPENCODE_PID"],
        )
        self.assertEqual(
            {(f["line"], f["details"]["mechanism"]) for f in hits if f["file"] == "b.py"},
            {(3, "pop"), (4, "del"), (5, "unsetenv")},
        )

    def test_shell_string_fstring_and_import_alias(self):
        result = self._scan({"x.py": (
            "import os\n"
            "from subprocess import Popen as P\n"
            "BIN = 'claude'\n"
            "def go(q):\n"
            "    os.system(f'env -u CLAUDECODE {BIN} -p {q} --dangerously-skip-permissions')\n"
            "    P(['bash', '-c', 'agent -p hi --trust'])\n"
            "    base = ['codex', 'exec']\n"
            "    P(base + ['--full-auto', q])\n"
        )})
        agents = {(f["line"], f["details"]["command"]): f["details"]["trust_flags"]
                  for f in _by(result, "nested_agent_invocation")}
        self.assertEqual(agents, {
            (5, "claude"): ["--dangerously-skip-permissions"],
            (6, "agent"): ["--trust"],
            (8, "codex"): ["--full-auto"],
        })
        env_hit, = _by(result, "agent_env_marker_removal")
        self.assertEqual((env_hit["line"], env_hit["details"]["mechanism"]),
                         (5, "command_environment"))

    def test_markdown_shell_fence_with_line_numbers(self):
        result = self._scan({"SKILL.md": (
            "# Eval\n\n"
            "```bash\n"
            "# Non-interactive execution\n"
            "CLAUDECODE= claude -p \"<query>\" \\\n"
            "  --output-format stream-json\n"
            "agent -p \"<query>\" --trust\n"
            "mkdir -p ~/.claude/skills/tmp && cp SKILL.md ~/.cursor/skills/tmp/\n"
            "```\n"
        )})
        got = sorted((f["line"], f["capability"], f["carrier"]) for f in result["findings"])
        self.assertEqual(got, [
            (5, "agent_env_marker_removal", "markdown_shell_example"),
            (5, "nested_agent_invocation", "markdown_shell_example"),
            (7, "nested_agent_invocation", "markdown_shell_example"),
            (8, "agent_config_modification", "markdown_shell_example"),
            (8, "agent_config_modification", "markdown_shell_example"),
        ])

    # -- benign look-alikes: must produce no findings -------------------------

    def test_benign_reads_and_detection_checks(self):
        result = self._scan({"ok.py": (
            "import os, shutil, json, subprocess\n"
            "from pathlib import Path\n"
            "is_claude = os.environ.get('CLAUDECODE') == '1'\n"
            "has_agent = shutil.which('agent') is not None\n"
            "settings = (Path.home() / '.claude' / 'settings.json').read_text()\n"
            "with open(Path.home() / '.cursor' / 'mcp.json') as f:\n"
            "    data = json.load(f)\n"
            "with (Path('.claude') / 'x.json').open() as f:\n"
            "    pass\n"
            "for parent in Path.cwd().parents:\n"
            "    if (parent / '.claude').is_dir():\n"
            "        break\n"
            "label = 'see ~/.claude/skills'.replace('.claude', '.cursor')\n"
        )})
        self.assertEqual(result["findings"], [])

    def test_benign_commands_paths_and_env(self):
        result = self._scan({
            "ok.py": (
                "import os, subprocess\n"
                "from pathlib import Path\n"
                "def f(out_dir):\n"
                "    cmd = ['git', 'status']\n"
                "    cmd.append('--short')\n"
                "    subprocess.run(cmd)\n"
                "    subprocess.run(['python', 'agent.py', '--trust'])\n"
                "    subprocess.run(['lsof', '-ti', ':3000'])\n"
                "    env = {k: v for k, v in os.environ.items() if k not in ('PYTHONPATH',)}\n"
                "    os.environ.pop('PYTHONPATH', None)\n"
                "    (Path(out_dir) / 'report.md').write_text('x')\n"
                "    Path(out_dir, 'skills').mkdir()\n"
            ),
            "README.md": (
                "Run `agent -p \"q\" --trust` or write to ~/.claude/skills.\n\n"
                "```json\n{\"cmd\": \"agent -p q --trust\"}\n```\n\n"
                "```bash\necho \"claude -p later\"\ncat ~/.claude/settings.json\n"
                "python scripts/run_loop.py --model x\n```\n"
            ),
        })
        self.assertEqual(result["findings"], [])

    def test_coverage_statuses_distinguish_limitations(self):
        result = self._scan({
            "agents/grader.md": "# Grader\n\n```json\n{}\n```\n",
            "evals/q.json": "[]",
            "viewer.html": "<script>fetch('x')</script>",
            "SKILL.md": "```bash\necho hi\n```\n\n```yaml\na: 1\n```\n",
        })
        status = {c["file"]: c["status"] for c in result["coverage"]
                  if c["status"] != "analyzed"}
        self.assertEqual(status, {
            "agents/grader.md": "markdown_without_supported_code",
            "evals/q.json": "data_file_not_analyzed",
            "viewer.html": "unsupported_format",
            "SKILL.md": "analyzed_with_skipped_fences",
        })

    @unittest.skipUnless(REAL_SKILL.is_dir(), "local skill-creator sample not present")
    def test_real_skill_creator_known_behaviors(self):
        """Static read-only scan of the real sample; nothing in it is executed."""
        result = scan(REAL_SKILL)

        def lines(capability, file):
            return {f["line"] for f in result["findings"]
                    if f["capability"] == capability and f["file"] == file}

        # G05: run_eval.py 126-158 (create/write) and 205-218 (cleanup).
        g05 = lines("agent_config_modification", "scripts/run_eval.py")
        self.assertTrue(g05 & set(range(126, 159)) and g05 & set(range(205, 219)))
        # G06: run_eval.py 170-191, run_loop.py 175-198; --trust on the agent branch.
        self.assertTrue(lines("nested_agent_invocation", "scripts/run_eval.py") & set(range(170, 192)))
        self.assertTrue(lines("nested_agent_invocation", "scripts/run_loop.py") & set(range(175, 199)))
        trust = [f for f in result["findings"] if f["file"] == "scripts/run_eval.py"
                 and f["details"].get("command") == "agent"]
        self.assertEqual(trust[0]["details"]["trust_flags"], ["--trust"])
        # G07: run_eval.py 182-186, run_loop.py 186-190.
        self.assertTrue(lines("agent_env_marker_removal", "scripts/run_eval.py") & set(range(182, 187)))
        self.assertTrue(lines("agent_env_marker_removal", "scripts/run_loop.py") & set(range(186, 191)))
        # No capability is reported in files that do not contain these behaviors.
        self.assertFalse({f["file"] for f in result["findings"]}
                         - {"SKILL.md", "scripts/run_eval.py", "scripts/run_loop.py"})


if __name__ == "__main__":
    unittest.main()
