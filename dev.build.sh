#!/bin/bash

rm -rf dist && rm -rf build && rm -rf site && rm -rf *.egg-info

# poetry run isort .
poetry run black .
poetry run flake8 --count .
# poetry run bandit --recursive .

poetry build --verbose

pip uninstall -y mkdocs_file_filter_plugin
# pip install -e dist/mkdocs_file_filter_plugin-*.tar.gz
pip install -e .

poetry run mkdocs serve --verbose --dev-addr 127.0.0.1:9001
