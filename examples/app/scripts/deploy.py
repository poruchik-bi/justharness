#!/usr/bin/env python3
"""Preview or publish the release bundle; publishing needs mode=publish and APP_DEPLOY_DIR."""

import hashlib
import os
import shutil
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def bundle():
    return [ROOT / "notes.py", *sorted((ROOT / "migrations").glob("*.sql"))]


def manifest(files):
    return "".join(f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.relative_to(ROOT)}\n" for path in files)


def deploy(mode, target_root):
    files = bundle()
    text = manifest(files)
    release = "release-" + hashlib.sha256(text.encode()).hexdigest()[:12]
    if mode == "preview":
        print(f"preview {release}: would publish\n{text}gate: run `just release deploy publish` with APP_DEPLOY_DIR set")
        return 0
    if mode != "publish":
        print(f"FAIL unknown mode {mode!r} → use preview or publish", file=sys.stderr)
        return 2
    # ponytail: a local directory stands in for the real host; swap this copy for the project's own upload.
    if not target_root or not Path(target_root).is_dir():
        print("FAIL APP_DEPLOY_DIR unset or not a directory → set it to the release target", file=sys.stderr)
        return 1
    target = Path(target_root) / release
    if target.exists():
        print(f"FAIL {release} already published → change the bundle or keep the existing release", file=sys.stderr)
        return 1
    target.mkdir()
    for path in files:
        destination = target / path.relative_to(ROOT)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, destination)
    (target / "MANIFEST").write_text(text)
    print(f"published {release} → {target}")
    return 0


if __name__ == "__main__":
    sys.exit(deploy(sys.argv[1] if len(sys.argv) > 1 else "preview", os.environ.get("APP_DEPLOY_DIR")))
