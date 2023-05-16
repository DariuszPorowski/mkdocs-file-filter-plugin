#!/bin/bash

poetry poe clean-linux
poetry self add "poethepoet[plugin]"
poetry poe pre-commit-update
poetry poe pre-commit-all
poetry self add "poetry-dynamic-versioning[plugin]"
poetry poe test
poetry poe build
poetry poe mkdocs-serve --config-file mkdocs.plugins.yml
