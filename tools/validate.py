#!/usr/bin/env python3
"""Check the public command contract in a justfile and its modules."""

import argparse
import json
import subprocess
import sys
from pathlib import Path


VALUES = {
    "effect": {"read", "local", "external", "publish"},
    "cost": {"free", "metered"},
    "duration": {"short", "long"},
}


def validate(path, selected=None):
    result = subprocess.run(
        ["just", "--justfile", str(path), "--dump", "--dump-format", "json"],
        capture_output=True,
        text=True,
    )
    if result.returncode:
        return [result.stderr.strip() or "just could not read the justfile"]

    root = json.loads(result.stdout)
    recipes = {}
    errors = []

    def collect(module, prefix=""):
        for name, recipe in module["recipes"].items():
            recipes[prefix + name] = recipe
        for name, child in module["modules"].items():
            module_name = prefix + name
            if not child.get("doc") and (selected is None or any(
                item.startswith(module_name + "::") for item in selected
            )):
                errors.append(f"{module_name}: module needs a description")
            collect(child, module_name + "::")

    collect(root)
    if selected is not None:
        for name in selected - recipes.keys():
            errors.append(f"{name}: selected recipe does not exist")
        for name in selected & recipes.keys():
            if recipes[name]["private"]:
                errors.append(f"{name}: selected recipe is private")

    for name, recipe in recipes.items():
        if recipe["private"] or (selected is not None and name not in selected):
            continue
        if not recipe.get("doc"):
            errors.append(f"{name}: recipe needs a description")

        tags = {}
        for attribute in recipe["attributes"]:
            for item in attribute.get("metadata", []):
                key, separator, value = item.partition(":")
                if not separator or not value:
                    errors.append(f"{name}: invalid metadata {item!r}")
                elif key in tags:
                    errors.append(f"{name}: duplicate metadata key {key!r}")
                else:
                    tags[key] = value

        for key, allowed in VALUES.items():
            if tags.get(key) not in allowed:
                errors.append(f"{name}: {key} must be one of {', '.join(sorted(allowed))}")

        if tags.get("effect") == "publish" and not tags.get("gate"):
            errors.append(f"{name}: publish recipe needs gate: metadata")
        if "verify" in tags:
            target = tags["verify"]
            if "::" not in target and "::" in name:
                target = name.rsplit("::", 1)[0] + "::" + target
            if target not in recipes or recipes[target]["private"] or target == name:
                errors.append(f"{name}: verify target {tags['verify']!r} is not a public recipe")

    return errors


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path, help="path to a justfile")
    parser.add_argument("--recipe", action="append", help="validate only this public recipe (repeatable)")
    args = parser.parse_args()
    try:
        problems = validate(args.path.resolve(), set(args.recipe) if args.recipe else None)
    except FileNotFoundError as error:
        sys.exit(f"missing tool: {error.filename}")
    for problem in problems:
        print(problem, file=sys.stderr)
    if problems:
        sys.exit(1)
    print("command contract: OK")
