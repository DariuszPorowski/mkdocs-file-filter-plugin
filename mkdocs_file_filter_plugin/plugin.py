import concurrent.futures
import pathlib

from mkdocs.config.defaults import MkDocsConfig
from mkdocs.exceptions import PluginError as MkDocsPluginError
from mkdocs.plugins import BasePlugin as MkDocsPlugin
from mkdocs.structure.files import Files as MkDocsFiles

from . import util as LOG
from .external_config import ExternalConfig
from .judger import Judger
from .plugin_config import PluginConfig


class FileFilter(MkDocsPlugin[PluginConfig]):
    def on_startup(self, *, command, dirty):
        self.is_serve = command == "serve"

    def on_config(self, config: MkDocsConfig):
        if self.config.config is not None:
            external_config = ExternalConfig()
            file_filter_config = external_config.load(self.config.config)

            for k in self.config.keys():
                if k != "config":
                    self.config[k] = file_filter_config.get(k, self.config[k])

            config.watch.append(pathlib.Path(self.config.config))

        if not self.config.enabled:
            LOG.debug("plugin disabled")
            return
        if not self.config.enabled_on_serve and self.is_serve:
            LOG.debug("plugin disabled on serve")
            return

        if self.config.mkdocsignore is True:
            if pathlib.Path(self.config.mkdocsignore_file).is_file() is False:
                raise MkDocsPluginError(
                    str(
                        "The path '%s' isn't an existing file."
                        % self.config.mkdocsignore_file
                    )
                )
            config.watch.append(pathlib.Path(self.config.mkdocsignore_file))

        for k in self.config.keys():
            LOG.debug("Config value '%s' = %s" % (k, self.config[k]))

        return config

    def on_files(self, files: MkDocsFiles, config: MkDocsConfig):
        if not self.config.enabled:
            return
        if not self.config.enabled_on_serve and self.is_serve:
            return

        judger = Judger(self.config, config)

        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = [executor.submit(judger.evaluate, file) for file in files]
            concurrent.futures.wait(results)

        for result in results:
            file, included, reason = result.result()
            if included:
                LOG.debug("include file: %s (because %s)" % (file.src_path, reason))
                continue
            else:
                LOG.debug("exclude file: %s (because %s)" % (file.src_path, reason))
                files.remove(file)

        return files
