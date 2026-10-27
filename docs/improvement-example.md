# A reviewable improvement from implementation

While wiring the root `just check`, its first run failed because this installed `just` requires `--unstable` for `--fmt`. The recipe now calls `just --unstable --fmt --check` for each justfile. The reason is concrete, the change is visible in the root justfile diff, and the same `just check` succeeds. This is a small example of promoting a real failure into the shared command path, without adding a rule or hook that would not prevent a different failure.
