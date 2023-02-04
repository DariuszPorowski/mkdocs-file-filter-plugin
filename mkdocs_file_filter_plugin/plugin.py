import pathlib
from mkdocs.plugins import BasePlugin
from mkdocs.config.base import Config as ConfigBase
import mkdocs.config.config_options as ConfigOptions
from mkdocs.structure.files import Files as MkdocsFiles
from mkdocs.exceptions import PluginError
from . import util as LOG
from .judger import Judger
from .yamlconfig import YamlConfig


class FileFilterConfig(ConfigBase):
    exclude_glob = ConfigOptions.Optional(
        ConfigOptions.Type((str, list), default=None))
    exclude_regex = ConfigOptions.Optional(
        ConfigOptions.Type((str, list), default=None))
    include_glob = ConfigOptions.Optional(
        ConfigOptions.Type((str, list), default=None))
    include_regex = ConfigOptions.Optional(
        ConfigOptions.Type((str, list), default=None))
    # TODO
    # conflict_behavior = ConfigOptions.Choice(
    #     ('include', 'exclude'), default='include')
    mkdocsignore = ConfigOptions.Type(bool, default=False)
    mkdocsignore_file = ConfigOptions.File(
        exists=False, default='.mkdocsignore')
    config = ConfigOptions.Optional(
        ConfigOptions.File(exists=True, default=None))


class FileFilter(BasePlugin[FileFilterConfig]):
    def on_config(self, config):
        if 'config' in self.config and self.config.config is not None:
            yaml_config = YamlConfig()
            file_filter_config = yaml_config.load(self.config.config)

            self.config.exclude_glob = file_filter_config.get(
                'exclude_glob', [])
            self.config.exclude_regex = file_filter_config.get(
                'exclude_regex', [])
            self.config.include_glob = file_filter_config.get(
                'include_glob', [])
            self.config.include_regex = file_filter_config.get(
                'include_regex', [])
            self.config.mkdocsignore = file_filter_config.get(
                'mkdocsignore', False)
            self.config.mkdocsignore_file = file_filter_config.get(
                'mkdocsignore_file', '.mkdocsignore')

        self.config.exclude_glob = self.__config_list(
            'exclude_glob', self.config)
        self.config.exclude_regex = self.__config_list(
            'exclude_regex', self.config)
        self.config.include_glob = self.__config_list(
            'include_glob', self.config)
        self.config.include_regex = self.__config_list(
            'include_regex', self.config)

        if self.config.mkdocsignore:
            if pathlib.Path(self.config.mkdocsignore_file).is_file() is False:
                raise PluginError(str("The path '%s' isn't an existing file." %
                                      self.config.mkdocsignore_file))
        else:
            self.config.mkdocsignore_file = None

        for k in self.config.keys():
            LOG.debug("Config value '%s' = %s" % (k, self.config[k]))

        return config

    def on_files(self, files, config):
        judger = Judger(self.config)
        out = []
        for file in files:
            if judger.evaluate(file.src_path, file.abs_src_path):
                LOG.debug("include file: ", file.src_path)
                out.append(file)
            else:
                LOG.debug("exclude file: ", file.src_path)
        return MkdocsFiles(out)

    def on_serve(self, server, config, builder):
        if 'config' in self.config and self.config.config is not None:
            server.watch(self.config.config)
        if self.config.mkdocsignore:
            server.watch(self.config.mkdocsignore_file)
        return server

    def __config_list(self, name, config):
        result = config[name] or []
        if not isinstance(result, list):
            result = [result]
        return result