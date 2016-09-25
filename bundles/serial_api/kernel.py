import kernel
import serial
import json
import inject
import logging
from src.sensor_storage.storage import StorageManager
from sensorflow import sensorflow
import time



class SerialKernel(kernel.Kernel):
    def __init__(self, environment):
        super().__init__(environment=environment)
        config = self.configuration.serial_api
        source = sensorflow.SerialSource(port=config.port, baudrate=config.speed)
        serializer = sensorflow.JsonSerializer()
        self.sensorflow = sensorflow.Sensorflow(source=source, serializer=serializer)
        self.sensors = {}
        self.quantities = {}
        self.sync()
        print(self.sensors)
        print(self.quantities)



    def sync(self):
        self.write({"command": "info"})
        response = self.read()
        for sensor_data in response:
            sensor = {
                "sensor": sensor_data["sensor"],
                "quantities": [d["name"] for d in sensor_data["quantities"]]
            }
            self.sensors[sensor_data["name"]] = sensor
            for d in sensor_data["quantities"]:
                if d["id"] not in self.quantities:
                    self.quantities[d["id"]] = d["name"]

    def run(self):
        run = True
        storage = inject.instance(StorageManager)
        logging.info("Press Ctrl + c to stop")
        while run:
            try:

                self.serial.write(json.dumps({"command": "read"}).encode("utf-8"))
                line = self.serial.readline().decode('utf-8')
                message = json.loads(line)
                if message["error"]:
                    logging.error(message)
                else:
                    for i in message["data"]:
                        sensor_name = i["name"]
                        if i["multiple"]:
                            values = i["values"]
                        else:
                            values = [i["value"]]

                        sensor_info = self.sensors[sensor_name]

                        measures = zip(sensor_info["quantities"], values)

                        for magnitude, value in measures:
                            logging.info({"name": sensor_name, "value": values, "magnitude": magnitude})
                            # measure = SensorMeasure()
                            # measure.magnitude_id = 1
                            # measure.sensor_id = 1
                            # measure.value = value
                            #
                            # storage.push(measure)

                time.sleep(3)
            except KeyboardInterrupt:
                logging.info("Stopping...")
                run = False

        self.serial.close()
        logging.info("Bye")

