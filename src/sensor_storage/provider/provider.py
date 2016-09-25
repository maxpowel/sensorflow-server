from abc import ABCMeta, abstractmethod


class StorageProvider(metaclass=ABCMeta):
    @abstractmethod
    def push(self, sensor_data):
        pass

    # @abstractmethod
    # def get_sensor(self, name):
    #     pass