# Files exclude/include plugin for MkDocs

`mkdocs-file-filter` is a [mkdocs plugin](http://www.mkdocs.org/user-guide/plugins/) that allows you to exclude or include files from your input using Unix-style wildcards (globs) or regular expressions (regexes).

## Quick start

1. Install the module using pip: `pip install mkdocs-file-filter`

1. In your project, add a plugin configuration to `mkdocs.yml`:

  ```yaml
  plugins:
    - file-filter:
        mkdocsignore: true
        exclude_glob:
          - 'exclude/this/path/*'
          - '*.tmp'
          - '*.pdf'
          - '*.gz'
        exclude_regex:
          - '.*\.(tmp|bin|tar)$'
        include_glob:
          - 'include/this/path/*'
          - '*.png"
          - '*.md"
          - 'assets/**' # the material theme requires this folder
        include_regex:
          - '.*\.(js|css)$'
  ```

## External config file

The plugin supports external files for the plugin's configuration. If the config file is specified, then `*_glob:` and `*_regex:` are not taken

  ```yaml
  plugins:
    - file-filter:
        # config: !ENV [MY_ENV_VAR_, "mkdocs.file-filter.yml"]
        config: mkdocs.file-filter.yml
  ```

You can provide zero or more patterns of each type. (If you don't give any patterns, nothing will happen!)

Note! Because of the peculiarity of yaml syntax, the `*_glob:` and `*_regex:` lines **must not** start with a dash, but the lines under them **must** begin with a dash.

Also, because of yaml, patterns that start with a punctuation mark must be quoted.

When writing regexes, it's best to use single quotes rather than double quotes so that your regex backslash escapes are preserved correctly without being doubled up.

## Exclude and Include

It is possible to exclude and include. For example, you could exclude `*` but include `*.md`.

**Include** has higher priority over exclude.

## .mkdocsignore

Setting `mkdocsignore` to `true` will ignore dirs/files specified in the `.mkdocsignore`. Use the same syntax as you use for gitignore.
