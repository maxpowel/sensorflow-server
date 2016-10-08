from .provider.sql_alchemy_provider import SqlAlchemyStorageProvider
import inject


class StorageManager(object):
    def _get_default_provider(self):
        return SqlAlchemyStorageProvider
    def push(self, data_object, provider=None):
        if provider is None:
            # Pick default
            provider = self._get_default_provider()
        return inject.instance(provider).push(data_object)

    def count(self, provider=None, **kwargs):
        if provider is None:
            # Pick default
            provider = self._get_default_provider()
        return inject.instance(provider).count(kwargs)

    def query(self, provider=None, **kwargs):
        if provider is None:
            # Pick default
            provider = self._get_default_provider()
        return inject.instance(provider).query()
    # def get_sensor(self, name, provider=None):
    #     if provider is None:
    #         # Pick default
    #         provider = SqlAlchemyStorageProvider
    #     return inject.instance(provider).get_sensor(name)
