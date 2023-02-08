import pathlib
from urllib.parse import urlsplit

from mkdocs.config.defaults import MkDocsConfig
from mkdocs.exceptions import PluginError as MkDocsPluginError
from mkdocs.plugins import BasePlugin as MkDocsPlugin
from mkdocs.structure.files import Files as MkDocsFiles
from mkdocs.structure.nav import Link as MkDocsLink
from mkdocs.structure.nav import Navigation as MkDocsNavigation
from mkdocs.structure.nav import Section as MkDocsSection

from . import util as LOG
from .external_config import ExternalConfig
from .judger import Judger
from .plugin_config import PluginConfig


class FileFilter(MkDocsPlugin[PluginConfig]):
    def on_startup(self, *, command, dirty):
        self.is_serve = command == "serve"

    def on_config(self, config: MkDocsConfig):
        for name, plugin in config.plugins.items():
            if name == "file-filter":
                break
            if hasattr(plugin, "on_nav"):
                LOG.info(
                    str(
                        f'The plugin "{name}" might not work correctly when '
                        "placed before file-filter in the list of plugins. "
                        'It defines an "on_nav" handler that will be overridden '
                        "by file-filter in some circumstances."
                    )
                )
            if hasattr(plugin, "on_files"):
                LOG.info(
                    str(
                        f'The plugin "{name}" might not work correctly when '
                        "placed before file-filter in the list of plugins. "
                        'It defines an "on_files" handler that will be overridden '
                        "by file-filter in some circumstances."
                    )
                )

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
                        f"The path '{self.config.mkdocsignore_file}' "
                        "isn't an existing file."
                    )
                )
            config.watch.append(pathlib.Path(self.config.mkdocsignore_file))

        for k in self.config.keys():
            LOG.debug(f"Config value '{k}' = {self.config[k]}")

        return config

    def on_files(self, files: MkDocsFiles, config: MkDocsConfig):
        if not self.config.enabled:
            return
        if not self.config.enabled_on_serve and self.is_serve:
            return

        judger = Judger(self.config, config)
        files_new = []
        for file in files:
            results, reason = judger.evaluate(file)
            if results:
                LOG.debug(f"include file: {file.src_path} (because {reason})")
                files_new.append(file)
            else:
                LOG.debug(f"exclude file: {file.src_path} (because {reason})")

        return MkDocsFiles(files_new)

    def on_nav(self, nav: MkDocsNavigation, config: MkDocsConfig, files: MkDocsFiles):
        if not self.config.enabled:
            return
        if not self.config.enabled_on_serve and self.is_serve:
            return
        if not self.config.filter_nav:
            return

        nav_items_new = []
        for nav_item in nav.items:
            if not isinstance(nav_item, MkDocsSection):
                scheme, netloc, path, query, fragment = urlsplit(nav_item.url)

            if (
                isinstance(nav_item, MkDocsLink)
                and not nav_item.url.startswith("/")
                and not scheme
                and not netloc
            ):
                LOG.debug(f"removing navigation item: {nav_item.url}")
            else:
                nav_items_new.append(nav_item)

        return MkDocsNavigation(nav_items_new, nav.pages)
