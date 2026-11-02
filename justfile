# List the repository's commands.
[metadata('effect:read', 'cost:free', 'duration:short')]
help:
    @just --list

# Check the examples and the command contract.
[metadata('effect:local', 'cost:free', 'duration:short')]
check:
    @just --unstable --fmt --check
    @just --unstable --justfile examples/minimal/justfile --fmt --check
    @just --unstable --justfile examples/content/justfile --fmt --check
    @just --unstable --justfile examples/app/justfile --fmt --check
    @python3 tools/validate.py justfile
    @python3 tools/validate.py examples/minimal/justfile
    @python3 tools/validate.py examples/content/justfile
    @python3 tools/validate.py examples/app/justfile
    @python3 tools/validate.py bench/itsdangerous/justfile
    @just --unstable --justfile bench/itsdangerous/justfile --fmt --check
    @python3 -m unittest discover -s tests
    @just --justfile examples/minimal/justfile check
    @just --justfile examples/content/justfile check
    @just --justfile examples/app/justfile check

# Benchmark fresh agent sessions on itsdangerous with and without the catalog; writes runs/ab/.
[metadata('effect:external', 'cost:metered', 'duration:long')]
bench runs="3" model="claude-sonnet-5-5":
    @python3 bench/ab.py --runs {{ runs }} --model {{ model }}
