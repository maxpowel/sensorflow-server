from flask import Blueprint, jsonify

index_blueprint = Blueprint(
    'sensorflow_ui', __name__, url_prefix="/ui"
)

@index_blueprint.route("/", methods=['GET'])
def index_get_index():
    return "hola ahmigo"

#
# @index_blueprint.route("/read", methods=['GET'])
# def read_get_index():
#     kernel_intance = inject.instance(kernel.Kernel)
#     return jsonify(kernel_intance.sensorflow.sensor_read())

class WebUiBundle(object):
    def __init__(self):

        self.blueprints = [index_blueprint]

