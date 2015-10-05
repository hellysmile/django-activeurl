from io import open

from setuptools import setup

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


def long_description():
    f = open('README.rst', encoding='utf-8')
    rst = f.read()
    f.close()
    return rst


setup(
    name='django-activeurl',
    version='0.1.9',
    packages=packages,
    description=description,
    long_description=long_description(),
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
