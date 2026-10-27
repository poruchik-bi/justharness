# Check that Git and a repository are available.
[metadata('effect:read', 'cost:free', 'duration:short')]
doctor:
    @command -v git >/dev/null || { echo 'FAIL git unavailable → install Git' >&2; exit 1; }
    @git -C '{{justfile_directory()}}' rev-parse --is-inside-work-tree >/dev/null || { echo 'FAIL no Git repository → run: git init' >&2; exit 1; }
    @echo 'prerequisites: OK'

# Show the Git state without changing files.
[metadata('effect:read', 'cost:free', 'duration:short')]
status:
    @git -C '{{justfile_directory()}}' status --short --branch

# Verify that the project entry points exist and contain content.
[metadata('effect:read', 'cost:free', 'duration:short')]
check:
    @test -s '{{justfile_directory()}}/README.md' || { echo 'FAIL README.md missing → restore or write it' >&2; exit 1; }
    @test -s '{{justfile_directory()}}/AGENTS.md' || { echo 'FAIL AGENTS.md missing → restore or write it' >&2; exit 1; }
    @echo 'documentation: OK'
