import inject
from .provider import StorageProvider
from ..entity import Sensor, Magnitude
from entity_manager.manager import EntityManager
from sqlalchemy.orm.exc import NoResultFound


class SqlAlchemyStorageProvider(StorageProvider):
    @inject.params(entity_manager=EntityManager)
    def __init__(self, entity_manager):
        self.em = entity_manager

    def push(self, sensor_data):
        with self.em.one_use_session as session:
            session.add(sensor_data)
            session.commit()
            return sensor_data.id

    # def push(self, sensor_name, values):
    #     sensor = self.get_sensor(sensor_name)
    #     if sensor is None:
    #         sensor = self.create_sensor(sensor_name)
    #
    #     for value in values:
    #         magnitude = self.get_magnitude(value[""])
    #
    # def get_sensor(self, name):
    #     with self.em.session() as session:
    #         try:
    #             return session.query(Sensor).filter(Sensor.name == name).one()
    #         except NoResultFound:
    #             return None
    #
    # def get_magnitude(self, name):
    #     with self.em.session() as session:
    #         try:
    #             return session.query(Magnitude).filter(Magnitude.name == name).one()
    #         except NoResultFound:
    #             return None
    #
    # def create_sensor(self, name):
    #     sensor = Sensor(name=name)
    #     if not isinstance(magnitudes, list):
    #         magnitudes = [magnitudes]
    #
    #     for magnitude_name in magnitudes:
    #         magnitude = self.get_magnitude(magnitude_name)
    #         if magnitude is None:
    #             magnitude = Magnitude(name=magnitude_name)
    #

