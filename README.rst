=============================
event_email
=============================

.. image:: https://badge.fury.io/py/event-email.svg
    :target: https://badge.fury.io/py/event-email

.. image:: https://travis-ci.org/narnikgamarnikus/event-email.svg?branch=master
    :target: https://travis-ci.org/narnikgamarnikus/event-email

.. image:: https://codecov.io/gh/narnikgamarnikus/event-email/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/narnikgamarnikus/event-email

App for email marketing for CohoEvents

Documentation
-------------

The full documentation is at https://event-email.readthedocs.io.

Quickstart
----------

Install event_email::

    pip install event-email

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'event_email.apps.EventEmailConfig',
        ...
    )

Add event_email's URL patterns:

.. code-block:: python

    from event_email import urls as event_email_urls


    urlpatterns = [
        ...
        url(r'^', include(event_email_urls)),
        ...
    ]

Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
