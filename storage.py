import inject

from kernel import Environments
from bundles.rest_api.kernel import FlaskKernel
from bundles.rest_api.bundle import RestApiBundle
from bundles.web_ui.bundle import WebUiBundle
from bundles.entity_manager.bundle import EntityManagerBundle
from sensorflow import sensorflow
from flask_apscheduler import APScheduler
from src.sensor_storage.bundle import SensorStorageBundle


class AppKernel(FlaskKernel):
    config_file = "storage_config.yml"

    def __init__(self, environment):
        super().__init__(environment)
        self.sf = sensorflow.Sensorflow(
            source=sensorflow.SerialSource(port="/dev/ttyUSB0"),
            serializer=sensorflow.JsonSerializer()
        )

    def register_bundles(self):
        bundles = [
            EntityManagerBundle(),
            RestApiBundle(),
            WebUiBundle(),
            SensorStorageBundle()
        ]

        return bundles

    def run(self):
        # Start the scheduler
        # scheduler = BackgroundScheduler()
        # scheduler.add_job(tick, 'interval', seconds=10)
        # scheduler.start()
        scheduler = APScheduler()
        #self.application.config.from_object(Config())
        self.application.config["SCHEDULER_VIEWS_ENABLED"] = True
        self.application.config["JOBS"] = [
            {
                'id': 'sensor_read',
                'func': 'src.sensor_storage.jobs:sensor_read',
                # 'args': (1, 2),
                'trigger': 'interval',
                'seconds': 10
            }
        ]
        scheduler.init_app(self.application)
        for rule in self.application.url_map.iter_rules():
            print(rule)
        scheduler.start()
        super().run()


kernel = AppKernel(Environments.DEVELOPMENT)
kernel.run()
