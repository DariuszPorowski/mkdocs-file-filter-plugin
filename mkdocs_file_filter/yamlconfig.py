import os
import yaml
from schema import Optional, Schema, SchemaError
from mkdocs.exceptions import PluginError
from . import util as LOG


class YamlConfig:
    def __init__(self):
        self.config_schema = Schema({
            Optional("mkdocsignore"): bool,
            Optional("mkdocsignore_file"): str,
            Optional("exclude_glob"): [str],
            Optional("exclude_regex"): [str],
            Optional("include_glob"): [str],
            Optional("include_regex"): [str]
        })

    def load(self, config_path):
        LOG.trace("Loading config file: ",
                  os.path.basename(config_path))
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        self.__validate(config)
        return config

    def __validate(self, config):
        try:
            self.config_schema.validate(config)
            LOG.debug("Configuration file is valid.")
        except SchemaError as se:
            raise PluginError(str(se))
