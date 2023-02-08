# MkDocs File Filter Plugin

[![PyPI - Version][pypi-v-image]][pypi-v-link]
[![PyPI - Python Version][pypi-pyversions-image]][pypi-pyversions-link]

> :exclamation: **This plugin is under early Alpha stage.** Significant changes may occur. It may not yet be fully compatible with other MkDocs configurations and thus may break with some advanced configs. Once these have been resolved and all bugs have been ironed out, it will be moved to an upper stage.

---

`mkdocs-file-filter-plugin` is a [mkdocs plugin][mkdocs-plugins] that allows you to exclude/include files using Unix-style wildcards (`globs`), regular expressions (`regexes`), `.mkdocsignore` ([gitignore-style][gitignore] file) or Markdown/FrontMatter `tags` metadata.

- [Installation](#installation)
  - [pip](#pip)
  - [Poetry](#poetry)
- [Configuration](#configuration)
  - [Basic](#basic)
  - [External config](#external-config)
  - [Options](#options)
- [Usage](#usage)
  - [Globs](#globs)
  - [Regexes](#regexes)
  - [Tags](#tags)
    - [Tags metadata property](#tags-metadata-property)
    - [Custom metadata list](#custom-metadata-list)
  - [.mkdocsignore](#mkdocsignore)
  - [Navigation filtering](#navigation-filtering)
  - [Conflict behavior](#conflict-behavior)
- [License](#license)

## Installation

This package requires Python >=3.8 and MkDocs version 1.4.0 or higher.

### pip

Install the plugin using [pip][pip]:

```console
pip install mkdocs-file-filter-plugin
```

Or include it in a `requirements.txt` file in your project:

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

Add a plugin configuration to `mkdocs.yml` - below example contains only example, to adjust config for your needs read [Usage](#usage) section:

```yaml
# mkdocs.yml
plugins:
  - search # if you include another plugin, and want search you have to add it again
  - file-filter:
      filter_nav: true # default value
      exclude_glob:
        - 'exclude/this/path/**'
        - 'exclude/this/file/draft.md'
        - '*.tmp'
      exclude_regex:
        - '.*\.(tmp|bin|tar)$'
      exclude_tag:
        - draft
        - preview
      include_glob:
        - 'include/this/path/**'
        - 'include/this/file/Code-of-Conduct.md'
        - '*.png'
        - 'assets/**' # the material theme requires this folder
      include_regex:
        - '.*\.(js|css)$'
      include_tag:
        - released
```

> :warning: **NOTE**
>
> If you have no `plugins` entry in your config file yet, you'll likely also want to add the `search` plugin. MkDocs enables it by default if there is no `plugins` entry set, but now you have to enable it explicitly.
>
> More information about plugins in the [MkDocs documentation][mkdocs-plugins].

### External config

The plugin supports external files for the plugin configuration. If the external config file is specified, then plugin's config properties from `mkdocs.yml` are overwritten.

```yaml
# mkdocs.yml
plugins:
  - search # if you include another plugin, and want search you have to add it again
  - file-filter:
      config: !ENV [MY_FILE_FILTER_CONFIG, '.file-filter.yml']
      # config: path/to/config/file/.file-filter.yml
```

> :bulb: **HINT**
>
> For external file config, you can use [MkDocs Environment Variables][mkdocs-envs] to set the desired file dynamically. A useful case for serving the site with different content based on stage/environment/etc. Works well with CI/CD automation.

External plugin config file example:

```yaml
# mkdocs.file-filter.yml
enabled: !ENV [CI, true]
enabled_on_serve: true
filter_nav: true
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

> :warning: **NOTE**
>
> - External config uses exactly the same properties as plugin's config in the `mkdocs.yml` except `config` property.
>
> - External config support [MkDocs Environment Variables][mkdocs-envs] as well.

### Options

The below table shows all supported options by the plugin.

| Property | Type | Default | Description |
| --- | --- | --- | --- |
| `config` | string | *none* | Path to external plugin's configuration file |
| `enabled` | bool | `true` | Turn on/off plugin without removing/adding plugin's config from `mkdocs.yml` |
| `enabled_on_serve` | bool | `false` | Turn on/off plugin on `serve` command |
| `filter_nav` | bool | `true` | Remove `nav` items pointed to excluded files |
| `mkdocsignore` | bool | `false` | Use gitignore-style file for patterns |
| `mkdocsignore_file` | string | `.mkdocsignore` | Path to gitignore-style file with patterns |
| `metadata_property` | string | `tags` | What Markdown/FrontMatter metadata property list will be used for checking keywords |
| `exclude_tag` | [string] | *none* | List of excluded tags |
| `include_tag` | [string] | *none* | List of included tags |
| `exclude_glob` | [string] | *none* | Exclude glob patterns |
| `include_glob` | [string] | *none* | Include glob patterns |
| `exclude_regex` | [string] | *none* | Exclude regex patterns |
| `include_regex` | [string] | *none* | Include regex patterns |

## Usage

> :warning: **NOTE**
>
> - If you do not provide patterns, everything will stay the same - standard MkDocs behavior - include all.
>
> - Because of the YAML syntax specifics, glob/regex patterns that start with a punctuation mark must be quoted.
>
> - The preferred way for quotes is to use single quotes `'` rather than double quotes `"` - regex backslash escapes are preserved correctly without being doubled up.
>
> - You can combine all patterns - globs/regexes with tags, and mkdocsignore.

### Globs

```yaml
# mkdocs.yml
plugins:
  - file-filter:
      filter_nav: true # default value
      exclude_glob:
        - 'drafts/**'
      include_glob:
        - 'drafts/**/preview-*.md'
```

**RESULT:** exclude all content from `drafts` and related subdirectories, but include all markdown files with prefix starting `preview` from `drafts` and related subdirectories.

> :warning: **NOTE**
>
> **Glob** patterns relative to your [docs_dir][mkdocs-docs-dir] setting from `mkdocs.yml`

### Regexes

```yaml
# mkdocs.yml
plugins:
  - file-filter:
      filter_nav: true # default value
      exclude_regex:
        - '.*\.(tmp|bin|tar)$'
      include_regex:
        - '.*\.(js|css)$'
```

**RESULT:** exclude all files with `tmp`, `bin` or `tar` extension and include all files with `js`, or `css` extension.

> :warning: **NOTE**
>
> **Regex** patterns relative to your [docs_dir][mkdocs-docs-dir] setting from `mkdocs.yml`

### Tags

You can filter your content based on the [Markdown metadata][mkdocs-metadata] (often called front-matter) keywords.

#### Tags metadata property

By default plugin filter files using `tags` property of your Markdown metadata.

```yaml
# mkdocs.yml
plugins:
  - file-filter:
      filter_nav: true # default value
      exclude_tag:
        - abc
        - draft
        - alpha
      include_tag:
        - foo
        - release
        - beta
```

`fileA.md` metadata example:

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

`fileB.md` metadata example:

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

**RESULT:** only `fileA.md` will be included.

#### Custom metadata list

Because the `tags` property is very often used to render tags on the site, in some scenarios, you'd like to filter files using specific tag keywords and avoid rendering them. In that case, you can create a custom metadata list and use it for filtering without affecting tags' used for rendering.

Set `metadata_property` with your custom list property, e.g., `labels` for this example.

```yaml
# mkdocs.yml
plugins:
  - file-filter:
      filter_nav: true # default value
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

`fileA.md` metadata example:

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

# Markdown with metadata - tags and custom list

Lorem ipsum dolor sit amet...
```

`fileB.md` metadata example:

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

# Markdown with metadata - tags and custom list

Lorem ipsum dolor sit amet...
```

**RESULT:** only `fileB.md` will be included.

### .mkdocsignore

Setting `mkdocsignore` to `true` will exclude the dirs/files specified in the `.mkdocsignore`. Use the same syntax as you use for [gitignore][gitignore].

Optionally you can set `mkdocsignore_file` parameter with your path to `.mkdocsignore` file. By default, the plugin uses `.mkdocsignore` from the root of your MkDocs.

Example config for mkdocsignore.

```yaml
# mkdocs.yml
plugins:
  - file-filter:
      filter_nav: true # default value
      mkdocsignore: true # default: false
      mkdocsignore_file: 'custom/path/.mkdocsignore' # optional, relative to mkdocs.yml, default: .mkdocsignore
```

Example `.mkdocsignore` file.

```bash
# MkDocs
docs/test/**
docs/**/draft-*.md
```

**RESULT:** exclude all content from `docs/test` and related subdirectories and all markdown files with prefix starting `draft` from `docs` and related subdirectories.

> :warning: **NOTE**
>
> **.mkdocsignore** patterns relative to your root.

### Navigation filtering

Suppose you customized [MkDocs navigation configuration][mkdocs-nav], and your `nav` contains elements defined in exclude patterns. In that case, the default MkDocs behavior is to render navigation to a non-existing file, and generated site gives 404.

By default, the plugin filters those cases and removes not working navigation items.

You can control the plugin's behavior to explicitly disable that option by setting `filter_nav: false`.

Example `mkdocs.yml` config.

```yaml
# mkdocs.yml
nav:
- Foo: exclude/this/path
- Bar: exclude/this/file/draft.md
- Abc:
    - About: exclude/this/path/about.md
    - Contact: include/this/file/contact.md
- Xyz: path/xyz.md

plugins:
  - file-filter:
      filter_nav: true # default value
      exclude_glob:
        - 'exclude/this/path/**'
        - 'exclude/this/file/draft.md'
```

**Nav** results with `filter_nav: false`:

```yaml
- Foo: exclude/this/path # -> 404
- Bar: exclude/this/file/draft.md # -> 404
- Abc:
    - About: exclude/this/path/about.md # -> 404
    - Contact: include/this/file/contact.md
- Xyz: path/xyz.md
```

**Nav** results with `filter_nav: true`:

```yaml
- Abc:
    - Contact: include/this/file/contact.md
- Xyz: path/xyz.md
```

> :warning: **NOTE**
>
> If you use any other 3rd-party plugins that modify navigation (e.g., [mkdocs-awesome-pages-plugin][mkdocs-awesome-pages-plugin-pypi]) - first, test and evaluate expected behavior. Plugin configuration order may impact results.

> In most cases is recommended to transform navigation first and next filter with the file-filter plugin.

### Conflict behavior

It is possible to exclude and include will have conflict. For example, you could exclude `drafts/**` but include `*.md`. In that case, **include** has higher priority over exclude. So all `*.md` files from the drafts folder will be **included**.

## License

`mkdocs-file-filter-plugin` is distributed under the terms of the [MIT][mit] license.

[pypi-v-image]: https://img.shields.io/pypi/v/mkdocs-file-filter-plugin.svg
[pypi-v-link]: https://pypi.org/project/mkdocs-file-filter-plugin
[pypi-pyversions-image]: https://img.shields.io/pypi/pyversions/mkdocs-file-filter-plugin.svg
[pypi-pyversions-link]: https://pypi.org/project/mkdocs-file-filter-plugin
[mkdocs-plugins]: http://www.mkdocs.org/user-guide/plugins
[mkdocs-envs]: https://www.mkdocs.org/user-guide/configuration/#environment-variables
[mkdocs-metadata]: https://www.mkdocs.org/user-guide/writing-your-docs/#meta-data
[mkdocs-docs-dir]: https://www.mkdocs.org/user-guide/configuration/#docs_dir
[mkdocs-nav]: https://www.mkdocs.org/user-guide/writing-your-docs/#configure-pages-and-navigation
[poetry]: https://python-poetry.org
[pip]: https://pip.pypa.io
[gitignore]: https://git-scm.com/docs/gitignore
[mit]: https://opensource.org/licenses/MIT
[mkdocs-awesome-pages-plugin-pypi]: https://pypi.org/project/mkdocs-awesome-pages-plugin
