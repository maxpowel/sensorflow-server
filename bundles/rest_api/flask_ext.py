from flask import Response
from serializer import serializer


def serialize(response_object, _format=None):
    if _format is None:
        _format = serializer.default_format()

    return Response(serializer.dumps(response_object, _format), mimetype=serializer.mimetype(_format))


def unserialize(data, model, content_type):
    _format = serializer.content_type_format(content_type)
    if _format is None:
        _format = serializer.default_format()
    return serializer.loads(data, model, _format)
