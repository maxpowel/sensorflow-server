import kernel
from flask import Flask
from flask.json import JSONEncoder
import datetime

class CustomJSONEncoder(JSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        return JSONEncoder.default(self, obj)


class FlaskKernel(kernel.Kernel):
    config_file = "api_config.yml"

    def __init__(self, environment):
        super().__init__(environment=environment)
        app = Flask("Sensorflow")
        app.json_encoder = CustomJSONEncoder
        self.application = app

        for bundle_blueprints in [bundle.blueprints for bundle in self.bundles if hasattr(bundle, "blueprints")]:
            for blueprint in bundle_blueprints:
                app.register_blueprint(blueprint)

    def run(self):
        self.application.run(use_debugger=False, port=3003)
