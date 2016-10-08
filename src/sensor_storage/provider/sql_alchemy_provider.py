import inject
from .provider import StorageProvider
from bundles.entity_manager.manager import EntityManager
from sqlalchemy.orm.exc import NoResultFound

from bundles.entity_manager.manager import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import relationship
import datetime
import uuid
from sqlalchemy import func
from sqlalchemy import desc
import pytz

class Sensor(Base):
    __tablename__ = 'sensor'

    id = Column(String(36), primary_key=True)
    name = Column(String(255))


class Quantity(Base):
    __tablename__ = 'sensor_quantity'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))


class SensorMeasure(Base):
    __tablename__ = 'sensor_measure'

    id = Column(Integer, primary_key=True)
    value = Column(Numeric(precision=16, scale=8))
    sensor_id = Column(String(36), ForeignKey('sensor.id'), nullable=False)
    sensor = relationship("Sensor")
    created_at = Column(DateTime, default=datetime.datetime.utcnow())

    quantity_id = Column(Integer, ForeignKey('sensor_quantity.id'), nullable=False)
    quantity = relationship("Quantity")


class SqlAlchemyStorageProvider(StorageProvider):
    @inject.params(entity_manager=EntityManager)
    def __init__(self, entity_manager):
        self.em = entity_manager
        self.em.generate_schema()

    def push(self, sensor_data):
        with self.em.one_use_session as session:
            name = sensor_data["name"]
            value = sensor_data["value"]
            quantity_name = sensor_data["quantity"]
            try:
                sensor = session.query(Sensor).filter(Sensor.name == name).one()
            except NoResultFound:
                sensor = Sensor()
                sensor.name = name
                sensor.id = str(uuid.uuid4())
                session.add(sensor)
            
            try:
                quantity = session.query(Quantity).filter(Quantity.name == quantity_name).one()
            except NoResultFound:
                quantity = Quantity()
                quantity.name = quantity_name
                session.add(quantity)

            measure = SensorMeasure(quantity=quantity, sensor=sensor, value=value)
            session.add(measure)
            session.commit()

    def count(self, grouped=False):
        with self.em.one_use_session as session:
            if grouped:
                return [
                    c
                    for c in session
                    .query(
                        func.count(SensorMeasure.id).label("count"),
                        Sensor.name,
                        Quantity.name.label("quantity"),
                        func.max(SensorMeasure.value).label("max"),
                        func.min(SensorMeasure.value).label("min"),
                        func.avg(SensorMeasure.value).label("avg"),
                    )
                    .join(SensorMeasure.sensor)
                    .join(SensorMeasure.quantity)
                    .group_by(SensorMeasure.sensor_id, SensorMeasure.quantity_id)
                    .all()
                ]
            else:
                return session.query(func.count(SensorMeasure.id)).scalar()

    def query(self):
        with self.em.one_use_session as session:
            return session.query(SensorMeasure.created_at, Sensor.name, SensorMeasure.value, Quantity.name.label("quantity")).join(SensorMeasure.sensor).join(SensorMeasure.quantity).order_by(desc(SensorMeasure.created_at)).all()

    # def push(self, sensor_name, values):
    #     sensor = self.get_sensor(sensor_name)
    #     if sensor is None:
    #         sensor = self.create_sensor(sensor_name)
    #
    #     for value in values:
    #         quantity = self.get_quantity(value[""])
    #
    # def get_sensor(self, name):
    #     with self.em.session() as session:
    #         try:
    #             return session.query(Sensor).filter(Sensor.name == name).one()
    #         except NoResultFound:
    #             return None
    #
    # def get_quantity(self, name):
    #     with self.em.session() as session:
    #         try:
    #             return session.query(Quantity).filter(Quantity.name == name).one()
    #         except NoResultFound:
    #             return None
    #
    # def create_sensor(self, name):
    #     sensor = Sensor(name=name)
    #     if not isinstance(quantitys, list):
    #         quantitys = [quantitys]
    #
    #     for quantity_name in quantitys:
    #         quantity = self.get_quantity(quantity_name)
    #         if quantity is None:
    #             quantity = Quantity(name=quantity_name)
    #

