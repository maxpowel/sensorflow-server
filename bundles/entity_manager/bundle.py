
class EntityManagerBundle(object):
    def __init__(self):
        self.config_mapping = {
            "entity_manager": {
                "driver": None,
                "debug": False,
                "username": "root",
                "hostname": "localhost",
                "password": "",
                "database": None,
                "port": None

            }
        }

