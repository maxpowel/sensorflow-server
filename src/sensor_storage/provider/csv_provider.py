
from .provider import StorageProvider
import datetime


class SqlAlchemyStorageProvider(StorageProvider):

    def push(self, sensor_data):
        name = str(sensor_data["name"])
        value = str(sensor_data["value"])
        quantity_name = str(sensor_data["quantity"])
        with open("data.csv", "a") as myfile:
                myfile.write(",".join([str(datetime.datetime.now()), name, value, quantity_name]))
                myfile.write("\n")
