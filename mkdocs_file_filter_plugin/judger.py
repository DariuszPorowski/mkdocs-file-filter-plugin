import os
import fnmatch
import re
import pathlib
import igittigitt


class Judger:
    def __init__(self, config):
        self.config = config

        if self.config.mkdocsignore:
            self.mkdocsignore_parser = igittigitt.IgnoreParser()
            self.mkdocsignore_parser.parse_rule_file(
                pathlib.Path(self.config.mkdocsignore_file)
            )

    def evaluate(self, src_path, abs_src_path):
        if os.sep is not "/":
            src_path = src_path.replace(os.sep, "/")
            abs_src_path = abs_src_path.replace(os.sep, "/")

        if not self.__included(src_path, abs_src_path):
            return False

        return True

    def __included(self, src_path, abs_src_path):
        for glob in self.config.include_glob:
            if fnmatch.fnmatchcase(src_path, glob):
                return True
        for regex in self.config.include_regex:
            if re.match(regex, src_path):
                return True
        for glob in self.config.exclude_glob:
            if fnmatch.fnmatchcase(src_path, glob):
                return False
        for regex in self.config.exclude_regex:
            if re.match(regex, src_path):
                return False
        if self.config.mkdocsignore and self.__mkdocsignore(abs_src_path):
            return False

        return True

    def __mkdocsignore(self, abs_src_path):
        return self.mkdocsignore_parser.match(pathlib.Path(abs_src_path))
