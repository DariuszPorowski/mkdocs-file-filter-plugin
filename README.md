# File exclude/include plugin for MkDocs

[![PyPI - Version](https://img.shields.io/pypi/v/mkdocs-file-filter-plugin.svg)](https://pypi.org/project/mkdocs-file-filter-plugin)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/mkdocs-file-filter-plugin.svg)](https://pypi.org/project/mkdocs-file-filter-plugin)

---

`mkdocs-file-filter-plugin` is a [mkdocs plugin][mkdocs-plugins] that allows you to exclude/include files from your input using Unix-style wildcards (`globs`), regular expressions (`regexes`), `.mkdocsignore` file ([gitignore-style][gitignore] syntax) or Markdown/Frontmatter `tags` metadata.

## Installation

This package requires Python >=3.8 and MkDocs version 1.4.0 or higher.

### pip

Install the plugin using [pip][pip]:

```console
pip install mkdocs-file-filter-plugin
```

Or include it in a `requirements.txt` file in your project

```python
mkdocs==1.4.*
mkdocs-file-filter-plugin==0.0.*
```

and run

```console
pip install -r requirements.txt
```

### Poetry

Install the plugin using [Poetry][poetry]:

```console
poetry add mkdocs-file-filter-plugin
```

## Configuration

### Basic

Add a plugin configuration to `mkdocs.yml`:

```yaml
plugins:
  - search # if you include another plugin, and want search you have to add it again
  - file-filter:
      exclude_glob:
        - 'exclude/this/path/*'
        - 'exclude/this/file/draft.md'
        - '*.tmp'
      exclude_regex:
        - '.*\.(tmp|bin|tar)$'
      exclude_tag:
        - draft
        - preview
      include_glob:
        - 'include/this/path/*'
        - 'include/this/file/Code-of-Conduct.md'
        - '*.png'
        - 'assets/**' # the material theme requires this folder
      include_regex:
        - '.*\.(js|css)$'
      include_tag:
        - released
```

> **NOTE**
>
> If you have no `plugins` entry in your config file yet, you'll likely also want to add the `search` plugin. MkDocs enables it by default if there is no `plugins` entry set, but now you have to enable it explicitly.

More information about plugins in the [MkDocs documentation][mkdocs-plugins].

### External config

The plugin supports external files for the plugin configuration. If the external config file is specified, then plugin's config properties from `mkdocs.yml` are overwritten.

```yaml
plugins:
  - search # if you include another plugin, and want search you have to add it again
  - file-filter:
      config: !ENV [MY_FILE_FILTER_CONFIG, 'mkdocs.file-filter.yml']
```

External plugin config file example:

```yaml
enabled_on_serve: true
mkdocsignore: false
exclude_glob:
  - 'exclude/this/path/*'
  - 'exclude/this/file/draft.md'
  - '*.tmp'
exclude_regex:
  - '.*\.(tmp|bin|tar)$'
exclude_tag:
  - draft
include_glob:
  - 'include/this/path/*'
  - 'include/this/file/Code-of-Conduct.md'
  - '*.png'
  - 'assets/**' # the material theme requires this folder
include_regex:
  - '.*\.(js|css)$'
include_tag:
  - prod
```

> **HINT**
>
> For external file config, you can use [MkDocs Environment Variables][mkdocs-envs] to set the desired file dynamically. A useful case for serving the site with different content based on stage/environment/etc. Works well with CI/CD automation.

### .mkdocsignore

Setting `mkdocsignore` to `true` will exclude the dirs/files specified in the `.mkdocsignore`. Use the same syntax as you use for [gitignore][gitignore].

Optionally you can set `mkdocsignore_file` parameter with your path to `.mkdocsignore` file. By default, the plugin uses `.mkdocsignore` from the root of your MkDocs.

You can combine mkdocsignore with globs/regexes nad tags as well. The patterns from all will apply.

Example config for mkdocsignore.

```yaml
plugins:
  - file-filter:
      enabled_on_serve: true # default: false
      mkdocsignore: true # default: false
      mkdocsignore_file: 'custom/path/.myignore' # relative to mkdocs.yml, default: .mkdocsignore
```

Example `.mkdocsignore` file.

```bash
# MkDocs
docs/test/**
docs/**/draft-*.md
```

## Usage

The below table shows all supported properties by the plugin.

| Property | Type | Default | Description |
| --- | --- | --- | --- |
| `config` | string | *none* | Path to external plugin's configuration file |
| `enabled` | bool | `true` | Turn on/off plugin without removing/adding plugin's config from `mkdocs.yml` |
| `enabled_on_serve` | bool | `false` | Turn on/off plugin on `serve` command |
| `mkdocsignore` | bool | `false` | Use gitignore-style file for patterns |
| `mkdocsignore_file` | string | `.mkdocsignore` | Path to gitignore-style file with patterns |
| `metadata_property` | string | `tags` | What markdown/frontmatter metadata property will be used for checking tags |
| `exclude_tag` | [string] | *none* | List of excluded tags |
| `include_tag` | [string] | *none* | List of included tags |
| `exclude_glob` | [string] | *none* | Exclude glob patterns |
| `include_glob` | [string] | *none* | Include glob patterns |
| `exclude_regex` | [string] | *none* | Exclude regex patterns |
| `include_regex` | [string] | *none* | Include regex patterns |

> **NOTE**
>
> - If you do not provide patterns, everything will stay the same - standard MkDocs behavior.
>
> - Because of the YAML syntax specifics, glob/regex patterns that start with a punctuation mark must be quoted.
>
> - The preferred way for quotes is to use single quotes `'` rather than double quotes `"` - regex backslash escapes are preserved correctly without being doubled up.

### Globs

```yaml
plugins:
  - file-filter:
      exclude_glob:
        - 'TODO'
        - 'TODO'
      include_glob:
        - 'TODO'
        - 'TODO'
```

### Regexes

```yaml
plugins:
  - file-filter:
      exclude_regex:
        - 'TODO'
        - 'TODO'
      include_regex:
        - 'TODO'
        - 'TODO'
```

### Tags

#### Tags metadata property

```yaml
plugins:
  - file-filter:
      exclude_tag:
        - foo
        - draft
        - alpha
      include_tag:
        - xyz
        - release
        - beta
```

```markdown
<!-- fileA.md -->
---
tags:
  - foo
  - bar
---

# Markdown with tags metadata

Lorem ipsum dolor sit amet...
```

```markdown
<!-- fileB.md -->
---
tags:
  - abc
  - xyz
---

# Markdown with tags metadata

Lorem ipsum dolor sit amet...
```

#### Custom metadata property

```yaml
plugins:
  - file-filter:
      metadata_property: labels
      exclude_tag:
        - foo
        - draft
        - alpha
      include_tag:
        - xyz
        - release
        - beta
```

```markdown
<!-- fileA.md -->
---
tags:
  - foo
  - bar
labels:
  - draft
  - internal
---

# Markdown with metadata - tags and labels

Lorem ipsum dolor sit amet...
```

```markdown
<!-- fileB.md -->
---
tags:
  - foo
  - bar
labels:
  - release
  - v1
---

# Markdown with metadata - tags and labels

Lorem ipsum dolor sit amet...
```

### Conflict behavior

It is possible to exclude and include will have conflict. For example, you could exclude `drafts/*` but include `*.md`. In that case, **include** has higher priority over exclude. So all `*.md` files from the drafts folder will be **included**.

## License

`mkdocs-file-filter-plugin` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.

[mkdocs-plugins]: http://www.mkdocs.org/user-guide/plugins/
[mkdocs-envs]: https://www.mkdocs.org/user-guide/configuration/#environment-variables
[poetry]: https://python-poetry.org/
[pip]: https://pip.pypa.io/
[gitignore]: https://git-scm.com/docs/gitignore
