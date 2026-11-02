#!/usr/bin/env python3
"""Print Claude Code permission rules derived from a justfile's recipe metadata.

Recipes declared effect:read and cost:free become allow rules. Recipes declared
external, publish, or metered become ask rules. Everything else, including local
and undeclared recipes, gets no rule and keeps the agent's default prompt. Review
the output before merging it into .claude/settings.json; metadata is a claim the
repository owner makes, and this tool does not inspect recipe bodies.
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path


def recipes(module, path=()):
    for name, recipe in module["recipes"].items():
        if not recipe["private"]:
            yield path + (name,), recipe
    for name, child in module["modules"].items():
        yield from recipes(child, path + (name,))


def tags(recipe):
    items = []
    for attribute in recipe["attributes"]:
        if isinstance(attribute, dict):
            items += attribute.get("metadata", [])
    return dict(item.partition(":")[::2] for item in items)


def rules(justfile):
    result = subprocess.run(
        ["just", "--justfile", str(justfile), "--dump", "--dump-format", "json"],
        capture_output=True,
        text=True,
        check=True,
    )
    allow, ask = ["Bash(just)", "Bash(just --list *)"], []
    for path, recipe in recipes(json.loads(result.stdout)):
        # A trailing " *" matches arguments at a word boundary, so `just test *` never matches `just tests`.
        command = "just " + " ".join(path) + (" *" if recipe["parameters"] else "")
        tag = tags(recipe)
        if tag.get("effect") == "read" and tag.get("cost") == "free":
            allow.append(f"Bash({command})")
        elif tag.get("effect") in {"external", "publish"} or tag.get("cost") == "metered":
            ask.append(f"Bash({command})")
    return {"permissions": {"allow": allow, "ask": ask}}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("path", type=Path, help="path to a justfile")
    args = parser.parse_args()
    try:
        print(json.dumps(rules(args.path.resolve()), indent=2))
    except FileNotFoundError as error:
        sys.exit(f"missing tool: {error.filename}")
    except subprocess.CalledProcessError as error:
        sys.exit(error.stderr.strip() or "just could not read the justfile")
