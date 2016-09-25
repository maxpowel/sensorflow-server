import inject
import requests
import json

from kernel import Environments, Kernel
from bundles.entity_manager.bundle import EntityManagerBundle

from apscheduler.schedulers.blocking import BlockingScheduler

def tick():
    r = requests.get("http://localhost:3003/read")
    payload = json.loads(r.text)
    with open("data.csv", "a") as myfile:
        for sensor in payload["data"]:
            myfile.write(",".join([str(sensor["name"]), str(sensor["value"]), str(sensor["quantity"])]))
            myfile.write("\n")

class AppKernel(Kernel):
    config_file = "storage_config.yml"

    def register_bundles(self):
        bundles = [
            EntityManagerBundle(),
            #src.sensor_storage.bundle.SensorStorageBundle(),
        ]

        return bundles

    def run(self):
        # Start the scheduler
        scheduler = BlockingScheduler()
        scheduler.add_job(tick, 'interval', seconds=10)
        scheduler.start()


kernel = AppKernel(Environments.DEVELOPMENT)
kernel.run()
# em = inject.instance(EntityManager)
#
# session1 = em.session
#
# with em.one_use_session as session:
#     logging.debug("hola")

# em.generate_schema()

