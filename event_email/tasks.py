from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from .models import Email, Schedule
from celery.task import periodic_task
from django.core.mail import send_mail
from celery import shared_task
from django_celery_beat.models import PeriodicTask, IntervalSchedule
import json
from django.core.mail import EmailMessage

@shared_task
def send_event_mail(html, text, subject, sender, recipients):
	#send_mail(
	#	subject,
	#	html,
	#	sender,
	#	recipients
	#	fail_silently=False,
	#	)
	mail = EmailMessage(
		subject,
		text,
		sender,
		recipients,
		fail_silently=False,
		)
	mail.attach_alternative(html, "text/html")
	mail.send()


@receiver(post_save, sender=Schedule)
def schedule_task(sender, instance, created, **kwargs):
	if created:
		if instance.sending_frequency == 'One time':
			send_event_mail.delay(
				html = instance.email_template.html,
				text = instance.email_template.text,
				subject = instance.email_template.subject,
				sender = instance.user.email,
				recipients = [r for r in instance.recipients.all()],
				)
		else:
			if instance.sending_frequency == 'Daily':
				period = 1
			elif instance.sending_frequency == 'Weekly':
				period = 7
			elif instance.sending_frequency == 'Monthly':
				period = 30
			else instance.sending_frequency == 'Yearly':
				period = 365

			schedule, created = IntervalSchedule.objects.get_or_create(
				every=period,
				period=IntervalSchedule.DAYS,
				)
			PeriodicTask.objects.create(
				interval=schedule,
				name='sending event email {}'.format(instance.pk),
				task='event_email.tasks.send_event_email',
				args=json.dumps([
					instance.email_template.html,
					instance.email_template.text,
					instance.email_template.subject,
					instance.user.email,
					[r for r in instance.recipients.all()],
					]),
				kwargs=json.dumps({
					'be_careful': True,
					}),
				expires=None,
				)




