---
name: justharness-adopt
description: Retrofit a repository with a JustHarness command catalog — a justfile whose recipes wrap the project's existing scripts and declare their effect, cost, duration and check — and leave it as a reviewable diff. Use when the user asks to adopt JustHarness, make a repository agent-operable, add a justfile for agents, or reduce permission prompts for routine project commands.
---

# Adopt JustHarness

The goal is a small diff a maintainer can review: a fresh agent runs `just`, finds the right command, runs it, and reports its check. Wrap what already works; do not rewrite it. The contract is at https://github.com/poruchik-bi/justharness/blob/main/SPEC.md.

## Steps

1. **Get the tools.** Run `git ls-remote --tags https://github.com/poruchik-bi/justharness` and shallow-clone the newest release tag into a temporary directory outside the target repository. Use its `tools/validate.py` and `tools/allowlist.py`. Check `just --version` is 1.42 or newer; if `just` is missing, stop and tell the person to install it from https://just.systems/man/en/installation.html.
2. **Inventory, read-only.** Read the existing `justfile`, `Makefile`, `package.json` scripts, CI workflows, README commands, and `AGENTS.md` or `CLAUDE.md`. List the commands people actually run: test, lint, build, run, migrate, release. Run nothing yet.
3. **Pick three to seven tasks.** Prefer the ones CI runs and the ones the README tells people to run. Each recipe calls the existing command; keep its name if one exists. If a justfile already exists, add metadata in place rather than restructuring, and validate only the adopted recipes with `--recipe NAME`.
4. **Declare each recipe.** One-line doc comment saying what it does and what it produces, then `[metadata(...)]`:
   - `effect:read` only if it leaves the working tree alone. Tests that write caches or coverage files are `local` unless the recipe disables those writes.
   - `effect:local` for builds, formatters that rewrite files, local databases and containers.
   - `effect:external` for anything that calls a network service; `effect:publish` for deploys, releases, package uploads and messages to people.
   - `cost:metered` if a normal run can be billed: paid APIs, cloud jobs, LLM calls.
   - `duration:long` for anything over about a minute. Add `verify:NAME` when another recipe checks the result.
5. **Gate publishing.** A `publish` recipe defaults to a preview and needs an explicit argument or variable to publish, declared in `gate:`. Never run a publish, external or metered recipe during adoption; run its preview at most.
6. **Add `doctor` and `check`.** `doctor` checks prerequisites that commonly fail and names the repair in each failure. `check` is the fast local verifier, the same one CI runs. Put `help` first so bare `just` lists the catalog.
7. **Tell agents.** Add a short section to `AGENTS.md`: run `just`, inspect a module with `just --list NAME`, run the recipe, then its check.
8. **Verify.** Run `just --unstable --fmt --check`, the validator against the justfile, `just doctor`, and `just check`. Run each new `read` recipe once. Fix what fails; do not weaken a check to pass.
9. **Offer the allowlist.** Print `python3 tools/allowlist.py justfile`. It allows `read` + `free` recipes and asks before `external`, `publish` and `metered` ones. Show it to the person and merge it into `.claude/settings.json` only if they approve.

## Report

Return the diff summary, each recipe with its effect, the `just check` result, and anything skipped with the reason. Do not commit or push unless the person asks.
