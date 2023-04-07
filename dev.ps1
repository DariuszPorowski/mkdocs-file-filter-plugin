$paths = @('dist', 'build', 'site', '*.egg-info')
Remove-Item -Path $paths -Recurse -Force -ErrorAction SilentlyContinue

poetry run pre-commit autoupdate
poetry run pre-commit run --all-files
poetry self add "poetry-dynamic-versioning[plugin]"
poetry build --verbose
poetry run mkdocs build --verbose --config-file mkdocs.plugins.yml
