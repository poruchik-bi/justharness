# JustHarness

A small, vendor-neutral convention for exposing workspace tasks to people and shell-capable agents through [`just`](https://just.systems/).

**Status:** v0.1 examples and checks implemented; an existing-project pilot and release tag remain open. The [implementation plan](PLAN.md) records the remaining acceptance work.

The goal is a simple command interface that agents can discover and run, and people can inspect and run. Modules reveal related commands on demand; optional skills explain when to use them. The same commands should work in CI.

## Try it

Install [`just` 1.42 or newer](https://just.systems/man/en/installation.html), Python 3, and Git. From this repository:

```sh
just                    # discover commands
just check              # check the command contract and both examples
just --justfile examples/minimal/justfile --list work
just --justfile examples/content/justfile content build
just --justfile examples/content/justfile content verify
```

The content example writes a review sheet to `examples/content/out/review.md`. See the one-page [command contract](SPEC.md), [adoption guide](docs/adoption.md), and [optional run ledger](docs/ledger.md). `AGENTS.md` gives agents the same entry point.

## Problems to solve

- Agents repeatedly reconstruct project commands from scattered scripts and prose, sometimes choosing the wrong target or environment.
- A human reviewing an agent's work cannot easily tell what a command changes, how long it runs, or what result proves success.
- The agent, maintainer, and CI can end up using different paths for the same task, so checks and release steps drift.
- Useful lessons stay in one conversation instead of becoming a better command, description, check, or skill.

## How someone would use it

In an existing workspace, the maintainer keeps the scripts that already work and exposes repeated operations as documented `just` recipes. Bare `just` is the entry point; coherent areas can have modules, with `just --list <module>` revealing their commands. `AGENTS.md` tells an agent to use that interface, and an optional `SKILL.md` explains decisions that need more than a command description. The agent runs a recipe and reports its check or artifact. A person can run the same recipe and review any proposed improvement as a normal Git diff.

The first release also needs a pilot in an existing repo to test whether this interface improves real work. The examples establish mechanics; they do not measure adoption value yet. The same `just check` runs in GitHub Actions.

## Usage scenarios to prove

1. **Retrofit an existing project.** An agent is asked to make a repository easier to operate. It inventories the current scripts, justfile, CI, and agent instructions; keeps working commands intact; fixes missing descriptions and unsafe or unclear entry points; and leaves a small diff. A fresh agent should then find and verify one real task without reconstructing it from source code.
2. **Build a new domain harness.** A team starts a market-research workspace using search data and CRM exports. Small scripts handle each source's authentication and errors; recipes expose fetch, review, and report steps; a skill explains evidence quality and when a claim is ready to use. The output includes source, date, and method, so a reviewer can trace a report back to its inputs.
3. **Use a harness during ordinary work.** From a terminal or a phone client, a person asks an agent to produce a report or render a clip. The agent finds the relevant recipe, follows its skill if needed, runs it, inspects the resulting artifact, and returns the artifact and check result. The person can review or repeat the same operation.
4. **Improve after a real failure.** A repeated task fails because a prerequisite is missing or a command's effect is unclear. The agent proposes a clearer description, a preflight check, or a better recipe, then runs the local checks. A person reviews the diff before the change becomes the next agent's default path.

These cover creation, daily use, and improvement. A phone app such as Cookbox is a way to reach the workspace in scenario 3; the project commands stay in the workspace.

This idea grew from a [shared research conversation](https://mammouth.ai/shared/588f41bd-935c-40db-808a-e90f93638878). The plan includes an independent assessment of that proposal.

Licensed under [MIT](LICENSE).
