import pygame

from typing import (
    Tuple,
    Sequence,
)

from mice import (
    Game,
    system,
    resource_system,
)
from mice.common.components import Transform

from example.components import (
    Grid,
    DebugView,
)


@system(Grid, DebugView)
class GridView:

    window_name: str
    grid_name: str

    default_args = [Game.WINDOW_RES, "grid"]

    def __init__(self, wn: str, gn: str):
        super().__init__()
        self.window_name = wn
        self.grid_name = gn

    def create(self):
        [self.window] = self.resources[self.window_name].components

    def update(self):
        for grid, _ in self.components:
            for i in range((self.window.height // grid.size) + 1):
                pygame.draw.line(
                    self.window.display,
                    (0, 255, 0),
                    (0, i * grid.size),
                    (self.window.width, i * grid.size),
                )
            for i in range((self.window.width // grid.size) + 1):
                pygame.draw.line(
                    self.window.display,
                    (0, 0, 255),
                    (i * grid.size, 0),
                    (i * grid.size, self.window.height),
                )
        yield None
