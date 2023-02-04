#!/bin/bash

# rm -rf dist && rm -rf build
# python3 setup.py bdist_wheel sdist --formats gztar
# # twine upload dist/*
# pip uninstall -y mkdocs-file-filter-plugin
# pip install dist/mkdocs-file-filter-plugin-0.0.1.tar.gz
# rm -rf dist && rm -rf build

# hatch clean
# hatch build

rm -rf dist && rm -rf build
poetry build

pip uninstall -y mkdocs_file_filter_plugin
pip install dist/mkdocs_file_filter_plugin-*.tar.gz

