#!/bin/bash

rm -rf dist build site *.egg-info

poetry run pre-commit autoupdate
poetry run pre-commit run --all-files
poetry self add "poetry-dynamic-versioning[plugin]"
poetry build --verbose
poetry run mkdocs build --verbose --config-file mkdocs.plugins.yml
