#!/bin/bash

rm -rf dist && rm -rf build && rm -rf site && rm -rf *.egg-info
poetry run isort .
poetry run black .
poetry run flake8 --count .
poetry build
pip uninstall -y mkdocs_file_filter_plugin
pip install dist/mkdocs_file_filter_plugin-*.tar.gz
