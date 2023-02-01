import fnmatch
import re
import os
import sys
import mkdocs
import mkdocs.plugins
import mkdocs.structure.files


class Exclude(mkdocs.plugins.BasePlugin):
    """A mkdocs plugin that removes all matching files from the input list."""

    config_scheme = (
        ('exclude-glob', mkdocs.config.config_options.Type((str, list), default=None)),
        ('exclude-regex', mkdocs.config.config_options.Type((str, list), default=None)),
        ('include-glob', mkdocs.config.config_options.Type((str, list), default=None)),
        ('include-regex', mkdocs.config.config_options.Type((str, list), default=None)),
    )

    def on_files(self, files, config):
        exclude_globs = self.config['exclude-glob'] or []
        if not isinstance(exclude_globs, list):
            exclude_globs = [exclude_globs]
        exclude_regexes = self.config['exclude-regex'] or []
        if not isinstance(exclude_regexes, list):
            exclude_regexes = [exclude_regexes]


        include_globs = self.config['include-glob'] or []
        if not isinstance(include_globs, list):
            include_globs = [include_globs]
        include_regexes = self.config['include-regex'] or []
        if not isinstance(include_regexes, list):
            include_regexes = [include_regexes]

        out = []

        def include(name):
            for g in exclude_globs:
                if fnmatch.fnmatchcase(name, g):
                    return False
            for r in exclude_regexes:
                if re.match(r, name):
                    return False
            return True
        for i in files:
            name = i.src_path
            if not include(name):
                continue

            # Windows reports filenames as eg.  a\\b\\c instead of a/b/c.
            # To make the same globs/regexes match filenames on Windows and
            # other OSes, let's try matching against converted filenames.
            # On the other hand, Unix actually allows filenames to contain
            # literal \\ characters (although it is rare), so we won't
            # always convert them.  We only convert if os.sep reports
            # something unusual.  Conversely, some future mkdocs might
            # report Windows filenames using / separators regardless of
            # os.sep, so we *always* test with / above.
            if os.sep != '/':
                namefix = name.replace(os.sep, '/')
                if not include(namefix):
                    continue
            out.append(i)
        return mkdocs.structure.files.Files(out)
