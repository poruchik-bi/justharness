# App example

A small Python notes service with the commands a coding agent meets in a real project: tests (`read`), a database migration (`local`, verified by `db status`), and a release (`publish`). Run `just` to discover them. `just check` runs the tests, migrates the ignored `out/app.db`, and previews a release. It needs only Python 3 with SQLite.

`just release deploy` previews by default. `just release deploy publish` with `APP_DEPLOY_DIR` set to an existing directory copies the bundle there; the directory stands in for a real host. The tests prove that the gate refuses a missing target, an unknown mode, and a repeated release.
