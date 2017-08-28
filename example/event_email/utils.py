import string
import random
import json
from django.core import signing
from django.core.signing import BadSignature, SignatureExpired
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.dateparse import parse_datetime
from .signals import pixel_data
import logging


logger = logging.getLogger(__name__)


def token_generator(size=50, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))


def event_email_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/<instance.template_name.html>
    return '{}.html'.format(instance.template_name)


def dont_track(request):
    """Do not send tracking pixel when certain http headers exist."""

    http_x_purpose = request.META.get("HTTP_X_PURPOSE", "").strip().lower()
    http_x_moz = request.META.get("HTTP_X_MOZ", "").strip().lower()
    prefetch_qs_arg = request.GET.get("prefetch", None)
    dnt = int(request.META.get("HTTP_DNT", 0))
    return bool(
        any(x in http_x_purpose for x in ("prerender", "preview", "instant")) or
        ("prefetch" in http_x_moz) or
        prefetch_qs_arg or
        dnt
        )


def decode_pixel(tracking_pixel):
    """Decode tracking pixel data and publish as Django signal.
    The tracking pixel data is encoded in the pixel template tag
    (.templatetags.pixel.pixel) using Django's signing functionality.
    tracking_pixel is verified and the timestamp checked, so no unauthorized
    or expired data will be processed.
    Tracking pixel data is broadcast to the pixel_data signal (signals.py),
    which can be subscribed to by any other apps within the site. Current
    example of signal processing can be found in models.py.
    """

    pixel = None
    print('TRACKING PIXEL: ' + str(tracking_pixel))
    try:
        pixel = signing.loads(tracking_pixel)
        print(pixel)
    except SignatureExpired:
        logger.exception("pixel expired")
    except BadSignature:
        logger.exception("pixel invalid")
        print('PIXEL AFTER DECODE :' + str(pixel))
    print(pixel)
    if json.loads(pixel, compress=True):
        pixel['timestamp'] = parse_datetime(pixel['timestamp'])
        pixel_data.send(sender='decode_pixel', pixel_data=pixel)