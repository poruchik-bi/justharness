import tempfile
import unittest
from pathlib import Path

from tools.validate import validate


BASE = """# Show commands.
[metadata('effect:read', 'cost:free', 'duration:short')]
help:
    @just --list
"""


class ValidatorTests(unittest.TestCase):
    def check(self, source, selected=None):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "justfile"
            path.write_text(source)
            return validate(path, selected)

    def test_valid_recipe(self):
        self.assertEqual(self.check(BASE), [])

    def test_missing_description(self):
        self.assertIn("recipe needs a description", " ".join(self.check(BASE.replace("# Show commands.\n", ""))))

    def test_missing_effect(self):
        self.assertIn("effect must be", " ".join(self.check(BASE.replace("'effect:read', ", ""))))

    def test_missing_cost(self):
        self.assertIn("cost must be", " ".join(self.check(BASE.replace("'cost:free', ", ""))))

    def test_invalid_cost(self):
        self.assertIn("cost must be", " ".join(self.check(BASE.replace("cost:free", "cost:unknown"))))

    def test_missing_duration(self):
        self.assertIn("duration must be", " ".join(self.check(BASE.replace(", 'duration:short'", ""))))

    def test_invalid_metadata_item(self):
        self.assertIn("invalid metadata", " ".join(self.check(BASE.replace("duration:short", "duration"))))

    def test_duplicate_metadata_key(self):
        self.assertIn("duplicate metadata key", " ".join(self.check(BASE.replace("duration:short'", "duration:short', 'effect:local'"))))

    def test_publish_needs_gate(self):
        self.assertIn("needs gate:", " ".join(self.check(BASE.replace("effect:read", "effect:publish"))))

    def test_verify_target_must_exist(self):
        self.assertIn("verify target", " ".join(self.check(BASE.replace("duration:short'", "duration:short', 'verify:missing'"))))

    def test_verify_target_cannot_be_self(self):
        self.assertIn("verify target", " ".join(self.check(BASE.replace("duration:short'", "duration:short', 'verify:help'"))))

    def test_module_needs_description(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "justfile"
            path.write_text(BASE + "\nmod work\n")
            module = path.parent / "work"
            module.mkdir()
            (module / "mod.just").write_text(BASE)
            self.assertIn("module needs a description", " ".join(validate(path)))

    def test_scoped_check_ignores_legacy_recipe(self):
        legacy = "\nlegacy:\n    @true\n"
        self.assertEqual(self.check(BASE + legacy, {"help"}), [])
        self.assertIn("recipe needs a description", " ".join(self.check(BASE + legacy)))

    def test_scoped_check_rejects_unknown_recipe(self):
        self.assertIn("selected recipe does not exist", " ".join(self.check(BASE, {"missing"})))

    def test_scoped_check_rejects_private_recipe(self):
        self.assertIn("selected recipe is private", " ".join(self.check(BASE + "\n_private:\n    @true\n", {"_private"})))


if __name__ == "__main__":
    unittest.main()
