# import fnmatch
# import re


# if fnmatch.fnmatch('aaa/README.md', "['aaa/**', 'docs/test.md']"):
# if fnmatch.fnmatchcase('aaa/README.md', 'aaa/**'):
#     print("match")
# else:
#     print("no match")

# fruits = ['docs/aaa/**', 'docs/test.md']
# print("exclude_globsBBB:", fruits)
# for x in fruits:
#   print(x)


# class ExcludeDecider:
#     def __init__(self, exclude_globs):
#         self.exclude_globs = exclude_globs

#     def is_include(self):
#         print("exclude_globs111:", self.exclude_globs)
#         for g in self.exclude_globs:
#             print(g)


# exclude_globs = ['docs/aaa/**', 'docs/test.md']
# exclude_decider = ExcludeDecider(exclude_globs)

# exclude_decider.is_include()

# from gitignore_parser import parse_gitignore
# matches = parse_gitignore('.gitignore')
# if matches('docs/test.md'):
#     print("match")
# else:
#     print("no match")

# if matches('docs/aaa/test.md'):
#     print("match")
# else:
#     print("no match")

# import os
# import pathlib
# import igittigitt

# parser = igittigitt.IgnoreParser()
# parser.parse_rule_file(pathlib.Path('.gitignore'))

# if parser.match(pathlib.Path('docs/test.md')):
#     print("match")
# else:
#     print("no match")

# if parser.match(pathlib.Path('docs/aaa/test.md')):
#     print("match")
# else:
#     print("no match")

# print(os.path.basename('docs/aaa/.git'))

# # import os
# import yaml
# # from yaml import load, dump, file

# with open('mkdocs.files-filter.yml', 'r') as file:
#     files_filter_config = yaml.safe_load(file)

# print(files_filter_config['gitignore'])

# xyz = files_filter_config.get('gitignore')


# # try:
# #     xyz = files_filter_config['include_regex']
# # except KeyError:
# #     xyz = None

# print(xyz)
