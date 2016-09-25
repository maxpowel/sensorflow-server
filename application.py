import inject
from kernel import Environments, Kernel
from bundles.rest_api.kernel import FlaskKernel
import bundles.entity_manager.bundle
import bundles.rest_api.bundle
import src.sensor_storage.bundle

from bundles.entity_manager.manager import EntityManager
import logging


class AppKernel(FlaskKernel):
    def register_bundles(self):
        bundle_list = [
            bundles.rest_api.bundle.RestApiBundle(),
        ]

        return bundle_list

kernel = AppKernel(Environments.DEVELOPMENT)
kernel.run()
# em = inject.instance(EntityManager)
#
# session1 = em.session
#
# with em.one_use_session as session:
#     logging.debug("hola")

# em.generate_schema()

