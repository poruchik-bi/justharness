# JustHarness v0.1 command contract

JustHarness is a convention for a repository's operational commands. Bare `just` lists a short root catalog. Use `mod` when related commands benefit from their own catalog (`just --list <module>`). Every public recipe has a useful one-line doc comment. A project script can do the work; the recipe is its stable, inspectable entry point. `AGENTS.md` gives agents the entry point. Add a skill only when a real decision or multi-step procedure needs more guidance than a recipe description.

Use `just` **1.42 or newer** for `[metadata(...)]`. Public recipes declare:

| Key | Values | Meaning |
| --- | --- | --- |
| `effect` | `read`, `local`, `external`, `publish` | Expected reach of the operation. `read` is intended to leave project state alone; `local` changes local state; `external` calls a remote service; `publish` sends material to an audience. |
| `cost` | `free`, `metered` | Whether normal execution may incur a usage charge. |
| `duration` | `short`, `long` | Scheduling hint; `long` does **not** imply background execution. |
| `verify` | public recipe name | A command that checks the output. A module recipe can name a sibling recipe. |
| `gate` | short text | Required for `effect:publish`; describes the explicit approval or flag that enables publishing. |

The first three keys are required. `verify` and `gate` are required only where applicable. `tools/validate.py` checks descriptions, metadata values, publish gate presence, and verify target existence from `just --dump --dump-format json`. Metadata helps discovery and review; it grants no permission and does not prove a publish gate works. A publish recipe itself must default to a non-publishing preview and enforce its stated gate. Keep secrets out of recipe arguments, logs, and artifacts.

Each operational module should provide a fast, read-only `doctor` where prerequisites can fail. Its failure should name the missing item and a real repair command or clear manual action. Keep `just check` as the default local verifier; run metered, live-service, or publishing checks through separate named recipes. Record inputs, outputs, and check results when an artifact benefits from traceability; the optional [run ledger](docs/ledger.md) demonstrates this. Report the artifact and verification result to the user.

Adopt the contract incrementally: expose one existing task, document its effect and check, then expand only when use reveals a gap. See the [adoption guide](docs/adoption.md) and the [minimal](examples/minimal/README.md) and [content](examples/content/README.md) examples. A recipe is a shell command, not a sandbox; use the project's existing authorization and review controls.
