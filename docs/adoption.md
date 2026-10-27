# Adopt JustHarness in an existing repository

1. Inventory the commands people and agents already run, including scripts, CI jobs, and existing `just` recipes. Pick one repeated task with a clear result.
2. Add a documented recipe that calls the existing implementation. Keep its current callers working. Add `effect`, `cost`, and `duration` metadata, plus a `verify` target if the result can be checked.
3. Add a fast `doctor` only for prerequisites that commonly fail. Name the exact repair action in each failure. Put the command discovery sequence in `AGENTS.md`: bare `just`, then the relevant module catalog, then the recipe and its check.
4. Add `just check` for fast local checks and run it in CI. Try the task from a clean checkout and a nested directory. Confirm its description, effect, artifact, and failure message are understandable without reading the implementation script.
5. Review a normal Git diff after a real failure or repeated need. Move a lesson into a command, check, agent instruction, or skill according to what would prevent the failure. Preserve the same command path for humans, agents, and CI.

A flat catalog is fine when it is easy to scan. Adding a module changes invocation and working directory, so migrate existing imports and callers deliberately. A copied block should state its source repository, revision, and license in its README once it is reused across projects.
