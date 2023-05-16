#!/bin/bash

poetry poe clean-linux
poetry poe pre-commit-all
poetry poe test
poetry poe build
poetry poe mkdocs-serve --config-file mkdocs.plugins.yml
