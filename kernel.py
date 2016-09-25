import logging
import inject

import mapped_config.loader
from abc import ABCMeta, abstractmethod


# This class is only used for an friendly injection of configuration
class Configuration(object):
    pass


class Environments(object):
    DEVELOPMENT = "dev"
    PRODUCTION = "prod"
    TEST = "test"


class Kernel(metaclass=ABCMeta):

    config_file = "config.yml"

    def __init__(self, environment):
        self.logger = None
        self.bundles = self.register_bundles()

        try:
            self.configuration = self.load_configuration(environment)
            # Set this kernel and configuration available for injection
            inject.configure(lambda binder: binder
                             .bind(Kernel, self)
                             .bind(Configuration, self.configuration)
                             )
        except FileNotFoundError as e:
            logging.exception(e)
            raise e

        self.configure_logger(environment=environment)
        self.logger.info("Kernel started")


    def configure_logger(self, environment):
        # Get root logger
        self.logger = logging.getLogger(self.__class__.__name__)
        root_logger = logging.getLogger('')
        if environment == Environments.DEVELOPMENT:
            logging.basicConfig(level=logging.DEBUG)
            self.logger.setLevel(logging.DEBUG)
            root_logger.setLevel(logging.DEBUG)

            # Console output
            ch = logging.StreamHandler()
            ch.setLevel(logging.DEBUG)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            ch.setFormatter(formatter)
            # Remove the default handlers
            del root_logger.handlers[:]
            root_logger.addHandler(ch)
            root_logger.info("Console Handler Ready")
        elif environment == Environments.PRODUCTION:
            pass
            # Fluent output
            # fluent_config = self.configuration.fluent
            # h = handler.FluentHandler('fonio', host=fluent_config.host, port=fluent_config.port)
            # # formatter = handler.FluentRecordFormatter(custom_format)
            # formatter = handler.FluentRecordFormatter()
            # h.setFormatter(formatter)
            # h.setLevel(logging.DEBUG)
            # root_logger.addHandler(h)
            # root_logger.info("Fluentd configuration ready")
        self.logger.info("Logger initialized")

    @abstractmethod
    def register_bundles(self):
        pass

    def load_configuration(self, environment):
        mappings = [bundle.config_mapping for bundle in self.bundles if hasattr(bundle, "config_mapping")]
        c = mapped_config.loader.YmlLoader()
        #path.dirname(path.realpath(__file__))
        config = c.load_config("/home/alvaro/sensorflow-server/config/{config}".format(config=self.config_file), "/home/alvaro/sensorflow-server/config/parameters.yml")
        try:
            config = c.build_config(config, mappings)
        except mapped_config.loader.NoValueException as ex:
            print("Configuration error: " + str(ex))
            exit()
        except mapped_config.loader.NodeIsNotConfiguredException as ex:
            print("Configuration error: " + str(ex))
            exit()
        except mapped_config.loader.IgnoredFieldException as ex:
            print("Configuration error: " + str(ex))
            exit()

        return config
