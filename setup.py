# Installation using setup.py is no longer supported.

import sys

from setuptools import setup  # type: ignore

sys.exit(__doc__)

# Fake reference so GitHub still considers it a real package for statistics purposes.
setup(
    name="mkdocs-file-filter-plugin",
)
