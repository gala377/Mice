from typing import (
    Mapping,
    Sequence,
    Any,
)

from ecs.system import GeneratorSystem

from mice_common.autoregister import register


@register
class UpdateTime(GeneratorSystem):

    res_name: str
    default_args: Sequence[Any] = ["timer"]
    default_kwargs: Mapping[str, Any] = {}

    def __init__(self, res_name: str):
        super().__init__()
        self.res_name = res_name

    def __iter__(self):
        [timer] = self.resources[self.res_name].components
        timer.update()
        yield None
        while True:
            timer.update()
            yield None
