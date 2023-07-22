#!/bin/bash

poetry poe clean-linux
poetry poe pre-commit-all
poetry poe test
poetry poe build
pushd "tests/fixtures" || exit
poetry run mkdocs serve --config-file mkdocs.plugins.yml --verbose
popd || exit
