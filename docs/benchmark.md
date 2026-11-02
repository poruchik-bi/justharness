# A/B benchmark: does the catalog help a fresh agent?

`just bench` gives one task to fresh headless Claude Code sessions on [pallets/itsdangerous](https://github.com/pallets/itsdangerous) at a pinned commit: *run the tests and the type checks, report whether each passes and the commands used*. Baseline runs see the repository as published. Harness runs also get the [overlay](../bench/itsdangerous/): a four-recipe justfile that wraps CI's own `uv run --locked tox run -e …` path, plus `AGENTS.md`. The task has a real trap: the tox env list names five interpreters, so a plain `tox` fails where only some are installed.

Runs alternate baseline and harness so a warm uv cache favours neither. Each records turns, Bash commands, tool errors, tokens, cost, and wall time in `runs/ab/<timestamp>/results.md`; the raw stream of each run is kept beside it. Correctness is judged by reading the answers: did the agent run both checks, and does its pass or fail claim match the commands' output?

```sh
just bench               # 3 runs per variant with claude-sonnet-5-5, capped at $2 per run
just bench 5 claude-opus-5-5
```

The runs are metered and execute the target repository's tests on this machine. They use `--setting-sources project` and `--strict-mcp-config` to keep personal hooks, plugins, and MCP servers out; `--setting-sources` alone still loads user-scope MCP servers. Before trusting a run, confirm that personal instructions do not leak in: ask one isolated session whether its context mentions a word that appears only in your `~/.claude/CLAUDE.md`.

Publish a result only with its sample size, model, commit, and date. Three runs per variant is a pilot, not proof; one repository says nothing about others. A null or negative result is worth publishing too.

## Pilot result, 2026-11-02

Five runs per variant, `claude-sonnet-5-5` (Claude Code 2.1.316), itsdangerous at `672971d`, run with the isolation above. Medians unless noted.

| | Baseline | With catalog |
|---|---|---|
| Reported a correct pass/fail | 5/5 | 5/5 |
| Ran CI's full typing job, including `pyright --verifytypes` | 2/5 | 5/5 |
| Turns | 4 | 3 |
| Bash commands | 3 | 2 |
| Runs with a failed command | 4/5 | 0/5 |
| Input tokens | 70.3k | 36.3k |
| Mean cost | $0.049 | $0.043 |
| Wall time | 13 s | 14 s |

Every agent got the right answer; none fell into the `tox` interpreter trap. Without the catalog, three of five agents left out one of CI's three typing commands and still reported the type checks as passing, and four of five spent a command probing for tools (`which uv tox`) that failed. With the catalog, every agent ran exactly what CI runs, in two commands, using about half the input tokens; cost fell only 13% because most input tokens are cached. Wall time did not change. This is one repository, one model, and a short task: a pilot.
