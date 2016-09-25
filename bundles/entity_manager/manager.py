from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from kernel import Configuration, Kernel
from contextlib import contextmanager
import inject

Base = declarative_base()


class EntityManager(object):
    @inject.params(configuration=Configuration)
    def __init__(self, configuration):
        config = configuration.entity_manager
        uri = "{driver}://{username}{password}@{host}/{database}?charset=utf8".format(
            driver=config.driver,
            username=config.username,
            password=":"+str(config.password) if config.password is not None else "",
            host=config.hostname,
            database=config.database
        )

        engine = create_engine(uri, echo=config.debug, pool_recycle=60)
        self.engine = engine

        session_factory = sessionmaker(bind=engine, autocommit=False, autoflush=False)
        self.Session = scoped_session(session_factory)
        # Register mappings
        kernel = inject.instance(Kernel)
        for bundle in kernel.bundles:
            if hasattr(bundle, "register_entities"):
                getattr(bundle, "register_entities")()

    def session(self):
        return self.Session()

    @property
    @contextmanager
    def one_use_session(self):
        try:
            yield self.Session()
        finally:
            self.Session.remove()

    def generate_schema(self):
        Base.metadata.create_all(self.engine)
