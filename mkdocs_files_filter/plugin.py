import os
import pathlib
import yaml
from mkdocs.plugins import BasePlugin
from mkdocs.config.base import Config as ConfigBase
import mkdocs.config.config_options as ConfigOptions
from mkdocs.structure.files import Files as MkdocsFiles
from . import util as LOG
from .judger import Judger


class FilesFilterConfig(ConfigBase):
    exclude_glob = ConfigOptions.Optional(
        ConfigOptions.Type((str, list), default=None))
    exclude_regex = ConfigOptions.Optional(
        ConfigOptions.Type((str, list), default=None))
    include_glob = ConfigOptions.Optional(
        ConfigOptions.Type((str, list), default=None))
    include_regex = ConfigOptions.Optional(
        ConfigOptions.Type((str, list), default=None))
    conflict_behavior = ConfigOptions.Choice(
        ('include', 'exclude'), default='include')
    mkdocsignore = ConfigOptions.Type(bool, default=False)
    mkdocsignore_file = ConfigOptions.File(
        exists=False, default='.mkdocsignore')

    config = ConfigOptions.Optional(ConfigOptions.File(exists=True))


class FilesFilter(BasePlugin[FilesFilterConfig]):
    """A mkdocs plugin that removes all matching files from the input list."""

    def __config_list(self, name, config, external_config_file: False):
        """ Gets a list item from config. If it doesn't exist, gets empty list.
        If it is not a list, wrap it in a list """

        if external_config_file:
            result = config.get(name, [])
        else:
            result = config[name] or []
        if not isinstance(result, list):
            result = [result]
        return result

    def on_config(self, config):
        if 'config' in self.config:
            LOG.trace("Loading config file: ",
                      os.path.basename(self.config.config))
            with open(self.config.config, 'r') as f:
                files_filter_config = yaml.safe_load(f)

            self.config.exclude_glob = self.__config_list(
                'exclude_glob', files_filter_config, True)
            self.config.exclude_regex = self.__config_list(
                'exclude_regex', files_filter_config, True)
            self.config.include_glob = self.__config_list(
                'include_glob', files_filter_config, True)
            self.config.include_regex = self.__config_list(
                'include_regex', files_filter_config, True)
            self.config.conflict_behavior = files_filter_config.get(
                'conflict_behavior', 'include')
            self.config.mkdocsignore = files_filter_config.get(
                'mkdocsignore', False)
            self.config.mkdocsignore_file = files_filter_config.get(
                'mkdocsignore_file', '.mkdocsignore')

        if self.config.mkdocsignore:
            if pathlib.Path(self.config.mkdocsignore_file).is_file() is False:
                LOG.error("The path '%s' isn't an existing file." %
                          self.config.mkdocsignore_file)
                raise Exception()
        else:
            self.config.mkdocsignore_file = None

        LOG.debug("Config value 'config' = ", self.config.config)
        LOG.debug("Config value 'conflict_behavior' = ",
                  self.config.conflict_behavior)
        LOG.debug("Config value 'mkdocsignore' = ", self.config. mkdocsignore)
        LOG.debug("Config value 'mkdocsignore_file' = ",
                  self.config.mkdocsignore_file)
        LOG.debug("Config value 'exclude_glob' = ", self.config.exclude_glob)
        LOG.debug("Config value 'exclude_regex' = ", self.config.exclude_regex)
        LOG.debug("Config value 'include_glob' = ", self.config.include_glob)
        LOG.debug("Config value 'include_regex' = ", self.config.include_regex)

        return config

    def on_files(self, files, config):
        judger = Judger(
            self.config.exclude_glob, self.config.exclude_regex, self.config.include_glob, self.config.include_regex, self.config.conflict_behavior, self.config.mkdocsignore, self.config.mkdocsignore_file)
        out = []
        for file in files:
            if judger.evaluate(file.src_path, file.abs_src_path):
                LOG.debug("include file: ", file.src_path)
                out.append(file)
            else:
                LOG.debug("exclude file: ", file.src_path)
        return MkdocsFiles(out)
