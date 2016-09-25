from .provider.json_provider import JsonProvider


handlers = {
    'json': JsonProvider()
}


def mimetype(_format):
    return handlers[_format].mimetype

def content_type_format(content_type):
    for _format, handler in handlers.items():
        if handler.mimetype == content_type:
            return _format



def default_format():
    return 'json'


def dumps(model_object, _format=None):
    if _format is None:
        _format = default_format()

    return handlers[_format].dumps(model_object)


def loads(data, model_class, _format=None):
    if _format is None:
        _format = default_format()

    return handlers[_format].loads(data, model_class)
