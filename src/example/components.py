from dataclasses import dataclass

from mice import register


@register
@dataclass
class Grid:
    size: float


@register
class DebugView:
    ...
