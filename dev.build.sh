#!/bin/bash

rm -rf dist && rm -rf build
poetry run black .
poetry build
pip uninstall -y mkdocs_file_filter_plugin
pip install dist/mkdocs_file_filter_plugin-*.tar.gz
