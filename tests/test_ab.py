import json
import unittest

from bench.ab import summarize


STREAM = [
    {"type": "assistant", "message": {"content": [{"type": "tool_use", "name": "Bash", "input": {"command": "tox"}}]}},
    {"type": "user", "message": {"content": [{"type": "tool_result", "is_error": True, "content": "py3.13: InterpreterNotFound"}]}},
    {"type": "assistant", "message": {"content": [{"type": "tool_use", "name": "Read", "input": {"file_path": "AGENTS.md"}}]}},
    {"type": "user", "message": {"content": "plain text content"}},
    {"type": "result", "num_turns": 4, "total_cost_usd": 0.12, "duration_ms": 61500, "result": "tests pass",
     "usage": {"input_tokens": 10, "cache_read_input_tokens": 90, "output_tokens": 7}},
]


class SummarizeTests(unittest.TestCase):
    def test_counts_bash_errors_and_usage(self):
        summary = summarize(json.dumps(event) for event in STREAM)
        self.assertEqual(summary["bash_commands"], ["tox"])
        self.assertEqual(summary["tool_errors"], 1)
        self.assertEqual(summary["input_tokens"], 100)
        self.assertEqual((summary["turns"], summary["seconds"], summary["answer"]), (4, 62, "tests pass"))


if __name__ == "__main__":
    unittest.main()
