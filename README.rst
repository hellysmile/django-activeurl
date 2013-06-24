django-activeurl
================

:info: Easy to use active url highlighting for django

.. image:: https://api.travis-ci.org/hellysmile/django-activeurl.png
    :target: https://travis-ci.org/hellysmile/django-activeurl
.. image:: https://coveralls.io/repos/hellysmile/django-activeurl/badge.png?branch=master
    :target: https://coveralls.io/r/hellysmile/django-activeurl?branch=master
.. image:: https://pypip.in/d/django-activeurl/badge.png
    :target: https://pypi.python.org/pypi/django-activeurl
.. image:: https://pypip.in/v/django-activeurl/badge.png
    :target:: https://pypi.python.org/pypi/django-activeurl

live demo is available on `heroku.com <http://django-activeurl.herokuapp.com/>`_

features
********

* automatic highlighting currently active ``<a>`` tags via css class
* automatic highlighting up-level ``<a>`` tags for menus
* removes boring\hardcoded stuff from your life!

usage
*****

load template library

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


if ``request.get_full_path()`` starts with  ``/some_page/``

content of ``{% activeurl %}{% endactiveurl %}`` must have valid root tag,
like ``<ul>`` or ``<div>``, etc - otherwise an exception will be raised

installation
************

install the ``stable version`` using ``pip``

.. code-block:: console

    pip install django-activeurl

or install the ``in-development version`` using ``pip``

.. code-block:: console

    pip install -e git+git://github.com/hellysmile/django-activeurl#egg=django_activeurl


modify ``settings.py``

add ``'django_activeurl'`` to ``INSTALLED_APPS``

add ``'django.core.context_processors.request'`` to ``TEMPLATE_CONTEXT_PROCESSORS``

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

successful ``lxml`` building requires some system stuff eg:

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

mac os x
--------

.. code-block:: console

    brew install libxml2 libxslt
    sudo update_dyld_shared_cache -force


windows
-------

pre build lxml binary can found here `here <http://www.lfd.uci.edu/~gohlke/pythonlibs/>`_

clouds
------

99.99% thats ``lxml`` will build out from the box

configuration
*************

there is two different way to determine "active" status

* starts with logic (``request.get_full_path()`` starts with ``<a>`` ``href``)

useful for menus/submenus, like

.. code-block:: html+django

    {% activeurl menu="yes" parent_tag="div" %}
        <div>
            <div>
                <a href="/menu/">
                    menu
                </a>
                <div>
                    <a href="/menu/submenu/">
                        submenu
                    </a>
                </div>
            </div>
        </div>
    {% endactiveurl %}

when ``<a>`` with ``href="/menu/"`` needs to be marked as "active"
if ``request.get_full_path()`` is ``/menu/submenu/`` or ``href="/menu/"``

* equals logic (``request.get_full_path()`` equals ``href``)

example

.. code-block:: html+django

    {% activeurl menu="no" parent_tag="div" %}
        <div>
            <div>
                <a href="/menu/">
                    menu
                </a>
            </div>
            <div>
                <a href="/menu/submenu/">
                    submenu
                </a>
            </div>
        </div>
    {% endactiveurl %}

menu
----

so ``menu`` is one of configuration options which can be passed to template tag,
which means support menus layout or not

parent_tag
----------

``parent_tag`` in previous example is ``<div>``, means which what parent element
of ``<a>``, needs to be marked as "active"

css_class
---------

``css_class`` means what css class needs to be added to parent element

by default these values are

.. code-block:: html+django

    {% activeurl css_class="active" parent_tag="li" menu="yes" %}
        ...
    {% endactiveurl %}

they can be changed in ``settings.py``

.. code-block:: python

    ACTIVE_URL_KWARGS = {
        'css_class': 'active',
        'parent_tag': 'li',
        'menu': 'yes'
    }

any one of this options can be skipped

if "active" status needs be applied direct to ``<a>``, just

.. code-block:: html+django

    {% activeurl parent_tag="self" css_class="current" %}
        <div>{# do not forget valid html root tag #}
            <a href="/some_page/">
                some_page
            </a>
        </div>
    {% endactiveurl %}

will be rendered to

.. code-block:: html

    <div>
        <a href="/some_page/" class="current">
            some_page
        </a>
    </div>

root/index links
----------------

``<a>`` with ``href='/'`` will be processed only with disabled ``menu`` support,
otherwise it will be always "active", exmaple

.. code-block:: html+django

    {% activeurl menu='no' %}
        <ul>
            <li>
                <a href="/">
                    home
                </a>
            </li>
        </ul>
    {% endactiveurl %}

performance
***********

there is no rebuilding content of template tag when no "active" urls found

by default ``ACTIVE_URL_CACHE`` is ``True``, so before building HTML tree,
searching "active" urls, ``django-activeurl`` will try to get
previously rendered HTML from django cache backend

caching can be disabled in ``settngs.py``

.. code-block:: python

    ACTIVE_URL_CACHE = False

in addition can be set ``ACTIVE_URL_CACHE_TIMEOUT`` which is
timeout for cache key to expire, default value is

.. code-block:: python

    ACTIVE_URL_CACHE_TIMEOUT = 60 * 60 * 24  # 1 day

and the last one configurable option is ``ACTIVE_URL_CACHE_PREFIX`` which is
by defaults ``django_activeurl`` - it is django cache backend prefix

tests
*****

.. code-block:: console

    pip install tox
    tox

jinja2
******

plain `jinja2 <https://github.com/mitsuhiko/jinja2>`_ configuration

.. code-block:: jinja

    {% activeurl options(request, css_class="active", menu="yes", parent_tag="li") %}
        <ul>
            <li>
                <a href="/page/">page</a>
            </li>
            <li>
                <a href="/other_page/">other_page</a>
            </li>
        </ul>
    {% endactiveurl %}

.. code-block:: python

    from jinja2 import Environment

    from django_activeurl.ext.django_jinja import ActiveUrl
    from django_activeurl.ext.utils import options

    env = Environment(
        extensions=[ActiveUrl]
    )
    env.globals['options'] = options

for `django-jinja <https://github.com/niwibe/django-jinja>`_,
`jingo <https://github.com/jbalogh/jingo>`_,
`coffin <https://github.com/coffin/coffin/>`_ extension and global function
needs to be loaded in ``settings.py```

background
**********

for building HTML element tree ``django-activeurl`` uses
`lxml <http://pypi.python.org/pypi/lxml/>`_, which is one of the best HTML
parsing tools,more info and benchmarks can be found at
`habrahabr.ru <http://habrahabr.ru/post/163979/>`_ (in russian)

notes
*****

``django-activeurl`` supports python 2.6, 2.7, 3.2, 3.3 and pypy 1.9

`initializr <http://www.initializr.com/>`_ is used for example html template

nice one "fork me" `solution <https://github.com/simonwhitaker/github-fork-ribbon-css>`_
