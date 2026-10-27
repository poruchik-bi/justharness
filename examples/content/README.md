# Content review example

Run `just` and `just --list content` to discover the workflow. `just check` reads the fixture records in `posts.json`, writes `out/review.md`, and verifies that the sheet includes every source and claim. The generated `out/` directory is ignored by Git. No account, network call, or paid service is needed.

This demonstrates a file handoff between a source and a review artifact. The review decision stays with a person or a domain-specific skill; the command does not declare a claim true.
