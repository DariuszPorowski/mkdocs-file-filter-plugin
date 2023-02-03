#!/bin/bash

rm -rf dist && rm -rf build
python3 setup.py bdist_wheel sdist --formats gztar
# twine upload dist/*
pip uninstall -y mkdocs-file-filter
pip install dist/mkdocs-file-filter-0.0.1.tar.gz
rm -rf dist && rm -rf build
