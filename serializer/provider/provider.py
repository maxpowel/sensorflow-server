from abc import ABCMeta, abstractmethod, abstractproperty


class SerializerProvider(metaclass=ABCMeta):
    @abstractmethod
    def dumps(self, model_object):
        pass

    @abstractmethod
    def dumps(self, data, model_class):
        pass

    @abstractproperty
    def mimetype(self):
        pass
