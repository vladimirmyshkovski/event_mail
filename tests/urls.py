# -*- coding: utf-8
from __future__ import unicode_literals, absolute_import

from django.conf.urls import url, include

from event_email.urls import urlpatterns as event_email_urls

urlpatterns = [
    url(r'^', include(event_email_urls, namespace='event_email')),
]
