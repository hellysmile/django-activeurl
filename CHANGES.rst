=========
Changelog
=========

Here you can find the recent changes to django-activeurl

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
