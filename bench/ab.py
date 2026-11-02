#!/usr/bin/env python3
"""Run one task with fresh headless Claude Code sessions, with and without a JustHarness overlay.

Each run gets its own clone at a pinned commit. Baseline and harness runs alternate
so a warm package cache favours neither. The raw stream of every run is kept next
to results.json and results.md; correctness is left to a human reading the answers.
"""

import argparse
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path


def summarize(lines):
    commands, errors, result = [], 0, {}
    for line in lines:
        event = json.loads(line)
        content = event.get("message", {}).get("content", [])
        for block in content if isinstance(content, list) else []:
            if block.get("type") == "tool_use" and block.get("name") == "Bash":
                commands.append(block["input"].get("command", ""))
            elif block.get("type") == "tool_result" and block.get("is_error"):
                errors += 1
        if event.get("type") == "result":
            result = event
    usage = result.get("usage", {})
    return {
        "turns": result.get("num_turns"),
        "cost_usd": result.get("total_cost_usd"),
        "seconds": round(result.get("duration_ms", 0) / 1000),
        "input_tokens": sum(usage.get(key, 0) for key in ("input_tokens", "cache_read_input_tokens", "cache_creation_input_tokens")),
        "output_tokens": usage.get("output_tokens", 0),
        "bash_commands": commands,
        "tool_errors": errors,
        "answer": result.get("result", ""),
    }


def run(args, variant, index, source):
    work = args.out / f"{variant}-{index}"
    subprocess.run(["git", "clone", "-q", str(source), str(work / "repo")], check=True)
    if variant == "harness":
        shutil.copytree(args.overlay, work / "repo", dirs_exist_ok=True)
    command = [
        "claude", "-p", args.task,
        "--model", args.model,
        "--output-format", "stream-json", "--verbose",
        "--setting-sources", "project",
        "--no-session-persistence",
        "--allowedTools", "Bash", "Read", "Grep", "Glob",
        "--disallowedTools", "Edit", "Write", "Bash(sudo *)", "Bash(pip install *)",
        "--max-budget-usd", str(args.budget),
    ]
    started = time.time()
    try:
        output = subprocess.run(command, cwd=work / "repo", capture_output=True, text=True, timeout=args.timeout).stdout
    except subprocess.TimeoutExpired as error:
        output = error.stdout.decode() if isinstance(error.stdout, bytes) else (error.stdout or "")
    (work / "stream.jsonl").write_text(output)
    shutil.rmtree(work / "repo")
    summary = summarize(line for line in output.splitlines() if line.startswith("{"))
    summary.update(variant=variant, run=index, wall_seconds=round(time.time() - started))
    return summary


def table(results):
    lines = ["| variant | run | turns | bash | tool errors | tokens in/out | cost USD | seconds |", "|---|---|---|---|---|---|---|---|"]
    for item in results:
        lines.append(
            f"| {item['variant']} | {item['run']} | {item['turns']} | {len(item['bash_commands'])} | {item['tool_errors']} "
            f"| {item['input_tokens']}/{item['output_tokens']} | {item['cost_usd']} | {item['wall_seconds']} |"
        )
    for item in results:
        lines += ["", f"### {item['variant']} {item['run']}", "", "Commands: " + "; ".join(f"`{c}`" for c in item["bash_commands"]), "", item["answer"]]
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--repo", default="https://github.com/pallets/itsdangerous")
    parser.add_argument("--commit", default="672971d66a2ef9f85151e53283113f33d642dabd")
    parser.add_argument("--overlay", type=Path, default=here / "itsdangerous")
    parser.add_argument("--task", default="Run this project's tests and its type checks, then report whether each passes and the exact commands you used.")
    parser.add_argument("--model", default="claude-sonnet-5-5")
    parser.add_argument("--runs", type=int, default=3)
    parser.add_argument("--budget", type=float, default=2.0, help="per-run spending cap in USD")
    parser.add_argument("--timeout", type=int, default=900, help="per-run timeout in seconds")
    parser.add_argument("--out", type=Path, default=here.parent / "runs" / "ab")
    args = parser.parse_args()
    if shutil.which("claude") is None:
        sys.exit("missing tool: claude")
    args.out = args.out / time.strftime("%Y%m%d-%H%M%S")
    source = args.out / "source"
    subprocess.run(["git", "clone", "-q", args.repo, str(source)], check=True)
    subprocess.run(["git", "-C", str(source), "checkout", "-q", args.commit], check=True)
    results = [run(args, variant, index, source) for index in range(1, args.runs + 1) for variant in ("baseline", "harness")]
    (args.out / "results.json").write_text(json.dumps({"args": {k: str(v) for k, v in vars(args).items()}, "results": results}, indent=2))
    (args.out / "results.md").write_text(table(results))
    print(table(results).split("\n\n###")[0])
    print(f"full answers: {args.out / 'results.md'}")
