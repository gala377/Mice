from typing import Tuple

from mice import system
from mice.common.components import Window

from ..components import (
    SquareSprite,
    GridPosition,
    Grid,
)

import pygame

@system(GridPosition, SquareSprite)
class DrawSquares:

    def create(self):
        self.window = self.resources.window[Window]
        self.grid = self.resources.game[Grid]

    def update(self):
        for pos, square in self.components:
            rect = self._square_to_pygame_rect(pos, square)
            pygame.draw.rect(
                self.window.display,
                square.color,
                rect)
        yield

    def _square_to_pygame_rect(self, pos, square):
        in_dsp_pos = self._get_in_display_pos(pos.x, pos.y)
        rect = pygame.Rect(
            in_dsp_pos[0],
            in_dsp_pos[1],
            square.size,
            square.size)
        return rect

    def _get_in_display_pos(self, x: float, y: float) -> float:
        return (
            self.grid.size * x,
            self.grid.size * y) 

