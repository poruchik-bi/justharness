# A/B benchmark: does the catalog help a fresh agent?

`just bench` gives one task to fresh headless Claude Code sessions on [pallets/itsdangerous](https://github.com/pallets/itsdangerous) at a pinned commit: *run the tests and the type checks, report whether each passes and the commands used*. Baseline runs see the repository as published. Harness runs also get the [overlay](../bench/itsdangerous/): a four-recipe justfile that wraps CI's own `uv run --locked tox run -e …` path, plus `AGENTS.md`. The task has a real trap: the tox env list names five interpreters, so a plain `tox` fails where only some are installed.

Runs alternate baseline and harness so a warm uv cache favours neither. Each records turns, Bash commands, tool errors, tokens, cost, and wall time in `runs/ab/<timestamp>/results.md`; the raw stream of each run is kept beside it. Correctness is judged by reading the answers: did the agent run both checks, and does its pass or fail claim match the commands' output?

```sh
just bench               # 3 runs per variant with claude-sonnet-5-5, capped at $2 per run
just bench 5 claude-opus-5-5
```

The runs are metered and execute the target repository's tests on this machine. They use `--setting-sources project` to keep personal hooks and plugins out. Before trusting a run, confirm that personal instructions do not leak in: ask one isolated session whether its context mentions a word that appears only in your `~/.claude/CLAUDE.md`.

Publish a result only with its sample size, model, commit, and date. Three runs per variant is a pilot, not proof; one repository says nothing about others. A null or negative result is worth publishing too.
