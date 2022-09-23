# -*- coding: utf-8 -*-
import io

from setuptools import setup

about = {}
with io.open('django_activeurl/__about__.py', encoding='utf-8') as fp:
    exec(fp.read(), about)


classifiers = '''\
Framework :: Django
Environment :: Web Environment
Intended Audience :: Developers
Topic :: Internet :: WWW/HTTP
License :: OSI Approved :: Apache Software License
Development Status :: 5 - Production/Stable
Natural Language :: English
Programming Language :: Python
Programming Language :: Python :: 3
Programming Language :: Python :: 3.8
Programming Language :: Python :: 3.9
Programming Language :: Python :: 3.10
Programming Language :: Python :: Implementation :: CPython
Programming Language :: Python :: Implementation :: PyPy
Operating System :: MacOS :: MacOS X
Operating System :: Microsoft :: Windows
Operating System :: POSIX
Operating System :: Unix
'''


def long_description():
    with io.open('README.rst', encoding='utf-8') as fp:
        return fp.read()


packages = [
    str('django_activeurl'),
    str('django_activeurl.templatetags'),
    str('django_activeurl.ext'),
]

install_requires = [
    'django<2;python_version<"3"',
    'django;python_version>"2"',
    'lxml',
    'django-classy-tags',
    'django_appconf',
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
    install_requires=install_requires,
    license=about['__license__'],
    classifiers=list(filter(None, classifiers.split('\n'))),
    keywords=[
        'django', 'url', 'link', 'active', 'css', 'templatetag', 'jinja2',
    ],
)
