import unittest
from pathlib import Path

from tools.allowlist import rules


APP = Path(__file__).resolve().parents[1] / "examples" / "app" / "justfile"


class AllowlistTests(unittest.TestCase):
    def test_app_example(self):
        permissions = rules(APP)["permissions"]
        self.assertEqual(permissions["allow"], [
            "Bash(just)",
            "Bash(just --list *)",
            "Bash(just doctor)",
            "Bash(just help)",
            "Bash(just test)",
            "Bash(just db status)",
        ])
        self.assertEqual(permissions["ask"], ["Bash(just release deploy *)"])

    def test_local_recipes_get_no_rule(self):
        commands = " ".join(sum(rules(APP)["permissions"].values(), []))
        self.assertNotIn("just check", commands)
        self.assertNotIn("just db migrate", commands)


if __name__ == "__main__":
    unittest.main()
