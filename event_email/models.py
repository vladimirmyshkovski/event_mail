# -*- coding: utf-8 -*-

from django.db import models

from django.conf import settings

from model_utils.models import TimeStampedModel
from model_utils.fields import StatusField, MonitorField
from model_utils import Choices

from django.utils.encoding import python_2_unicode_compatible

from django.utils.translation import ugettext_lazy as _
from geoposition.fields import GeopositionField
from django.utils.translation import get_language

from django.utils.functional import cached_property
from django.utils import timezone
from django.core.urlresolvers import reverse
import uuid

from pprint import pprint
from django.dispatch import receiver
from .signals import pixel_data
from .utils import event_email_directory_path
from django.core.files import File
from bs4 import BeautifulSoup
import os
from django.utils.safestring import mark_safe

@python_2_unicode_compatible
class Event(TimeStampedModel):
	pass


@python_2_unicode_compatible
class EmailTemplate(TimeStampedModel):
	
	source = models.FileField(blank=True
	)
	template_name = models.CharField(verbose_name=_('Name of template'), 
		max_length=50,
		unique=True
	)
	html = models.CharField(verbose_name=_('HTML'),
		max_length=2000,
	)
	text = models.CharField(verbose_name=_('Text'),
		max_length=2000,
		blank=True
	)
	subject = models.CharField(verbose_name=_('Subject'), 
		max_length=50
	)

	def get_absolute_url(self):
		return reverse('event_email:EmailTemplate_detail', 
			kwargs={'pk': self.pk})

	def save(self, *args, **kwargs):
		# Read the html
		soup = BeautifulSoup(self.html, "html.parser")
		# Convert to text and set it to the field 
		self.text = soup.get_text()
		# Check exist file in self.source
		if not self.source:
			# Write html with needed template tags 
			html = mark_safe(
					"""{% extends 'base_email.html' %}
				   	{% block content %} 
				   	{}
				   	{% endblock content %}
				   	""".format(self.html)
				   )
			# Create path
			file_path = event_email_directory_path(self, self.template_name)
			# Create new HTML file
			new_file = open(file_path, 'w+')
			# Write self.html to the new file
			new_file.write(html)
			# Convert file to Django file 
			new_file = File(new_file)
			# Remove old file from filesystem
			os.remove(file_path)
			# Set file to the filefield
			self.source = new_file
			# After set new file it exist in the directory 
		return super(EmailTemplate, self).save(*args, **kwargs)

	def __str__(self):
		return self.template_name

@python_2_unicode_compatible
class Recipient(TimeStampedModel):

	first_name = models.CharField(max_length=25)
	last_name = models.CharField(max_length=25)
	email_address = models.CharField(max_length=50)
	phone_number = models.CharField(max_length=20)
	location = GeopositionField()
	token = models.CharField(max_length=50)

	subscribe = models.BooleanField(default=False)

	def _subscribe_url(self):
		return reverse('event_email:subscribe',
			kwargs={'token': self.token})

	def _unsubscribe_url(self):
		return reverse('event_email:unsubscribe',
			kwargs={'token': self.token}) 

	def _subscribe(self):
		self.subscribe = True
		self.subscribe_date = timezone.now()

	def _unsubscribe(self):
		self.subscribe = False
		self.unsubscribe_date = timezone.now()

	@cached_property
	def full_name(self):
		return '{} {}'.format(
			self.first_name,
			self.last_name)

	@cached_property
	def address(self):
		return geocoder.google([
			self.location.latitude,
			self.location.longitude],
			method='reverse',
			language=get_language())

	def save(self, *args, **kwargs):
		self.first_name = self.first_name.capitalize()
		self.last_name = self.last_name.capitalize()

		if not self.token:
			self.token = uuid.uuid4().hex
		return super(Recipient, self).save(*args, **kwargs)

	def get_absolute_url(self):
		return reverse('event_email:Recipient_detail', 
			kwargs={'pk': self.pk})

	def __str__(self):
		return self.full_name


@python_2_unicode_compatible
class Schedule(TimeStampedModel):

	SENDING_FREQUENCY = Choices(
		_('One time'), _('Daily'), _('Weekly'), _('Monthly'), _('Yearly')
	)
	sending_frequency = StatusField(
		choices_name='SENDING_FREQUENCY',
		verbose_name=_('Frequency of sending')
	)
	recipients = models.ManyToManyField(
		'event_email.Recipient',
		verbose_name=_('Recipients')
	)
	email_template = models.ForeignKey('event_email.EmailTemplate',
		verbose_name=_('EmailTemplate')
	)
	complete = models.BooleanField(default=False,
		verbose_name=_('Complete')
	)

	def get_absolute_url(self):
		return reverse('event_email:Schedule_detail', 
			kwargs={'pk': self.pk})

@python_2_unicode_compatible
class Email(TimeStampedModel):
	STATUS = Choices(
		_('Created'), _('Sent'), _('Opened'), _('Clicked')
	)
	user = models.ForeignKey(settings.AUTH_USER_MODEL,
		related_name='event_email',
		verbose_name=_('User')
	)
	recipient = models.ForeignKey('event_email.Recipient', 
		verbose_name=_('Recipient')
	)
	event = models.ForeignKey(
		'event_email.Event', verbose_name=_('Event')
	)
	template = models.ForeignKey(
		'event_email.EmailTemplate', verbose_name=_('Email Template')
	) 
	schedule = models.ForeignKey(
		'event_email.Schedule', verbose_name=_('Schedule')
	)
	status = StatusField(verbose_name=_('Email status'))
	status_changed = MonitorField(monitor='status')

	sent_at = MonitorField(monitor='status',
		when=['Sent'],
		verbose_name=_('Email sent at')
	)
	opened_at = MonitorField(monitor='status',
		when=['Opened'],
		verbose_name=_('Email opened at')
	)
	clicked_at = MonitorField(monitor='status',
		when=['Clicked'],
		verbose_name=_('Email clicked at')
	)
	token = models.CharField(max_length=50)

	def save(self, *args, **kwargs):
		if not self.token:
			self.token = uuid.uuid4().hex
		return super(Recipient, self).save(*args, **kwargs)

	def get_absolute_url(self):
		return reverse('event_email:Email_detail', 
			kwargs={'pk': self.pk})

@receiver(pixel_data)
def example_receiver(**kwargs):
	"""Example receiver of pixel_data signal."""

	pixel_data = kwargs['pixel_data']
	pprint(pixel_data)