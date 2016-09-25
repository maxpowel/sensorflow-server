from protobuf3.message import Message
from protobuf3.fields import FloatField, MessageField, Int32Field, StringField


class Command(Message):
    pass


class Status(Message):
    pass


class RgbLed(Message):
    pass


class Sensor(Message):
    pass


class SensorList(Message):
    pass


class Pin(Message):
    pass


class PinStatus(Message):
    pass

Command.add_field('command', Int32Field(field_number=1, required=True))
Status.add_field('code', Int32Field(field_number=1, required=True))
RgbLed.add_field('red', Int32Field(field_number=1, required=True))
RgbLed.add_field('green', Int32Field(field_number=2, required=True))
RgbLed.add_field('blue', Int32Field(field_number=3, required=True))
Sensor.add_field('name', StringField(field_number=1, required=True))
Sensor.add_field('values', FloatField(field_number=2, repeated=True))
SensorList.add_field('sensors', MessageField(field_number=1, repeated=True, message_cls=Sensor))
Pin.add_field('name', Int32Field(field_number=1, required=True))
PinStatus.add_field('pin', MessageField(field_number=1, required=True, message_cls=Pin))
PinStatus.add_field('status', MessageField(field_number=2, required=True, message_cls=Status))
