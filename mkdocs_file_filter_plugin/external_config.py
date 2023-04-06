import os
import pathlib

import yaml
from mkdocs.exceptions import PluginError
from schema import Optional, Schema, SchemaError  # type: ignore
from yaml_env_tag import construct_env_tag  # type: ignore

from . import util as LOG


class ExternalConfig:
    def __init__(self):
        self.config_schema = Schema(
            {
                Optional("enabled"): bool,
                Optional("enabled_on_serve"): bool,
                Optional("only_doc_pages"): bool,
                Optional("metadata_property"): str,
                Optional("mkdocsignore"): bool,
                Optional("mkdocsignore_file"): str,
                Optional("exclude_glob"): [str],
                Optional("exclude_regex"): [str],
                Optional("exclude_tag"): [str],
                Optional("include_glob"): [str],
                Optional("include_regex"): [str],
                Optional("include_tag"): [str],
                Optional("filter_nav"): bool,
            }
        )

    def load(self, config_path):
        config_path = pathlib.Path(config_path)
        LOG.debug(f"Loading config file: {str(os.path.basename(config_path))}")
        yaml.SafeLoader.add_constructor("!ENV", construct_env_tag)
        with open(config_path, encoding="utf-8") as f:
            config = yaml.safe_load(f) or {}
        self.__validate(config)
        return config

    def __validate(self, config):
        try:
            self.config_schema.validate(config)
            LOG.debug("Configuration file is valid.")
        except SchemaError as se:
            raise PluginError(str(se))
