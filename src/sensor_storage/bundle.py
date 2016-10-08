from flask import Blueprint, jsonify
import inject
from src.sensor_storage.storage import StorageManager
import datetime

index_blueprint = Blueprint(
    'storage', __name__, url_prefix="/storage"
)



@index_blueprint.route("/", methods=['GET'])
def index_get_index():
    storage = inject.instance(StorageManager)
    return jsonify({
        "localdate": datetime.datetime.now().isoformat(),
        "date": datetime.datetime.utcnow().isoformat(),
        "count": {
            "total": storage.count(),
            "by_sensor": storage.count(grouped=True)
        }
    })


@index_blueprint.route("/list", methods=['GET'])
def list_get_index():
    storage = inject.instance(StorageManager)
    return jsonify({"elements": storage.query()})


class SensorStorageBundle(object):
    def __init__(self):
        self.blueprints = [index_blueprint]
