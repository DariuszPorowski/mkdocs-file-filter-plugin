import os
import fnmatch
import re
import pathlib
import igittigitt
from .plugin_config import PluginConfig
from mkdocs.structure.files import File as MkDocsFile
from mkdocs.structure.pages import Page as MkDocsPage
from mkdocs.config.defaults import MkDocsConfig


class Judger:
    def __init__(self, plugin_config: PluginConfig, mkdocs_config: MkDocsConfig):
        self.plugin_config = plugin_config
        self.mkdocs_config = mkdocs_config

        if self.plugin_config.mkdocsignore:
            self.mkdocsignore_parser = igittigitt.IgnoreParser()
            self.mkdocsignore_parser.parse_rule_file(
                pathlib.Path(self.plugin_config.mkdocsignore_file)
            )

    def evaluate(self, file: MkDocsFile):
        file.src_path, file.abs_src_path = self.__path_fix(
            file.src_path, file.abs_src_path
        )
        if not self.__included(file):
            return False
        return True

    def __path_fix(self, src_path, abs_src_path):
        if os.sep is not "/":
            src_path = src_path.replace(os.sep, "/")
            abs_src_path = abs_src_path.replace(os.sep, "/")
        return src_path, abs_src_path

    def __included(self, file: MkDocsFile):
        for glob in self.plugin_config.include_glob:
            if fnmatch.fnmatchcase(file.src_path, glob):
                return True
        for regex in self.plugin_config.include_regex:
            if re.match(regex, file.src_path):
                return True
        if file.is_documentation_page() and self.plugin_config.include_tag is not []:
            tags = self.__get_metadata_tags(file)
            for tag in self.plugin_config.include_tag:
                if tag in tags:
                    return True
        for glob in self.plugin_config.exclude_glob:
            if fnmatch.fnmatchcase(file.src_path, glob):
                return False
        for regex in self.plugin_config.exclude_regex:
            if re.match(regex, file.src_path):
                return False
        if file.is_documentation_page() and self.plugin_config.exclude_tag is not []:
            tags = self.__get_metadata_tags(file)
            for tag in self.plugin_config.exclude_tag:
                if tag in tags:
                    return False
        if self.plugin_config.mkdocsignore is True:
            if self.mkdocsignore_parser.match(pathlib.Path(file.abs_src_path)):
                return False
        return True

    def __get_metadata_tags(self, file: MkDocsFile):
        page = MkDocsPage(None, file, self.mkdocs_config)
        page.read_source(self.mkdocs_config)
        return page.meta.get("tags") or []
