import os.path
import setuptools
from setuptools import setup


def read(name):
    mydir = os.path.abspath(os.path.dirname(__file__))
    return open(os.path.join(mydir, name)).read()


setuptools.setup(
    name='mkdocs-files-filter',
    version='0.0.1',
    packages=['mkdocs_files_filter'],
    url='https://github.com/DariuszPorowski/mkdocs-files-filter',
    license='MIT',
    author='Dariusz Porowski',
    author_email='Dariusz.Porowski@hotmail.com',
    description='A mkdocs plugin that lets you exclude/include files or trees.',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    install_requires=['mkdocs', 'igittigitt'],

    # The following rows are important to register your plugin.
        # The format is "(plugin name) = (plugin folder):(class name)"
        # Without them, mkdocs will not be able to recognize it.
        entry_points={
                'mkdocs.plugins': [
                    'files-filter = mkdocs_files_filter:FilesFilter',
                ]
    },
)
