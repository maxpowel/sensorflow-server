import serial
import struct
import command

class ProtocolBuffersSerial(object):
    def __init__(self, port='/dev/ttyUSB0', baudrate=115200):
        self.ser = serial.Serial(
            port=port,
            baudrate=baudrate
        )

    def send(self, data_object):
        data = data_object.encode_to_bytes()
        size = len(data)
        self.ser.write(struct.pack("B", size))
        self.ser.write(data)

    def receive(self, data_object):
        response_size = struct.unpack("B", self.ser.read())
        data_object.parse_from_bytes(self.ser.read(response_size[0]))

    def close(self):
        self.ser.close()

class Nukebox(object):
    def __init__(self):
        self.ser = ProtocolBuffersSerial()
        self.c = command.Command()
        self.status = command.Status()

    def _command_query(self, command_number):
        self.c.command = command_number
        self.ser.send(self.c)
        self.ser.receive(self.status)
        if self.status.code != 0:
            raise Exception("Command not found")

    def led_color(self, red=0, green=0, blue=0):
        self._command_query(0)
        led = command.RgbLed()
        led.red = red
        led.green = green
        led.blue = blue
        self.ser.send(led)

    def digital_write(self, pin, value):
        self._command_query(2)
        # A0 es el 14
        pin_status = command.PinStatus()
        pin_status.pin.name = pin
        pin_status.status.code = value
        self.ser.send(pin_status)

    def sensor_data(self):
        self._command_query(1)
        sensor_list = command.SensorList()
        self.ser.receive(sensor_list)
        return sensor_list.sensors

    def close(self):
        self.ser.close()


nuke = Nukebox()
input("dale")
nuke.led_color(blue=199)
for i in nuke.sensor_data():
     print(i.name)
nuke.digital_write(10, 1)

nuke.close()
exit()
run = True
while run:
    try:
        valor = int(input("Numero"))
        c = command.Command()
        c.command = valor
        data = c.encode_to_bytes()
        # otro = command.Command()
        # otro.parse_from_bytes(data)
        size = len(data)
        print("ENVIANDO", size)

        ser.write(struct.pack("B", size))
        ser.write(data)

        response_size = struct.unpack("B", ser.read())
        print("RESPUSTA tamano", response_size)
        c.parse_from_bytes(ser.read(response_size[0]))
        print(c.command)


    except KeyboardInterrupt:
        run = False

ser.close()

