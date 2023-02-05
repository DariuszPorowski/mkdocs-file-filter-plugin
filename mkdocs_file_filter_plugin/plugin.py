import pathlib
from mkdocs.plugins import BasePlugin as MkDocsPlugin
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.structure.files import Files as MkDocsFiles
from mkdocs.exceptions import PluginError as MkDocsPluginError
from . import util as LOG
from .judger import Judger
from .external_config import ExternalConfig
from .plugin_config import PluginConfig


class FileFilter(MkDocsPlugin[PluginConfig]):
    def on_config(self, config: MkDocsConfig):
        if self.config.config is not None:
            external_config = ExternalConfig()
            file_filter_config = external_config.load(self.config.config)

            self.config.exclude_glob = file_filter_config.get("exclude_glob", [])
            self.config.exclude_regex = file_filter_config.get("exclude_regex", [])
            self.config.exclude_tag = file_filter_config.get("exclude_tag", [])
            self.config.include_glob = file_filter_config.get("include_glob", [])
            self.config.include_regex = file_filter_config.get("include_regex", [])
            self.config.include_tag = file_filter_config.get("include_tag", [])
            self.config.mkdocsignore = file_filter_config.get("mkdocsignore", False)
            self.config.mkdocsignore_file = file_filter_config.get(
                "mkdocsignore_file", ".mkdocsignore"
            )

            config.watch.append(pathlib.Path(self.config.config))

        if self.config.mkdocsignore is True:
            if pathlib.Path(self.config.mkdocsignore_file).is_file() is False:
                raise MkDocsPluginError(
                    str(
                        "The path '%s' isn't an existing file."
                        % self.config.mkdocsignore_file
                    )
                )
            config.watch.append(pathlib.Path(self.config.mkdocsignore_file))
        else:
            self.config.mkdocsignore_file = None

        for k in self.config.keys():
            LOG.debug("Config value '%s' = %s" % (k, self.config[k]))

        return config

    def on_files(self, files: MkDocsFiles, config: MkDocsConfig):
        judger = Judger(self.config, config)
        for file in files:
            if judger.evaluate(file):
                LOG.debug("include file: ", file.src_path)
            else:
                LOG.debug("exclude file: ", file.src_path)
                files.remove(file)
        return MkDocsFiles(files)

