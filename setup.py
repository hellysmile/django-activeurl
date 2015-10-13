import ast
import os
import codecs
from setuptools import setup


class VersionFinder(ast.NodeVisitor):
    def __init__(self):
        self.version = None

    def visit_Assign(self, node):  # noqa
        if node.targets[0].id == '__version__':
            self.version = node.value.s


def read(*parts):
    filename = os.path.join(os.path.dirname(__file__), *parts)
    with codecs.open(filename, encoding='utf-8') as fp:
        return fp.read()


def find_version(*parts):
    finder = VersionFinder()
    finder.visit(ast.parse(read(*parts)))
    return finder.version


classifiers = '''\
Framework :: Django
Environment :: Web Environment
Intended Audience :: Developers
Topic :: Internet :: WWW/HTTP
License :: OSI Approved :: Apache Software License
Development Status :: 5 - Production/Stable
Natural Language :: English
Programming Language :: Python
Programming Language :: Python :: 2
Programming Language :: Python :: 2.6
Programming Language :: Python :: 2.7
Programming Language :: Python :: 3
Programming Language :: Python :: 3.2
Programming Language :: Python :: 3.3
Programming Language :: Python :: 3.4
Programming Language :: Python :: 3.5
Programming Language :: Python :: Implementation :: CPython
Programming Language :: Python :: Implementation :: PyPy
Operating System :: MacOS :: MacOS X
Operating System :: Microsoft :: Windows
Operating System :: POSIX
Operating System :: Unix
'''


description = 'Easy to use active URL highlighting for django'


packages = [
    'django_activeurl',
    'django_activeurl.templatetags',
    'django_activeurl.ext'
]


setup(
    name='django-activeurl',
    version=find_version('django_activeurl', '__init__.py'),
    packages=packages,
    description=description,
    long_description=read('README.rst'),
    author='hellysmile',
    author_email='hellysmile@gmail.com',
    url='https://github.com/hellysmile/django-activeurl/',
    zip_safe=False,
    install_requires=[
        'django',
        'lxml',
        'django-classy-tags',
        'django_appconf',
    ],
    license='http://www.apache.org/licenses/LICENSE-2.0',
    classifiers=list(filter(None, classifiers.split('\n'))),
    keywords=[
        'django', 'url', 'link', 'active', 'css', 'templatetag', 'jinja2'
    ]
)
