# -*- coding: utf-8
from __future__ import unicode_literals, absolute_import

import django

DEBUG = True
USE_TZ = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "r&@rc8i3lyxjwv-zy6u+npy9(@j9@!pqaehquy-7r0jd9ov=&l"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

ROOT_URLCONF = "tests.urls"

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sites",
    "event_email",
    "geoposition", # https://github.com/philippbosch/django-geoposition
    "anymail", # https://github.com/anymail/django-anymail
    #"django-celery-beat", # https://github.com/celery/django-celery-beat 
]



SITE_ID = 1

if django.VERSION >= (1, 10):
    MIDDLEWARE = ()
else:
    MIDDLEWARE_CLASSES = ()

GEOPOSITION_GOOGLE_MAPS_API_KEY = 'AIzaSyBO-_WYrcSrU79tLuKPiINGkCJ1e__RWWw'


ANYMAIL = {
    # (exact settings here depend on your ESP...)
    "MAILGUN_API_KEY": "<your Mailgun key>",
    "MAILGUN_SENDER_DOMAIN": 'mg.example.com',  # your Mailgun domain, if needed
}
EMAIL_BACKEND = "anymail.backends.mailgun.EmailBackend"  # or sendgrid.EmailBackend, or...
DEFAULT_FROM_EMAIL = "you@example.com"  # if you don't already have this in settings