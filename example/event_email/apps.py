# -*- coding: utf-8
from django.apps import AppConfig


class EventEmailConfig(AppConfig):
    name = 'event_email'
    import .tasks
    import .signals