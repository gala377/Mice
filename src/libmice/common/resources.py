from libmice.autoregister import resource
from libmice.common.components import Time


@resource
class timer:
    components = [Time()]
