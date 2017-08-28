from django.utils import timezone
from django import template
from django.core import signing
from ..utils import dont_track
from annoying.functions import get_object_or_None
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
            "timestamp": timezone.now(), #.strftime('%Y %m %d %H:%M:%S'),
            "token": token
        }

        print('DATA IS : ' + str(data))
        print('DATA JSON DUMPS : ' + str(json.dumps(data)))
        pixel = signing.dumps(json.dumps(data, separators=(',', ':')), compress=True)
        #pixel = signing.dumps(
        #    data, serializer=PixelJSONSerializer, compress=True)
        print('PIXEL AFTER SIGING :' + str(pixel))
    if dont_track(context['request']):
        print('dont track')
        print(pixel)
        return {
            'pixel_url': pixel
            }
        #pass
    else:
        return {
            'pixel_url': pixel
            }