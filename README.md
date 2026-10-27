# JustHarness

A small, vendor-neutral convention for exposing workspace tasks to people and shell-capable agents through [`just`](https://just.systems/).

**Status:** planning. The [implementation plan](PLAN.md) records the design, scope, milestones, and acceptance checks. No harness or validator has been implemented yet.

The goal is a simple command interface that agents can discover and run, and people can inspect and run. Nested justfiles reveal related commands on demand; optional skills explain when to use them. The same commands should work in CI.

## Problems to solve

- Agents repeatedly reconstruct project commands from scattered scripts and prose, sometimes choosing the wrong target or environment.
- A human reviewing an agent's work cannot easily tell what a command changes, how long it runs, or what result proves success.
- The agent, maintainer, and CI can end up using different paths for the same task, so checks and release steps drift.
- Useful lessons stay in one conversation instead of becoming a better command, description, check, or skill.

## How someone would use it

In an existing workspace, the maintainer keeps the scripts that already work and exposes repeated operations as documented `just` recipes. Bare `just` is the entry point; coherent areas can have modules, with `just --list <module>` revealing their commands. `AGENTS.md` tells an agent to use that interface, and an optional `SKILL.md` explains decisions that need more than a command description. The agent runs a recipe and reports its check or artifact. A person can run the same recipe and review any proposed improvement as a normal Git diff.

The first release needs a short specification, a runnable example, and an adoption guide that works with an existing repo. This repository is currently the plan for that release.

This idea grew from a [shared research conversation](https://mammouth.ai/shared/588f41bd-935c-40db-808a-e90f93638878). The plan includes an independent assessment of that proposal.

Licensed under [MIT](LICENSE).
