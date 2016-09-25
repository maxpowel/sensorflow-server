import serial
from json.decoder import JSONDecodeError

# configure the serial connections (the parameters differs on the device you are connecting to)
ser = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=115200
)


# import time
# time.sleep(3)
import json
import struct
run = True
while run:
    try:

        input("Dale")
        ser.write(json.dumps({"command": "status"}).encode("utf-8"))
        line = ser.readline().decode('utf-8')
        print(line)
        ser.write(json.dumps({"command": "read"}).encode("utf-8"))
        line = ser.readline().decode('utf-8')
        print(line)
        input("DOLO")
  # buffer[0] = 'D';
  # buffer[1] = 'S';
  # buffer[2] = '1';
  # buffer[3] = '8';
  # buffer[4] = 'B';
  # buffer[5] = '2';
  # buffer[6] = '0';
  # buffer[7] = 0;
  # buffer[8] = 8;
  # buffer[9] = 0x28;
  # buffer[10] = 0xFF;
  # buffer[11] = 0x10;
  # buffer[12] = 0x93;
  # buffer[13] = 0x6F;
  # buffer[14] = 0x14;
  # buffer[15] = 0x4;
  # buffer[16] = 0x11;
  #
  # buffer[17] = 'D';
  # buffer[18] = 'S';
  # buffer[19] = '1';
  # buffer[29] = '8';
  # buffer[21] = 'B';
  # buffer[22] = '2';
  # buffer[23] = '0';
  # buffer[24] = 0;
  # buffer[25] = 8;
  # buffer[26] = 1;
  # buffer[27] = 2;
  # buffer[28] = 3;
  # buffer[29] = 4;
  # buffer[30] = 5;
  # buffer[31] = 6;
  # buffer[32] = 7;
  # buffer[33] = 8;
        sensor_type = "DS18B20"
        sensor_type_packed = struct.pack("{size}s".format(size=len(sensor_type)), bytes(sensor_type, 'ascii'))
        address = [0x28, 0xFF, 0x10, 0x93, 0x6F, 0x14, 0x4, 0x11]
        address_packed = struct.pack("8B", *address)
        # print(address)
        data = sensor_type_packed + struct.pack("BB", 0, len(address)) + address_packed
        # print(data)
        # print(len(data))
        print(json.dumps({"command": "writeConfig", "totalSensors": 1, "dataSize": len(data)}))
        ser.write(json.dumps({"command": "writeConfig", "totalSensors": 1, "dataSize": len(data)}).encode("utf-8"))
        ser.write(data)
        line = ser.readline().decode('utf-8')
        print(line)
        message = json.loads(line)
        print("FALLO" if message["error"] else "EXITO")
        # for i in message["data"]:
        #     print("Sensor:", i["name"])
        #     print("Valores", i["values"])

    except KeyboardInterrupt:
        run = False

ser.close()

