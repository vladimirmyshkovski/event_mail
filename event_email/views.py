# -*- coding: utf-8 -*-
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    UpdateView,
    ListView,
    RedirectView,
)

from .models import (
    Email,
    EmailTemplate,
    Recipient,
    Schedule
)

from django.http import HttpResponse
from django.views.decorators.http import require_GET
from django.views.decorators.cache import cache_control
from .utils import decode_pixel
from annoying.functions import get_object_or_None

from .forms import EmailTemplateForm
from django.core.files import File


class EmailCreateView(CreateView):

    model = Email
    fields = '__all__'


class EmailDeleteView(DeleteView):

    model = Email


class EmailDetailView(DetailView):

    model = Email


class EmailUpdateView(UpdateView):

    model = Email


class EmailListView(ListView):

    model = Email


class EmailTemplateCreateView(CreateView):

    model = EmailTemplate
    fields = ['subject', 'template_name', 'html']


class EmailTemplateDeleteView(DeleteView):

    model = EmailTemplate


class EmailTemplateDetailView(DetailView):

    model = EmailTemplate
    fields = ['subject', 'template_name', 'html']


class EmailTemplateUpdateView(UpdateView):

    model = EmailTemplate
    fields = ['subject', 'template_name', 'html']


class EmailTemplateListView(ListView):

    model = EmailTemplate


class ScheduleCreateView(CreateView):

    model = Schedule
    fields = '__all__'


class ScheduleDeleteView(DeleteView):

    model = Schedule


class ScheduleDetailView(DetailView):

    model = Schedule


class ScheduleUpdateView(UpdateView):

    model = Schedule


class ScheduleListView(ListView):

    model = Schedule


class RecipientCreateView(CreateView):

    model = Recipient
    fields = '__all__'


class RecipientDeleteView(DeleteView):

    model = Recipient


class RecipientDetailView(DetailView):

    model = Recipient


class RecipientUpdateView(UpdateView):

    model = Recipient


class RecipientListView(ListView):

    model = Recipient


class RecipientSubscribeView(RedirectView):

    model = Recipient


class RecipientUnsubscribeView(RedirectView):

    model = Recipient


@cache_control(max_age=0, no_cache=True, no_store=True, must_revalidate=True)
@require_GET
def tracking_pixel(request, tracking_pixel):
    """Decode tracking pixel request, return 204 No Content HTTP header
    decode_pixel verifies authenticity of pixel and fires off a Django
    signal with the data encoded in the pixel url.
    Returns a 204 No Content http response to save bandwidth.
    """
    '''
    email = get_object_or_None(Email, token=token)
    if email:
        email.status = 'Opened'
        email.save()
    '''
    decode_pixel(tracking_pixel)
    return HttpResponse(status=204)