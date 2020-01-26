=========
Changelog
=========

Here you can find the recent changes to django-activeurl

0.2.0 January 26th, 2020
------------------------

- Add support for Django 3.0, `#44`_, thanks `@meloncafe`_!
- Drop support for Django versions less than 2.2, `#48`_
- Travis improvements, sort imports, remove python 3.3/3.4, `#45`_

.. _#44: https://github.com/hellysmile/django-activeurl/pull/44
.. _@meloncafe: https://github.com/meloncafe
.. _#45: https://github.com/hellysmile/django-activeurl/pull/45
.. _#48: https://github.com/hellysmile/django-activeurl/pull/48

0.1.12 February 16, 2018
------------------------

- Ignore href="#" to fix incompatibilities with bootstrap.
  This matches <= 0.1.9 behaviour.

0.1.11 October 10, 2017
-----------------------

- ignore_params now works with menu="no"

0.1.10 July 28, 2017
--------------------

- Changelog started
- Added ``ignore_params`` for matching patterns with GET parameters.

  e.g. */path/* will match */path/?param=value*

  To enable this, add ``ignore_params="yes"`` to your ``{% activeurl %}``
  tag::

      {% activeurl ignore_params="yes" %}
