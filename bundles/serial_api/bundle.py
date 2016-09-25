class SerialApiBundle(object):
    def __init__(self):
        self.config_mapping = {
            "serial_api": {
                "port": "/dev/ttyUSB0",
                "speed": 115200

            }
        }

