from mice import resource

from .components import *


@resource
class Player:

    components = [
        Snake([
            GridPosition(0, 0),
            GridPosition(0, 1),
            GridPosition(0, 2),
        ], GridPosition(0, 0)),
        SquareSprite((255, 255, 255), 20),
    ]


@resource
class Game:

    components = [
        GameState(),
        Grid(20),
    ]