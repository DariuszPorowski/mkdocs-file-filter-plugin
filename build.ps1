# Remove-Item -Recurse -Force dist,build
python3 setup.py bdist_wheel sdist --formats gztar
pip uninstall -y mkdocs-files-filter
pip install dist\mkdocs-files-filter-0.0.1.tar.gz
# Remove-Item -Recurse -Force dist,build
