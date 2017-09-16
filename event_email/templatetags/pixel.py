from django.utils import timezone
from django import template
from django.core import signing
from ..utils import dont_track
import json


register = template.Library()


@register.inclusion_tag('event_email/pixel.html', takes_context=True)
def pixel(context):
    """Generate tracking pixel for single object.
    Context data is encoded as a url-safe, signed, timestamped hash value
    that is then used as the url for a png image request (see views.py).
    Function is set to respect a browser's "Do Not Track" setting.
    """

    pixel = None
    if context.get('object', None):
        token = None
        if context['object'].__class__.__name__ == 'Email':
            email = get_object_or_None(Email, pk=context['object'].id)
            token = email.token 
        data = {
            "path": context['request'].get_full_path(),
            "content_type": context['object'].__class__.__name__,
            "content_id": context['object'].id,
            "timestamp": timezone.now().isoformat(), #.strftime('%Y %m %d %H:%M:%S'),
            "token": token,
        }

        pixel = signing.dumps(
            json.dumps(data, separators=(',', ':')), compress=True)
    if dont_track(context['request']):
        pass
    else:
        return {
            'pixel_url': pixel
            }