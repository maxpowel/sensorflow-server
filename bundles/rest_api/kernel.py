import kernel
from flask import Flask
import inject
from sensorflow import sensorflow




class FlaskKernel(kernel.Kernel):
    config_file = "api_config.yml"
    def __init__(self, environment):
        super().__init__(environment=environment)
        app = Flask("Sensorflow")
        self.application = app

        for bundle_blueprints in [bundle.blueprints for bundle in self.bundles if hasattr(bundle, "blueprints")]:
            for blueprint in bundle_blueprints:
                app.register_blueprint(blueprint)

        self.sensorflow = sensorflow.Sensorflow(source=sensorflow.SerialSource(), serializer=sensorflow.JsonSerializer())

    def run(self):
        self.application.run(use_debugger=False, port=3003)
