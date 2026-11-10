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


if __name__ == "__main__":
    unittest.main()
