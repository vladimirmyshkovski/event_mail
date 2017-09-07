import json
from django.core.serializers.json import DjangoJSONEncoder

class PixelJSONSerializer(object):
	"""Allows datetime.datetime encoding."""

	def dumps(self, obj):
		return json.dumps(obj, cls=DjangoJSONEncoder)

	def loads(self, obj):
		return json.loads(obj)