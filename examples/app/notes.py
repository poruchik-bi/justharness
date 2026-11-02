#!/usr/bin/env python3
"""Store short notes in SQLite and manage the schema migrations."""

import sqlite3
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
MIGRATIONS = ROOT / "migrations"
DATABASE = ROOT / "out" / "app.db"


def pending(conn):
    conn.execute("CREATE TABLE IF NOT EXISTS schema_migrations (name TEXT PRIMARY KEY)")
    applied = {row[0] for row in conn.execute("SELECT name FROM schema_migrations")}
    return [path for path in sorted(MIGRATIONS.glob("*.sql")) if path.name not in applied]


def migrate(conn):
    names = []
    for path in pending(conn):
        with conn:
            conn.executescript(path.read_text())
            conn.execute("INSERT INTO schema_migrations VALUES (?)", (path.name,))
        names.append(path.name)
    return names


def add(conn, body):
    body = body.strip()
    if not body:
        raise ValueError("a note needs text")
    with conn:
        conn.execute("INSERT INTO notes (body) VALUES (?)", (body,))


def recent(conn, limit=10):
    return [row[0] for row in conn.execute("SELECT body FROM notes ORDER BY id DESC LIMIT ?", (limit,))]


if __name__ == "__main__":
    command = sys.argv[1] if len(sys.argv) == 2 else ""
    if command not in {"migrate", "status"}:
        sys.exit("usage: notes.py migrate|status")
    if command == "status" and not DATABASE.exists():
        sys.exit(f"FAIL {DATABASE.relative_to(ROOT)} missing → run: just db migrate")
    DATABASE.parent.mkdir(exist_ok=True)
    conn = sqlite3.connect(DATABASE)
    if command == "migrate":
        names = migrate(conn)
        print(f"applied: {', '.join(names) or 'nothing pending'}")
    else:
        names = [path.name for path in pending(conn)]
        if names:
            sys.exit(f"FAIL pending migrations: {', '.join(names)} → run: just db migrate")
        print("schema: up to date")
