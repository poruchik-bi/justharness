#!/usr/bin/env python3
"""Build or check an editorial review sheet from fixture posts."""

import json
import sys
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "out" / "review.md"


def posts():
    records = json.loads((ROOT / "posts.json").read_text())
    ids = set()
    if not isinstance(records, list) or not records:
        raise ValueError("posts.json needs a nonempty list of records")
    for post in records:
        if not isinstance(post, dict) or not all(
            isinstance(post.get(key), str) and post[key].strip()
            for key in ("id", "title", "source", "summary")
        ) or not isinstance(post.get("claims"), list) or not post["claims"] or not all(
            isinstance(claim, str) and claim.strip() for claim in post["claims"]
        ):
            raise ValueError("each post needs id, title, HTTPS source, summary, and nonempty claims")
        source = urlparse(post["source"])
        if post["id"] in ids or source.scheme != "https" or not source.netloc:
            raise ValueError(f"duplicate id or invalid HTTPS source: {post['id']}")
        ids.add(post["id"])
    return records


def render(records):
    lines = ["# Content review sheet", "", "Claims below are source statements awaiting review.", ""]
    for post in records:
        lines += [
            f"## {post['id']}: {post['title']}",
            "",
            f"Source: {post['source']}",
            "",
            post["summary"],
            "",
            "Claims to check:",
            *[f"- {claim}" for claim in post["claims"]],
            "",
            "Review: pending",
            "",
        ]
    return "\n".join(lines)


def main():
    if len(sys.argv) != 2 or sys.argv[1] not in ("build", "verify"):
        raise ValueError("usage: review.py build|verify")
    expected = render(posts())
    if sys.argv[1] == "build":
        OUTPUT.parent.mkdir(exist_ok=True)
        OUTPUT.write_text(expected)
        print(f"wrote {OUTPUT}")
    elif not OUTPUT.exists() or OUTPUT.read_text() != expected:
        raise ValueError("review sheet missing or stale → run: just content build")
    else:
        print(f"verified {OUTPUT}")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError) as error:
        sys.exit(f"FAIL {error}")
