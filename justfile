# List the repository's commands.
[metadata('effect:read', 'cost:free', 'duration:short')]
help:
    @just --list

# Check both examples and the command contract.
[metadata('effect:local', 'cost:free', 'duration:short')]
check:
    @just --unstable --fmt --check
    @just --unstable --justfile examples/minimal/justfile --fmt --check
    @just --unstable --justfile examples/content/justfile --fmt --check
    @python3 tools/validate.py justfile
    @python3 tools/validate.py examples/minimal/justfile
    @python3 tools/validate.py examples/content/justfile
    @python3 -m unittest discover -s tests
    @just --justfile examples/minimal/justfile check
    @just --justfile examples/content/justfile check
