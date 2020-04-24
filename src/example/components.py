from dataclasses import dataclass

from mice import component


@component
@dataclass
class Grid:
    size: float


@component
class DebugView:
    ...
