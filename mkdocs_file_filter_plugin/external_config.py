"""Plugin input configuration from external file."""

import pathlib

import yaml
from mkdocs.exceptions import PluginError
from schema import Optional, Schema, SchemaError
from yaml_env_tag import construct_env_tag

from . import logger as log


class ExternalConfig:  # pylint: disable=too-few-public-methods
    """TODO."""

    def __init__(self) -> None:
        """TODO."""
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
            },
        )

    def load(self, config_path: pathlib.Path) -> dict:
        """TODO."""
        log.debug(f"Loading config file: {config_path.name!s}")
        yaml.SafeLoader.add_constructor("!ENV", construct_env_tag)
        with pathlib.Path.open(config_path, encoding="utf-8") as config_file:
            config = yaml.safe_load(config_file) or {}
        config_file.close()
        self.__validate_schema(config)
        return config

    def __validate_schema(self, config: dict) -> None:
        """TODO."""
        try:
            self.config_schema.validate(config)
            log.debug("Configuration file is valid.")
        except SchemaError as schema_error:
            raise PluginError(str(schema_error)) from schema_error
