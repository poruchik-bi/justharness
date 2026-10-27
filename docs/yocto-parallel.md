# What JustHarness can learn from Yocto

This note assumes “yokto” means the [Yocto Project](https://docs.yoctoproject.org/dev/overview-manual/index.html). It is a design comparison, not a proposal to turn JustHarness into a build system.

## The useful parallel

[BitBake](https://docs.yoctoproject.org/bitbake/dev/bitbake-user-manual/bitbake-user-manual-intro.html) is a general task engine. OpenEmbedded and Yocto supply metadata: recipes, classes, configuration, and layers. A recipe names sources, dependencies, checksums, description, and tasks. [Layers](https://docs.yoctoproject.org/dev/overview-manual/concepts.html#layers) separate related metadata so it can be shared, customized, and selected for a build. This engine/metadata split is the strongest model for JustHarness: `just` executes commands; JustHarness describes how a workspace exposes capabilities to agents and people.

| Yocto concept | Possible JustHarness counterpart | Where the analogy ends |
| --- | --- | --- |
| BitBake task engine | `just` command runner | `just` does not resolve providers or build a global dependency graph. |
| `.bb` recipe and tasks | Documented `just` recipe plus its existing script | A `just` recipe does not declare complete inputs, outputs, or checksums. |
| Layer | Borrowable group of related commands, scripts, and optional skills | A `just` module is a local namespace; calling it a reusable layer would promise more than it provides. |
| `bblayers.conf` | Root justfile selecting local modules | There is no automatic cross-repository layer resolver. |
| `.bbclass` shared build behavior | Shared script or helper | A `SKILL.md` guides an agent's judgment; it is not executable code inheritance. |
| `bitbake -g` task graph | Explicit command dependencies and links to artifacts/checks | A semantic link in a skill is not an automatically executable dependency. |
| Shared state cache | Existing project caches, where appropriate | Live API calls, publishing, and subjective creative work cannot generally be replayed from a task hash. |
| `devtool modify` → `finish` | Adapt a borrowed block, verify it, submit a Git diff | Normal Git review is enough until a real adoption needs more tooling. |

Yocto can [generate its task dependency graph](https://docs.yoctoproject.org/bitbake/dev/bitbake-user-manual/bitbake-user-manual-intro.html#generating-dependency-graphs) and uses [task signatures and a shared state cache](https://docs.yoctoproject.org/dev/overview-manual/concepts.html#shared-state-cache) to avoid rebuilding unchanged outputs. Its [layer metadata](https://docs.yoctoproject.org/dev/dev-manual/layers.html) can declare dependencies and release compatibility. Those features are valuable because builds have a relatively well-defined relationship between inputs and outputs. JustHarness can borrow the discipline of stating dependencies and provenance without claiming equivalent reproducibility.

## Two different graphs

1. **Execution graph:** commands and scripts that must run in a particular order. Encode only relationships that are safe to automate as recipe dependencies or in a project script.
2. **Knowledge graph:** goals, skills, recipes, prerequisites, artifacts, checks, and sources linked by ordinary files. An agent or person follows these links to choose and assess work. Some edges require judgment or approval and should not become automatic execution.

For example, a market-research workflow can connect source collection → dated records → claim review → approved brief → content production. The collection and report-building steps may be commands. Deciding whether a source supports a claim is a skill and review step. Publishing is an external effect with its own gate. A graph view could be generated later, but the relationships must first be true in the files and outputs.

## What makes a block borrowable

A donor project's recipe is not portable just because it is named. To use it in another workspace, the recipient needs to know:

- **Interface:** command name, arguments, and result or artifact.
- **Dependencies:** binaries, files, service access, environment, and compatible versions.
- **Effects:** local writes, external writes, interaction, duration, and cost.
- **Verification:** a fixture or safe example and the check that proves the expected behavior.
- **Provenance:** source revision and license, with no copied credentials or private data.

Keep this in a short README or skill beside a real block. A formal manifest is useful only when more than one adoption needs machine-readable validation. The receiving project should adapt paths and environment locally, run the example, and review the resulting diff. Avoid silent overrides: Yocto's [layer priorities and append files](https://docs.yoctoproject.org/dev/dev-manual/layers.html) solve a real multi-layer problem, but they also require tools to reveal which definition won. Explicit local changes are easier to inspect at this scale.

## A test before building an ecosystem

1. Choose a read-only block from a real workflow, with a fixture that is safe to share.
2. Make its command, dependencies, output, and check explicit. Run it in the donor workspace.
3. Copy it into a different workspace and compose it with one existing command. Record every adaptation needed.
4. Ask a fresh agent to discover and run the composed workflow; ask a person to review the output and provenance.
5. Compare the result with implementing the same capability directly in the receiving workspace. Keep the block convention only if reuse saves work without hiding important dependencies.

If that succeeds repeatedly, add a small index of reusable blocks. A registry, package manager, generated graph, cache, or compatibility resolver would need a separate demonstrated reason to exist.
