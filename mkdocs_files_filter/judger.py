import os
import fnmatch
import re
import pathlib
import igittigitt


class Judger:
    def __init__(self, exclude_glob, exclude_regex, include_glob, include_regex, conflict_behavior, mkdocsignore, mkdocsignore_file):
        self.exclude_glob = exclude_glob
        self.exclude_regex = exclude_regex
        self.include_glob = include_glob
        self.include_regex = include_regex
        self.conflict_behavior = conflict_behavior
        self.mkdocsignore = mkdocsignore

        if self.mkdocsignore:
            self.mkdocsignore_parser = igittigitt.IgnoreParser()
            mkdocsignore_file_path = pathlib.Path(mkdocsignore_file)
            self.mkdocsignore_parser.parse_rule_file(
                pathlib.Path(mkdocsignore_file_path))


    def evaluate(self, src_path, abs_src_path):
        if os.sep is not '/':
            src_path = src_path.replace(os.sep, '/')
            abs_src_path = abs_src_path.replace(os.sep, '/')

        if not self.__included(src_path, abs_src_path):
            return False

        return True

    def __included(self, src_path, abs_src_path):
        for glob in self.include_glob:
            if fnmatch.fnmatchcase(src_path, glob):
                return True
        for regex in self.include_regex:
            if re.match(regex, src_path):
                return True
        for glob in self.exclude_glob:
            if fnmatch.fnmatchcase(src_path, glob):
                return False
        for regex in self.exclude_regex:
            if re.match(regex, src_path):
                return False
        if self.mkdocsignore and self.__mkdocsignore(abs_src_path):
            return False

        return True

    def __mkdocsignore(self, abs_src_path):
        return self.mkdocsignore_parser.match(pathlib.Path(abs_src_path))
