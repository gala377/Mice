from ecs.system import GeneratorSystem

from libmice.autoregister import register
from libmice.common.components import Time


@register
class UpdateTime(GeneratorSystem):
    def __iter__(self):
        timer = self.resources.timer[Time]
        timer.update()
        yield None
        while True:
            timer.update()
            yield None
