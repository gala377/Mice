from mice_common.autoregister import resource
from mice_common.components import Time


@resource
class timer:
    components = [Time()]
