from flask import Blueprint, jsonify
import inject
import kernel
from sensorflow import sensorflow

index_blueprint = Blueprint(
    'index', __name__
)

@index_blueprint.route("/", methods=['GET'])
def index_get_index():
    return jsonify({"Hello": "World"})

@index_blueprint.route("/read", methods=['GET'])
def read_get_index():
    kernel_intance = inject.instance(kernel.Kernel)
    return jsonify(kernel_intance.sensorflow.sensor_read())

class RestApiBundle(object):
    def __init__(self):
        self.config_mapping = {
            "rest_api": {
                "use_debugger": True,
                "port": 3003

            }
        }

        self.blueprints = [index_blueprint]

