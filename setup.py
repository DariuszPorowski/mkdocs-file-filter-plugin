import os.path
from setuptools import setup, find_packages

VERSION_NUMBER = '0.0.1'


def read_file(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='mkdocs-file-filter',
    version=VERSION_NUMBER,
    description='A MkDocs plugin that lets you exclude/include docs files using globs, regexes and gitignore-style file.',
    long_description=read_file('README.md'),
    long_description_content_type='text/markdown',
    keywords='mkdocs exclude include globs regexes gitignore',
    url='https://github.com/DariuszPorowski/mkdocs-file-filter',
    author='Dariusz Porowski',
    license='MIT',
    python_requires='>=3.8',
    install_requires=[
        'mkdocs>=1.4.0',
        'igittigitt',
        'pyyaml',
        'schema'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3'
        'Programming Language :: Python :: 3 :: Only',
    ],
    packages=['mkdocs_file_filter_plugin'],
    entry_points={
        'mkdocs.plugins': [
            'file-filter = mkdocs_file_filter_plugin:FileFilter',
        ]
    }
)
