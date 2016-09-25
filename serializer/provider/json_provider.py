from .provider import SerializerProvider
import simplejson
import inspect
import datetime


class JsonProvider(SerializerProvider):
    def dumps(self, model_object):
        return simplejson.dumps(obj=model_object, cls=CustomTypeEncoder)

    def loads(self, data, model_class):
        return model_class(**simplejson.loads(data))

    mimetype = "application/json"


def simple_class_encoder(python_object):
    return {
        attr: getattr(python_object, attr) for attr in dir(python_object) if
        getattr(python_object, attr) is not None and
        not inspect.ismethod(getattr(python_object, attr)) and
        not attr.startswith("_") and
        not inspect.isfunction(getattr(python_object, attr))
        }


# Si se quieren encoders especificos (algo mas que simplemente las propiedades no nulas) meterlos aqui tal como
# serializer.encoderHandlers.update({Response: serializer.simpleClassEncoder})
# Donde se especifica la clase (Response en ese caso) y la funcion
encoderHandlers = {}


def datetime_handler(datetime_object):
    return datetime_object.isoformat()

encoderHandlers[datetime.datetime] = datetime_handler


class CustomTypeEncoder(simplejson.JSONEncoder):
    def default(self, obj):
        handler = encoderHandlers.get(obj.__class__)
        if handler is not None:
            return handler(obj)
        return simple_class_encoder(obj)



