from django.contrib import admin
from .models import (
					EmailTemplate,
					Email,
					Schedule,
					Recipient
					)

admin.site.register(Email)
admin.site.register(EmailTemplate)
admin.site.register(Schedule)
admin.site.register(Recipient)