# Working in JustHarness

Run `just` to discover the repository commands. Read [SPEC.md](SPEC.md) before changing the convention, and inspect the relevant example's `AGENTS.md` and module catalog before running an example. Run `just check` after changes.

Keep public examples free of private workspace names, credentials, and data. Propose changes to a recipe or skill when a repeated workflow or concrete failure calls for them. Include the reason, the diff, and the `just check` result for review. Keep execution and verification in the repository's normal Git workflow; do not auto-publish changes.
