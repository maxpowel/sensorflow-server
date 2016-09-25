from .provider.sql_alchemy_provider import SqlAlchemyStorageProvider
import inject


class StorageManager(object):
    def push(self, data_object, provider=None):
        if provider is None:
            # Pick default
            provider = SqlAlchemyStorageProvider
        return inject.instance(provider).push(data_object)

    # def get_sensor(self, name, provider=None):
    #     if provider is None:
    #         # Pick default
    #         provider = SqlAlchemyStorageProvider
    #     return inject.instance(provider).get_sensor(name)
