import mkdocs.config.config_options as MkDocsConfigOptions
from mkdocs.config.base import Config as MkDocsConfigBase


class PluginConfig(MkDocsConfigBase):
    enabled = MkDocsConfigOptions.Type(bool, default=True)
    enabled_on_serve = MkDocsConfigOptions.Type(bool, default=False)
    exclude_glob = MkDocsConfigOptions.Type(list, default=[])
    exclude_regex = MkDocsConfigOptions.Type(list, default=[])
    exclude_tag = MkDocsConfigOptions.Type(list, default=[])
    include_glob = MkDocsConfigOptions.Type(list, default=[])
    include_regex = MkDocsConfigOptions.Type(list, default=[])
    include_tag = MkDocsConfigOptions.Type(list, default=[])
    filter_nav = MkDocsConfigOptions.Type(bool, default=True)
    metadata_property = MkDocsConfigOptions.Type(str, default="tags")
    mkdocsignore = MkDocsConfigOptions.Type(bool, default=False)
    mkdocsignore_file = MkDocsConfigOptions.File(exists=False, default=".mkdocsignore")
    config = MkDocsConfigOptions.Optional(
        MkDocsConfigOptions.File(exists=True, default=None)
    )
