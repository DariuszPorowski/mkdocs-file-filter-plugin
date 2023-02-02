# Files exclude/include plugin for mkdocs

`mkdocs-files-filter` is a [mkdocs plugin](http://www.mkdocs.org/user-guide/plugins/) that allows you to exclude or include files from your input using Unix-style wildcards (globs) or regular expressions (regexes).

This implements what people were asking for in some mkdocs bugs, such as <https://github.com/mkdocs/mkdocs/issues/1500> and <https://github.com/mkdocs/mkdocs/issues/1152>.

## Quick start

1. Install the module using pip: `pip install mkdocs-files-filter`

2. In your project, add a plugin configuration to `mkdocs.yml`:

   ```yaml
   plugins:
     - files-filter:
         gitignore: true
         exclude_glob:
           - "exclude/this/path/*"
           - "*.tmp"
           - "*.pdf"
           - "*.gz"
         exclude_regex:
           - ".*\.(tmp|bin|tar)$"
         include_glob:
           - "include/this/path/*"
           - "*.png"
           - "*.md"
           - "assets/**" # the material theme requires this folder
         include_regex:
           - ".*\.(js|css)$"
   ```

You can provide zero or more patterns of each type. (If you don't give any patterns, nothing will happen!)

Note! Because of the peculiarity of yaml syntax, the `glob:` and `regex:` lines **must not** start with a dash, but the lines under them **must** begin with a dash.
Also, because of yaml, patterns that start with a punctuation mark must be quoted.

When writing regexes, it's best to use single quotes rather than double quotes so that your regex backslash escapes are preserved correctly without having to be doubled up.

## Exclude and Include

It is possible to exclude and include. For example, you could exclude `*` but include `*.md`.
Include has higher priority over exclude.

## gitignore

Setting `gitignore` to `true` will ignore files if `git` ignores them.[^1] (This
defaults to `false` if omitted.)

---

[^1]: Some environments like [`tox`](https://tox.readthedocs.io/) do not pass on the `HOME` environment variable by default. `git` uses `HOME` to expand configurations like `excludesfile = ~/.gitignore`. If you rely on `git` configurations other than what lives in your repository, this can lead to disparities between what you observe when running `git` in your shell versus what gets ignored by this plugin. If you experience this and are unable to move the requisite configuration into your repository’s `.gitignore` file(s), consider exposing the `HOME` environment variable to your build environment, or modifying `.git/config` or `.git/info/exclude` in your local repository copy.
