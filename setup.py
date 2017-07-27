import sys
from io import open

from setuptools import setup
from setuptools.command.test import test as TestCommand


about = {}
with open("django_activeurl/__about__.py", encoding='utf-8') as fp:
    exec(fp.read(), about)


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def run_tests(self):
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


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
Programming Language :: Python :: 3.6
Programming Language :: Python :: Implementation :: CPython
Programming Language :: Python :: Implementation :: PyPy
Operating System :: MacOS :: MacOS X
Operating System :: Microsoft :: Windows
Operating System :: POSIX
Operating System :: Unix
'''


def long_description():
    f = open('README.rst', encoding='utf-8')
    rst = f.read()
    f.close()
    return rst


packages = [
    'django_activeurl',
    'django_activeurl.templatetags',
    'django_activeurl.ext'
]


setup(
    name=about['__title__'],
    version=about['__version__'],
    url='https://github.com/hellysmile/django-activeurl/',
    download_url='https://pypi.python.org/pypi/django-activeurl',
    packages=packages,
    description=about['__description__'],
    long_description=long_description(),
    author=about['__author__'],
    author_email=about['__email__'],
    zip_safe=False,
    install_requires=[
        'django',
        'lxml',
        'django-classy-tags',
        'django_appconf',
    ],
    license=about['__license__'],
    classifiers=list(filter(None, classifiers.split('\n'))),
    keywords=[
        'django', 'url', 'link', 'active', 'css', 'templatetag', 'jinja2'
    ],
    cmdclass={'test': PyTest},
)
