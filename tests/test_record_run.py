import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools.record_run import record


class RecordRunTests(unittest.TestCase):
    def test_success_and_verification_are_recorded(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            justfile = root / "justfile"
            justfile.write_text(
                "# Create an artifact.\n"
                "[metadata('effect:local', 'cost:free', 'duration:short', 'verify:verify')]\n"
                "build:\n    @touch result.txt\n\n"
                "# Check the artifact.\n"
                "[metadata('effect:read', 'cost:free', 'duration:short')]\n"
                "verify:\n    @test -f result.txt\n"
            )
            ledger = root / "runs"
            self.assertEqual(record(justfile, "build", ["source.txt"], ["result.txt"], ledger), 0)
            entry = json.loads(next(ledger.iterdir()).read_text())
            self.assertEqual(entry["effect"], "local")
            self.assertEqual(entry["inputs"], ["source.txt"])
            self.assertEqual(entry["outputs"], ["result.txt"])
            self.assertEqual(entry["exit_code"], 0)
            self.assertEqual(entry["verification"], {"recipe": "verify", "exit_code": 0})

    def test_failure_is_recorded(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            justfile = root / "justfile"
            justfile.write_text(
                "# Fail deliberately.\n"
                "[metadata('effect:read', 'cost:free', 'duration:short')]\n"
                "fail:\n    @exit 7\n"
            )
            ledger = root / "runs"
            with patch("tools.record_run.run", return_value=7):
                self.assertEqual(record(justfile, "fail", [], [], ledger), 7)
            entry = json.loads(next(ledger.iterdir()).read_text())
            self.assertEqual(entry["exit_code"], 7)
            self.assertIsNone(entry["verification"])
