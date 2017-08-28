=====
Usage
=====

To use event_email in a project, add it to your `INSTALLED_APPS`:

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
