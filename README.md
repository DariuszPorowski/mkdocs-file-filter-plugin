# File exclude/include plugin for MkDocs

[![PyPI - Version](https://img.shields.io/pypi/v/mkdocs-file-filter-plugin.svg)](https://pypi.org/project/mkdocs-file-filter-plugin)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/mkdocs-file-filter-plugin.svg)](https://pypi.org/project/mkdocs-file-filter-plugin)

---

`mkdocs-file-filter` is a [mkdocs plugin](http://www.mkdocs.org/user-guide/plugins/) that allows you to exclude/include files from your input using Unix-style wildcards (globs), regular expressions (regexes) or .mkdocsignore file ([gitignore-style](https://git-scm.com/docs/gitignore) syntax).

## Quick start

1. Install the plugin using pip.

```console
pip install mkdocs-file-filter-plugin
```

1. In your project, add a plugin configuration to `mkdocs.yml`:

  ```yaml
  plugins:
    - file-filter:
        mkdocsignore: true
        mkdocsignore_file: 'custom/path/.mkdocsignore' # relative to mkdocs.yml
        exclude_glob:
          - 'exclude/this/path/*'
          - 'exclude/this/file/draft.md'
          - '*.tmp'
          - '*.gz'
        exclude_regex:
          - '.*\.(tmp|bin|tar)$'
        include_glob:
          - 'include/this/path/*'
          - 'include/this/file/Code-of-Conduct.md'
          - '*.png'
          - 'assets/**' # the material theme requires this folder
        include_regex:
          - '.*\.(js|css)$'
  ```

## External config file

The plugin supports external files for the plugin configuration. If the external config file is specified, then `*_glob:` and `*_regex:` are not taken `mkdocs.yml` - only config from the external file applies.

```yaml
plugins:
  - file-filter:
      # config: !ENV [MY_FILE_FILTER_CONFIG, 'mkdocs.file-filter.yml']
      config: mkdocs.file-filter.yml
```

External plugin config file example.

```yaml
mkdocsignore: false
exclude_glob:
  - 'exclude/this/path/*'
  - 'exclude/this/file/draft.md'
  - '*.tmp'
  - '*.gz'
exclude_regex:
  - '.*\.(tmp|bin|tar)$'
include_glob:
  - 'include/this/path/*'
  - 'include/this/file/Code-of-Conduct.md'
  - '*.png'
  - 'assets/**' # the material theme requires this folder
include_regex:
  - '.*\.(js|css)$'
```

> **HINT**
>
> For external file config, you can use [MkDocs Environment Variables](https://www.mkdocs.org/user-guide/configuration/#environment-variables) to set the desired file dynamically. A useful case for serving the site with different content based on stage/environment. Works well with CI/CD automation.

## .mkdocsignore

Setting `mkdocsignore` to `true` will exclude the dirs/files specified in the `.mkdocsignore`. Use the same syntax as you use for gitignore.

Optionally you can set `mkdocsignore_file` parameter with your path to `.mkdocsignore` file. By default, the plugin uses `.mkdocsignore` from the root of your MkDocs.

You can combine mkdocsignore with globs/regex as well. The patterns from both will apply.

External config for mkdocsignore.

```yaml
plugins:
  - file-filter:
      mkdocsignore: true # default: false
      mkdocsignore_file: 'custom/path/.myignore' # relative to mkdocs.yml, default: .mkdocsignore
```

Example `.mkdocsignore` file.

```bash
# MkDocs
docs/test/**
docs/**/draft-*.md
```

## Conflict behavior

It is possible to exclude and include will have conflict. For example, you could exclude `drafts/*` but include `*.md`. In that case, **include** has higher priority over exclude. So all `*.md` files from the drafts folder will be included.

## Some useful stuff

If you do not provide patterns, everything will stay the same - standard MkDocs behavior.

Because of the YAML syntax specifics, patterns that start with a punctuation mark must be quoted.

The preferred way for quotes is to use single quotes `'` rather than double quotes `"` - regex backslash escapes are preserved correctly without being doubled up.

## License

`mkdocs-file-filter-plugin` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
