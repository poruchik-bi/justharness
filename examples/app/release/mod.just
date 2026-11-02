# Preview the release bundle; mode=publish copies it to APP_DEPLOY_DIR after the tests pass.
[metadata('effect:publish', 'cost:free', 'duration:short', 'gate:mode=publish argument and APP_DEPLOY_DIR')]
deploy mode="preview":
    @cd '{{justfile_directory()}}' && just test
    @PYTHONDONTWRITEBYTECODE=1 python3 '{{justfile_directory()}}/scripts/deploy.py' '{{mode}}'
