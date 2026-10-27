# Optional local run ledger

Use a ledger when an output needs traceability. This example runs a parameter-free recipe and its declared `verify:` recipe, then writes one JSON record under ignored `runs/`:

```sh
python3 tools/record_run.py --justfile examples/content/justfile \
  --recipe content::build --input examples/content/posts.json \
  --output examples/content/out/review.md
```

The record contains the recipe, Git revision, start time, duration, effect, declared input and output paths, command exit code, and verification exit code. It is written even when the command fails. The wrapper does not capture stdout, arguments, credentials, or an invented cost estimate. Inputs and outputs are labels supplied by the caller; only the recipe and verify result are executed. Keep sensitive path names out of labels and records. This optional pattern is for local auditability, not a replacement for an existing authoritative job or publishing ledger.
