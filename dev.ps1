poetry poe clean-win
poetry poe pre-commit-all
poetry poe test
poetry poe build
Push-Location tests\fixtures
poetry run mkdocs serve --config-file mkdocs.plugins.yml --verbose
Pop-Location
