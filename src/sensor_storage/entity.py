from entity_manager.manager import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import relationship
import datetime


class Sensor(Base):
    __tablename__ = 'sensor'

    id = Column(String(36), primary_key=True)
    name = Column(String(255))


class Magnitude(Base):
    __tablename__ = 'sensor_magnitude'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))


class SensorMeasure(Base):
    __tablename__ = 'sensor_measure'

    id = Column(Integer, primary_key=True)
    value = Column(Numeric(precision=16, scale=8))
    sensor_id = Column(String(36), ForeignKey('sensor.id'), nullable=False)
    sensor = relationship("Sensor")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    magnitude_id = Column(Integer, ForeignKey('sensor_magnitude.id'), nullable=False)
    magnitude = relationship("Magnitude")
