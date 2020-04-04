from dataclasses import dataclass

from mice_common.autoregister import register


@register
@dataclass
class Grid:
    size: float


@register
class DebugView:
    ...
