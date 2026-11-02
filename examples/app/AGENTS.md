# Working in this example

Run `just`, then `just --list db` or `just --list release`. Run `just doctor` before the other commands. After a code change, run `just test`; after a migration change, run `just db migrate` and `just db status`. `just release deploy` only previews. Never pass `publish` unless the person asked for a release in this conversation; report the release name it prints.
