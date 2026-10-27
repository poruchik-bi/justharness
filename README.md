# JustHarness

A small, vendor-neutral convention for exposing workspace tasks to people and shell-capable agents through [`just`](https://just.systems/).

**Status:** planning. The [implementation plan](PLAN.md) records the design, scope, milestones, and acceptance checks. No harness or validator has been implemented yet.

The goal is a simple command interface that agents can discover and run, and people can inspect and run. Nested justfiles reveal related commands on demand; optional skills explain when to use them. The same commands should work in CI.

This idea grew from a [shared research conversation](https://mammouth.ai/shared/588f41bd-935c-40db-808a-e90f93638878). The plan includes an independent assessment of that proposal.

Licensed under [MIT](LICENSE).
