# -*- coding: utf-8 -*-

from io import open
import os
import sys

# Get the project root dir, which is the parent dir of this
cwd = os.getcwd()
project_root = os.path.dirname(cwd)

sys.path.insert(0, project_root)

import django_activeurl  # NOQA

# package data
about = {}
with open("../django_activeurl/__about__.py", encoding='utf-8') as fp:
    exec(fp.read(), about)


extensions = []

releases_unstable_prehistory = True
releases_document_name = "history"
releases_issue_uri = "https://github.com/hellysmile/django-activeurl/issues/%s"
releases_release_uri = "https://github.com/hellysmile/django-activeurl/tree/v%s"

templates_path = ['_templates']

source_suffix = '.rst'

master_doc = 'index'

project = about['__title__']
copyright = about['__copyright__']

version = '%s' % ('.'.join(about['__version__'].split('.'))[:2])
release = '%s' % (about['__version__'])

exclude_patterns = ['_build']

pygments_style = 'sphinx'

html_static_path = ['_static']

htmlhelp_basename = '%sdoc' % about['__title__']

latex_documents = [
    ('index', '{0}.tex'.format(about['__package_name__']),
     '{0} Documentation'.format(about['__title__']),
     about['__author__'], 'manual'),
]

man_pages = [
    ('index', about['__package_name__'],
     '{0} Documentation'.format(about['__title__']),
     about['__author__'], 1),
]

texinfo_documents = [
    ('index', '{0}'.format(about['__package_name__']),
     '{0} Documentation'.format(about['__title__']),
     about['__author__'], about['__package_name__'],
     about['__description__'], 'Miscellaneous'),
]

intersphinx_mapping = {'http://docs.python.org/': None}
