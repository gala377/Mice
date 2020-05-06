from mice import resource

from .components import *

@resource
class WorldGrid:

    components = [
        Grid(20),
    ]


@resource
class Player:

    components = [
        GridPosition(0, 0),
        SquareSprite((255, 255, 255), 10),
    ]