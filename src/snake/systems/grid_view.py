import pygame

from mice import system
from mice.common.components import Window

from ..components import Grid

@system()
class GridDebugView:

    def create(self):
        self.window = self.resources.window[Window]
        self.grid = self.resources.world_grid[Grid]

    def update(self):
        for i in range((self.window.height // self.grid.size) + 1):
                pygame.draw.line(
                    self.window.display,
                    (0, 255, 0),
                    (0, i * self.grid.size),
                    (self.window.width, i * self.grid.size),
                )
        for i in range((self.window.width // self.grid.size) + 1):
            pygame.draw.line(
                self.window.display,
                (0, 0, 255),
                (i * self.grid.size, 0),
                (i * self.grid.size, self.window.height),
            )
        yield