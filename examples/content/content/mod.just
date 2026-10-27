# Check Python and the fixture before producing content.
[metadata('effect:read', 'cost:free', 'duration:short')]
doctor:
    @command -v python3 >/dev/null || { echo 'FAIL python3 unavailable → install Python 3' >&2; exit 1; }
    @test -s '{{justfile_directory()}}/posts.json' || { echo 'FAIL posts.json missing → restore the fixture' >&2; exit 1; }
    @echo 'prerequisites: OK'

# Build out/review.md from the fixture source records.
[metadata('effect:local', 'cost:free', 'duration:short', 'verify:verify')]
build:
    @python3 '{{justfile_directory()}}/scripts/review.py' build

# Verify that the review sheet contains every source and claim.
[metadata('effect:read', 'cost:free', 'duration:short')]
verify:
    @python3 '{{justfile_directory()}}/scripts/review.py' verify
