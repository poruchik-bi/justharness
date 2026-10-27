# JustHarness implementation plan

## Assessment of the source proposal

The [source conversation](https://mammouth.ai/shared/588f41bd-935c-40db-808a-e90f93638878) proposes a domain-neutral agent harness made from nested justfiles, skills, a validator, domain packs, and a review step for self-improvement. The valuable core is **discovery → documented command → verifiable result**. This is practical because `just` already supports [documented recipes](https://just.systems/man/en/documentation-comments.html), [modules](https://just.systems/man/en/modules.html), and [module-specific listing](https://just.systems/man/en/listing-available-recipes.html). The [Agent Skills format](https://github.com/agentskills/agentskills/blob/main/docs/specification.mdx) already covers optional, progressively loaded instructions.

My changes to the proposal:

1. **Start with a working example, then write the rules it proves.** Ten mandatory rules, compliance levels, badges, a linter, and six domain packs would make a convention harder to adopt before its basic workflow has been tested.
2. **Do not claim a new MCP bridge.** Projects such as [toolprint/just-mcp](https://github.com/toolprint/just-mcp) already expose recipes as MCP tools. JustHarness should stay a shell-accessible workspace convention; a bridge can be documented later if a real client needs one.
3. **Treat safety as execution policy, not a label.** A `safe` or `destructive` comment does not restrict shell access. Examples should contain no destructive command; any later mutating recipe needs input validation, a clear target, and a real confirmation or external approval mechanism.
4. **Use `just`'s working-directory behavior.** Recipes normally run from their justfile's directory, and module recipes run from the module directory. Use `justfile_directory()` when a recipe needs the repository root; do not force absolute paths into every command. See the [working-directory documentation](https://just.systems/man/en/working-directory.html).
5. **Make skills optional and purposeful.** A one-step recipe needs a good description. Add a `SKILL.md` only for decisions or multi-step work that a recipe cannot explain. Keep command logic in `just` or its scripts.
6. **Measure claims.** Nested catalogs should be demonstrated with a real task and output. Do not promise token savings or broad domain coverage until examples and comparisons support them.

The project should not add an agent runtime, LLM client, hosted service, automatic tool generation, or a replacement for MCP. APIs and MCP remain useful for remote services, authentication, and clients without shell access.

## v0.1 target

A user can copy a small example into an existing workspace, run bare `just` to discover commands, inspect one module, run a read-only command, and use the same command in CI. An agent can follow `AGENTS.md` to discover and verify commands without learning a framework. The entire example must run locally with documented prerequisites and no secrets.

Proposed v0.1 layout:

```text
README.md
SPEC.md                         # short rules, derived from the working example
examples/minimal/justfile
examples/minimal/work/mod.just
examples/minimal/AGENTS.md
examples/minimal/skills/.../SKILL.md   # only if the example needs a workflow
```

Use `just` 1.31 or newer as the initial compatibility target: modules were stabilized in that release. Put a `help` recipe first so bare `just` works without the newer `default-list` setting. Recheck the minimum version against every feature actually used before release.

## Steps

### 1. Build and run the minimal example

- Add a root `justfile` with a first `help` recipe that prints `just --list`, plus one documented module.
- Add two real, harmless recipes in the module: one that inspects workspace state and one that checks an example artifact. Use existing system tools and meaningful exit codes; no placeholder `echo` commands presented as capabilities.
- Check `just`, `just --list work`, each recipe, and invocation from a nested directory.

**Done when:** a new user can discover and execute the example using only the README and `just` output.

### 2. Write the one-page convention

- Explain the three layers: root catalog, module recipes, and optional skills.
- Require a useful one-line description for public recipes; document inputs, output, failure behavior, prerequisites, and side effects where they matter.
- State that recipes are ordinary shell commands, not a sandbox or permission system. Keep repository-relative paths correct and secrets out of arguments and output.
- Document how a user adopts one module without restructuring an entire project.

**Done when:** every rule maps to something in the example or an observed failure. Delete rules that cannot be demonstrated.

### 3. Add the agent entry point and one optional skill

- Add `AGENTS.md` with a short sequence: run `just`, inspect the relevant module, read the relevant skill if one exists, execute, then run checks.
- Add one skill only if it captures a real decision or multi-step procedure. It should point to recipes, not duplicate command bodies.
- Test the instructions with a fresh agent session or a person who has not read the implementation notes.

**Done when:** the user reaches the right command and understands its effects without reading every justfile.

### 4. Add only the validation the example needs

- Start with `just --fmt --check`, `just --list`, and a smoke check for the example. Add a custom checker only if these leave a concrete recurring failure, such as missing public descriptions or broken skill references.
- If a checker is needed, read `just --dump --dump-format json` instead of parsing justfile syntax with regular expressions. Keep one fixture for each failure it catches.
- Run the same checks locally and in CI.

**Done when:** an intentionally broken example fails the check, and a clean example passes. There is one canonical check command.

### 5. Prove one non-software use case

- Add one small, runnable example from content creation or 3D work. Pick the case with the fewest external prerequisites; state any required tool and version.
- Reuse the same root → module → command discovery sequence. Record anything that requires changing the convention.

**Done when:** both examples run from a clean checkout. If the second domain forces many exceptions, simplify the convention before adding more packs.

### 6. Document a reviewable improvement loop

- In `AGENTS.md`, tell agents to propose a recipe or skill change only after a repeated workflow or a concrete failure.
- Require a diff, a reason for the change, and the canonical check before a human merges it. Keep review in normal Git workflow; no self-editing daemon or automatic publishing.
- Walk through one real improvement and record what changed.

**Done when:** the example improvement is reproducible and a reviewer can understand its behavior and risk from the diff.

### 7. Pilot and publish v0.1

- Retrofit one existing workspace and ask a fresh agent or contributor to complete the same task with and without the catalog. Record discovery steps, failures, elapsed time, and context size if measurable. Describe the small sample honestly.
- Tighten the README quickstart and compatibility note from pilot feedback. Keep the chosen MIT license visible in release documentation.
- Tag v0.1 only after examples, checks, and links work from a clean clone.

**Done when:** another person can adopt the pattern without this conversation and the repo contains evidence for its main claims.

## Deferred until evidence calls for them

More domain packs, a custom linter beyond concrete failures, compliance badges, generated docs, an MCP adapter, and benchmark claims. Each adds maintenance cost; none is required to prove the first useful workflow.
