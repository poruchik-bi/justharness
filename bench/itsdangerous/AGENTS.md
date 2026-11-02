# Working in this repository

Run `just` to list the commands, then `just doctor`. `just test` runs the suite on Python 3.12; pass another installed version as `just test 3.13`. `just typing` runs mypy and pyright. Both go through tox and `uv.lock`, the same path as CI. Plain `tox` runs every Python in the env list and fails for interpreters that are not installed.
