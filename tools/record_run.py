#!/usr/bin/env python3
"""Optionally run a parameter-free just recipe and record its outcome."""

import argparse
import json
import subprocess
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path


def recipe_info(justfile, name):
    dump = subprocess.run(
        ["just", "--justfile", str(justfile), "--dump", "--dump-format", "json"],
        check=True, capture_output=True, text=True,
    )
    parts = name.split("::")
    node = json.loads(dump.stdout)
    for part in parts[:-1]:
        node = node["modules"][part]
    recipe = node["recipes"][parts[-1]]
    if recipe["private"]:
        raise ValueError("the recorded recipe must be public")
    tags = {}
    for attribute in recipe["attributes"]:
        for item in attribute.get("metadata", []):
            key, _, value = item.partition(":")
            tags[key] = value
    return tags


def run(justfile, name):
    return subprocess.run(["just", "--justfile", str(justfile), *name.split("::")]).returncode


def record(justfile, name, inputs, outputs, ledger):
    tags = recipe_info(justfile, name)
    if tags.get("effect") not in ("read", "local", "external", "publish"):
        raise ValueError("recipe needs valid effect metadata")
    verify = tags.get("verify")
    if verify and "::" not in verify and "::" in name:
        verify = name.rsplit("::", 1)[0] + "::" + verify

    source = subprocess.run(
        ["git", "-C", str(justfile.parent), "rev-parse", "HEAD"],
        capture_output=True, text=True,
    )
    started = datetime.now(timezone.utc).isoformat()
    clock = time.monotonic()
    exit_code = run(justfile, name)
    verification = run(justfile, verify) if exit_code == 0 and verify else None
    entry = {
        "recipe": name,
        "source_revision": source.stdout.strip() if source.returncode == 0 else None,
        "started_at": started,
        "duration_seconds": round(time.monotonic() - clock, 3),
        "effect": tags["effect"],
        "inputs": inputs,
        "outputs": outputs,
        "exit_code": exit_code,
        "verification": {"recipe": verify, "exit_code": verification} if verify else None,
    }
    ledger.mkdir(parents=True, exist_ok=True)
    path = ledger / f"{datetime.now(timezone.utc):%Y%m%dT%H%M%S}-{uuid.uuid4().hex[:8]}.json"
    path.write_text(json.dumps(entry, indent=2) + "\n")
    print(f"run record: {path}")
    return exit_code or (verification or 0)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--justfile", type=Path, required=True)
    parser.add_argument("--recipe", required=True, help="public recipe name, e.g. content::build")
    parser.add_argument("--input", action="append", default=[], help="non-secret input path")
    parser.add_argument("--output", action="append", default=[], help="non-secret output path")
    parser.add_argument("--ledger", type=Path, default=Path("runs"))
    args = parser.parse_args()
    try:
        return record(args.justfile.resolve(), args.recipe, args.input, args.output, args.ledger)
    except (KeyError, ValueError, OSError, subprocess.CalledProcessError) as error:
        parser.exit(2, f"run record failed: {error}\n")


if __name__ == "__main__":
    sys.exit(main())
