import os
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import notes


DEPLOY = Path(__file__).resolve().parents[1] / "scripts" / "deploy.py"


def run_deploy(*args, target=""):
    env = {**os.environ, "APP_DEPLOY_DIR": target, "PYTHONDONTWRITEBYTECODE": "1"}
    return subprocess.run([sys.executable, str(DEPLOY), *args], capture_output=True, text=True, env=env)


class NotesTests(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect(":memory:")
        notes.migrate(self.conn)

    def test_migrate_is_idempotent(self):
        self.assertEqual(notes.migrate(self.conn), [])
        self.assertEqual(notes.pending(self.conn), [])

    def test_add_and_recent(self):
        notes.add(self.conn, " first ")
        notes.add(self.conn, "second")
        self.assertEqual(notes.recent(self.conn), ["second", "first"])

    def test_blank_note_is_rejected(self):
        with self.assertRaises(ValueError):
            notes.add(self.conn, "  ")


class DeployGateTests(unittest.TestCase):
    def test_preview_is_default(self):
        result = run_deploy()
        self.assertEqual(result.returncode, 0)
        self.assertIn("preview release-", result.stdout)

    def test_publish_refuses_without_target(self):
        self.assertEqual(run_deploy("publish").returncode, 1)

    def test_unknown_mode_is_rejected(self):
        self.assertEqual(run_deploy("yes").returncode, 2)

    def test_publish_writes_release_once(self):
        with tempfile.TemporaryDirectory() as target:
            self.assertEqual(run_deploy("publish", target=target).returncode, 0)
            release = next(Path(target).iterdir())
            self.assertTrue((release / "MANIFEST").read_text())
            self.assertTrue((release / "notes.py").exists())
            self.assertEqual(run_deploy("publish", target=target).returncode, 1)


if __name__ == "__main__":
    unittest.main()
