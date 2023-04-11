"""Main plugin module."""
from __future__ import annotations

import pathlib
from typing import Literal

from mkdocs.config.defaults import MkDocsConfig  # noqa: TCH002
from mkdocs.exceptions import PluginError as MkDocsPluginError
from mkdocs.plugins import BasePlugin as MkDocsPlugin
from mkdocs.plugins import event_priority
from mkdocs.structure.files import Files as MkDocsFiles
from mkdocs.structure.nav import Navigation as MkDocsNavigation
from mkdocs.structure.nav import (
    _add_parent_links,
    _add_previous_and_next_links,
    _get_by_type,
)
from mkdocs.structure.pages import Page as MkDocsPage

from . import logger as log
from .external_config import ExternalConfig
from .judger import Judger
from .plugin_config import PluginConfig


class FileFilter(MkDocsPlugin[PluginConfig]):
    """TODO."""

    def on_startup(
        self,
        *,
        command: Literal["build", "gh-deploy", "serve"],
        dirty: bool,  # noqa: ARG002 # pylint: disable=unused-argument
    ) -> None:
        """TODO."""
        self.is_serve = command == "serve"  # pylint: disable=attribute-defined-outside-init

    def on_config(self, config: MkDocsConfig) -> MkDocsConfig | None:  # noqa: C901
        """TODO."""
        for name, plugin in config.plugins.items():
            if name == "file-filter":
                break
            if hasattr(plugin, "on_nav"):
                log.info(
                    str(
                        f'The plugin "{name}" might not work correctly when '
                        "placed after file-filter in the list of plugins. "
                        'It defines an "on_nav" handler that will be overridden '
                        "by file-filter in some circumstances.",
                    ),
                )
            if hasattr(plugin, "on_files"):
                log.info(
                    str(
                        f'The plugin "{name}" might not work correctly when '
                        "placed after file-filter in the list of plugins. "
                        'It defines an "on_files" handler that will be overridden '
                        "by file-filter in some circumstances.",
                    ),
                )

        if self.config.config is not None:
            external_config = ExternalConfig()
            file_filter_config = external_config.load(pathlib.Path(self.config.config))
            for k in self.config:
                if k != "config":
                    self.config[k] = file_filter_config.get(k, self.config[k])

            config.watch.append(str(pathlib.Path(self.config.config)))

        if not self.config.enabled:
            log.debug("plugin disabled")
            return None
        if not self.config.enabled_on_serve and self.is_serve:
            log.debug("plugin disabled on serve")
            return None

        if self.config.mkdocsignore is True:
            if pathlib.Path(self.config.mkdocsignore_file).is_file() is False:
                raise MkDocsPluginError(str(f"The path '{self.config.mkdocsignore_file}' isn't an existing file."))
            config.watch.append(str(pathlib.Path(self.config.mkdocsignore_file)))

        for k in self.config:
            log.debug(f"Config value '{k}' = {self.config[k]}")

        return config

    # @event_priority(-100)
    def on_files(self, files: MkDocsFiles, config: MkDocsConfig) -> MkDocsFiles | None:
        """TODO."""
        if not self.config.enabled:
            return None
        if not self.config.enabled_on_serve and self.is_serve:
            return None

        judger = Judger(self.config, config)
        files_new = []
        for file in files:
            result, reason = judger.evaluate_file(file)
            if result:
                log.debug(f"include file: {file.src_path} (because {reason})")
                files_new.append(file)
            else:
                log.debug(f"exclude file: {file.src_path} (because {reason})")

        return MkDocsFiles(files_new)

    @event_priority(-100)
    def on_nav(
        self,
        nav: MkDocsNavigation,
        config: MkDocsConfig,
        files: MkDocsFiles,  # pylint: disable=unused-argument  # noqa: ARG002
    ) -> MkDocsNavigation | None:
        """TODO."""
        if not self.config.enabled:
            return None
        if not self.config.enabled_on_serve and self.is_serve:
            return None
        if not self.config.filter_nav:
            return None

        judger = Judger(self.config, config)
        nav_items_new = []
        for nav_item in nav.items:
            result = judger.evaluate_nav(nav_item)
            if result is not None:
                nav_items_new.append(result)

        pages = _get_by_type(nav_items_new, MkDocsPage)
        _add_previous_and_next_links(pages)
        _add_parent_links(nav_items_new)

        return MkDocsNavigation(nav_items_new, pages)
