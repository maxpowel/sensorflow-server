from kernel import Kernel
from src.sensor_storage.storage import StorageManager
import inject


def greet():
    print("Hi!")


def sensor_read():
    m = inject.instance(StorageManager)
    kernel = inject.instance(Kernel)
    payload = kernel.sf.sensor_read()
    for sensor in payload["data"]:
        m.push(sensor)
