import pygame

from mice import system
from mice.common.components import Window

from example.components import (
    Grid,
    DebugView,
)


@system(Grid, DebugView)
class GridView:
    def create(self):
        self.window = self.resources.window[Window]

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
