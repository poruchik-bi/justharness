# Apply pending migrations to out/app.db.
[metadata('effect:local', 'cost:free', 'duration:short', 'verify:status')]
migrate:
    @PYTHONDONTWRITEBYTECODE=1 python3 '{{justfile_directory()}}/notes.py' migrate

# Fail if out/app.db is missing or has pending migrations.
[metadata('effect:read', 'cost:free', 'duration:short')]
status:
    @PYTHONDONTWRITEBYTECODE=1 python3 '{{justfile_directory()}}/notes.py' status
