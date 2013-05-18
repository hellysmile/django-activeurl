django-activeurl
================

:info: Easy to use active url highlighting for django

.. image:: https://api.travis-ci.org/hellysmile/django-activeurl.png
    :target: https://travis-ci.org/hellysmile/django-activeurl
.. image:: https://coveralls.io/repos/hellysmile/django-activeurl/badge.png?branch=master
    :target: https://coveralls.io/r/hellysmile/django-activeurl?branch=master
.. image:: https://pypip.in/d/django-activeurl/badge.png
.. image:: https://pypip.in/v/django-activeurl/badge.png

live demo is available on `heroku.com <http://django-activeurl.herokuapp.com/>`_

features
********

* automatic highlighting currently active ``<a>`` tags with css
* automatic highlighting up-level ``<a>`` tags for your menus
* removes boring stuff from your life!

usage
*****

in your templates you need

.. code-block:: html+django

    {% load activeurl %}

then

.. code-block:: html+django

    {% activeurl %}
        <ul>
            <li>
                <a href="/some_page/">
                    some_page
                </a>
            </li>
            <li>
                <a href="/another_page/">
                    another_page
                </a>
            </li>
        </ul>
    {% endactiveurl %}

will be rendered to

.. code-block:: html

    <ul>
        <li class="active">
            <a href="/some_page/">
                some_page
            </a>
        </li>
        <li>
            <a href="/another_page/">
                another_page
            </a>
        </li>
    </ul>

if your current ``request.get_full_path()`` starts with ``/some_page/``

html tags inside ``{% activeurl %}{% endactiveurl %}`` must have valid root tag,
like ``<ul>`` or ``<div>``, etc - otherwise you will get an exception

starts with logic decided for applying "active" status for up-level ``<a>``
in your menus/submenus

installation
************

install the ``stable version`` using ``pip``

.. code-block:: console

    pip install django-activeurl

install the ``in-development version`` using ``pip``

.. code-block:: console

    pip install -e git+git://github.com/hellysmile/django-activeurl#egg=django_activeurl-dev


modify your ``settings.py``

add ``'django_activeurl'`` to your ``INSTALLED_APPS``

add ``'django.core.context_processors.request'`` to your ``TEMPLATE_CONTEXT_PROCESSORS``

like this

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'django_activeurl',
        ...
    )

    TEMPLATE_CONTEXT_PROCESSORS = (
        ...
        'django.core.context_processors.request',
        ...
    )

quick start
***********

for successful lxml building you need to install some system stuff eg:

ubuntu
------

.. code-block:: console

    sudo apt-get install libxml2 libxml2-dev libxslt-dev build-essential python-dev
    sudo ldconfig

fedora
------

.. code-block:: console

    sudo yum groupinstall 'Development Tools'
    sudo yum install libxslt-devel libxml2 libxml2-devel python-devel
    sudo ldconfig


windows
-------

pre build lxml binary you can find `here <http://www.lfd.uci.edu/~gohlke/pythonlibs/>`_

clouds
------

99.99% thats ``lxml`` will build out from the box

keep in mind, if your distro/os provides executable ``python`` with ``python3``
(like `Archlinux <https://www.archlinux.org/>`_) you may check installation
and addition instructions

ready to use example
--------------------

.. code-block:: console

    git clone https://github.com/hellysmile/django-activeurl.git
    cd django-activeurl
    virtualenv env
    source env/bin/activate
    cd example
    pip install -r dev_requirements.txt
    python manage.py syncdb
    python manage.py runserver

then open `http://127.0.0.1:8000/simplepage/page1/ <http://127.0.0.1:8000/simplepage/page1/>`_
in your favorite web-browser

configuration and performance
*****************************

in addition to ``{% activeurl %}`` you can add keyword parameters
``css_class`` and ``parent_tag``, which means css class that will
be added to parent element of ``<a>``, in this case it is ``<li>``

example

.. code-block:: html+django

    {% activeurl css_class="current" parent_tag="div" %}
        <span>{# do not forget valid html root tag #}
            <div>
                <a href="/some_page/">
                    some_page
                </a>
            </div>
        </span>
    {% endactiveurl %}

will be rendered to

.. code-block:: html

    <span>
        <div class="current">
            <a href="/some_page/">
                some_page
            </a>
        </div>
    </span>

by default these values are

.. code-block:: html+django

    {% activeurl css_class="active" parent_tag="li" %}

there is no rebuilding HTML inside template tag when no "active" urls found

if you want to apply "active" status direct to ``<a>``, just

.. code-block:: html+django

    {% activeurl parent_tag="self" %}
        <div>
            <a href="/some_page/">
                some_page
            </a>
        </div>
    {% endactiveurl %}

will be rendered to

.. code-block:: html

    <div>
        <a href="/some_page/" class="active">
            some_page
        </a>
    </div>

by default ``CACHE_ACTIVE_URL`` is ``True``, so before building HTML tree,
searching "active" urls, ``django-activeurl`` will try to get
previously rendered HTML from your cache backend

you can disable caching in your ``settngs.py``

.. code-block:: python

    CACHE_ACTIVE_URL = False

in addition you can set ``CACHE_ACTIVE_URL_TIMEOUT`` which is
timeout for cache key to expire

default value is

.. code-block:: python

    CACHE_ACTIVE_URL_TIMEOUT = 60 * 60 * 24 # 1 day

and the last one configurable option is ``CACHE_ACTIVE_URL_PREFIX`` which is
by defaults ``django_activeurl.`` - its cache key prefix, for skipping issues
with similar keys in your backend

tests
*****

.. code-block:: console

    git clone https://github.com/hellysmile/django-activeurl.git
    cd django-activeurl
    virtualenv env
    source env/bin/activate
    pip install nose coverage
    python setup.py nosetests --with-coverage --cover-package='django_activeurl'

background
**********

for building HTML element tree ``django-activeurl`` uses
`lxml <http://pypi.python.org/pypi/lxml/>`_, which is one of the best HTML
parsing tools,more info and benchmarks can be found at
`habrahabr.ru <http://habrahabr.ru/post/163979/>`_ (in russian)

notes
*****

``django-activeurl`` supports python 2.5, 2.6, 2.7, 3.2, 3.3 and pypy 1.9

`initializr <http://www.initializr.com/>`_ is used for example html template

nice one "fork me" `solution <https://github.com/simonwhitaker/github-fork-ribbon-css>`_
