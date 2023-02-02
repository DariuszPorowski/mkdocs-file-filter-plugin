import fnmatch
import re
import os
import mkdocs
import mkdocs.plugins
import mkdocs.structure.files
import pathlib
import igittigitt
import logging
import yaml
from mkdocs.utils import warning_filter
from mkdocs.config import base, config_options as c
LOG = logging.getLogger("mkdocs.plugins." + __name__)
LOG.addFilter(warning_filter)


class ExcludeDecider:
    def __init__(self, exclude_globs, exclude_regexes, include_globs, include_regexes, gitignore):
        self.exclude_globs = exclude_globs
        self.exclude_regexes = exclude_regexes
        self.include_globs = include_globs
        self.include_regexes = include_regexes
        self.gitignore = gitignore

        if self.gitignore:
            self.gitignore_parser = igittigitt.IgnoreParser()
            self.gitignore_parser.parse_rule_file(pathlib.Path('.gitignore'))

    def is_include(self, src_path, abs_src_path):
        if not self._is_include(src_path, abs_src_path):
            return False
        # Windows reports filenames as eg.  a\\b\\c instead of a/b/c.
        # To make the same globs/regexes match filenames on Windows and
        # other OSes, let's try matching against converted filenames.
        # On the other hand, Unix actually allows filenames to contain
        # literal \\ characters (although it is rare), so we won't
        # always convert them.  We only convert if os.sep reports
        # something unusual. Conversely, some future mkdocs might
        # report Windows filenames using / separators regardless of
        # os.sep, so we *always* test with / above.
        if os.sep != '/':
            filefix_src_path = src_path.replace(os.sep, '/')
            filefix_abs_src_path = abs_src_path.replace(os.sep, '/')
            if not self._is_include(filefix_src_path, filefix_abs_src_path):
                return False
        return True

    def _is_include(self, src_path, abs_src_path):
        for g in self.include_globs:
            if fnmatch.fnmatchcase(src_path, g):
                return True
        for r in self.include_regexes:
            if re.match(r, src_path):
                return True
        for g in self.exclude_globs:
            if fnmatch.fnmatchcase(src_path, g):
                return False
        for r in self.exclude_regexes:
            if re.match(r, src_path):
                return False
        if self.gitignore and self._git_ignores(abs_src_path):
            return False

        return True

    def _git_ignores(self, abs_src_path):
        if os.path.basename(abs_src_path) == '.git':  # Ignore .git directory
            return True
        return self.gitignore_parser.match(pathlib.Path(abs_src_path))


def get_list_from_config(name, config, config_file: False):
    """ Gets a list item from config. If it doesn't exist, gets empty list.
    If it is not a list, wrap it in a list """

    if config_file:
        result = config.get(name, [])
    else:
        result = config[name] or []
    if not isinstance(result, list):
        result = [result]
    return result


class FilesFilter(mkdocs.plugins.BasePlugin):
    """A mkdocs plugin that removes all matching files from the input list."""

    config_scheme = (
        ('exclude_glob', mkdocs.config.config_options.Type((str, list), default=None)),
        ('exclude_regex', mkdocs.config.config_options.Type((str, list), default=None)),
        ('include_glob', mkdocs.config.config_options.Type((str, list), default=None)),
        ('include_regex', mkdocs.config.config_options.Type((str, list), default=None)),
        ('gitignore', mkdocs.config.config_options.Type(bool, default=False)),
        ('config', mkdocs.config.config_options.File(exists=True)),
    )

    def on_files(self, files, config):
        for k in self.config:
            for scheme in self.config_scheme:
                if scheme[0] == k:
                    break
            else:
                raise Exception(
                    "Configuration '%s' not found for files-filter" % k)

        files_filter_config_path = self.config['config']
        if files_filter_config_path is not None:
            LOG.info("Loading files-filter config file: %s",
                     os.path.basename(files_filter_config_path))
            with open(files_filter_config_path, 'r') as f:
                files_filter_config = yaml.safe_load(f)

            exclude_globs = get_list_from_config(
                'exclude_glob', files_filter_config, True)
            exclude_regexes = get_list_from_config(
                'exclude_regex', files_filter_config, True)
            include_globs = get_list_from_config(
                'include_glob', files_filter_config, True)
            include_regexes = get_list_from_config(
                'include_regex', files_filter_config, True)
            gitignore = files_filter_config.get('gitignore', False)
        else:
            exclude_globs = get_list_from_config('exclude_glob', self.config)
            exclude_regexes = get_list_from_config(
                'exclude_regex', self.config)
            include_globs = get_list_from_config('include_glob', self.config)
            include_regexes = get_list_from_config(
                'include_regex', self.config)
            gitignore = self.config['gitignore']

        LOG.debug("gitignore: %s", gitignore)
        LOG.debug("exclude_glob: %s", exclude_globs)
        LOG.debug("exclude_regex: %s", exclude_regexes)
        LOG.debug("include_glob: %s", include_globs)
        LOG.debug("include_regex: %s", include_regexes)

        exclude_decider = ExcludeDecider(
            exclude_globs, exclude_regexes, include_globs, include_regexes, gitignore)
        out = []
        for file in files:
            src_path = file.src_path
            abs_src_path = file.abs_src_path
            if exclude_decider.is_include(src_path, abs_src_path):
                LOG.info("include: %s", src_path)
                LOG.debug("include: %s", src_path)
                out.append(file)
            else:
                LOG.info("exclude: %s", src_path)
                LOG.debug("exclude: %s", src_path)
        return mkdocs.structure.files.Files(out)
