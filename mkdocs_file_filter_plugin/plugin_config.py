from mkdocs.config.base import Config as MkDocsConfigBase
import mkdocs.config.config_options as MkDocsConfigOptions


class PluginConfig(MkDocsConfigBase):
    exclude_glob = MkDocsConfigOptions.Type(list, default=[])
    exclude_regex = MkDocsConfigOptions.Type(list, default=[])
    exclude_tag = MkDocsConfigOptions.Type(list, default=[])
    include_glob = MkDocsConfigOptions.Type(list, default=[])
    include_regex = MkDocsConfigOptions.Type(list, default=[])
    include_tag = MkDocsConfigOptions.Type(list, default=[])
    mkdocsignore = MkDocsConfigOptions.Type(bool, default=False)
    mkdocsignore_file = MkDocsConfigOptions.File(exists=False, default=".mkdocsignore")
    config = MkDocsConfigOptions.Optional(
        MkDocsConfigOptions.File(exists=True, default=None)
    )
