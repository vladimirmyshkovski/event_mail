# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-28 11:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event_email', '0003_emailtemplate_html'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailtemplate',
            name='text',
            field=models.CharField(default='', max_length=2000, verbose_name='Text'),
            preserve_default=False,
        ),
    ]
