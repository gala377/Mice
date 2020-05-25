from typing import Tuple

from mice import system
from mice.systems import not_none
from mice.common.components import Window

from ..components import (
    Snake,
    GridPosition,
    Grid,
)

import pygame

@system()
class DrawSnake:

    def create(self):
        self.window = self.resources.window[Window]
        self.grid = self.resources.game[Grid]
        self.snake = self.resources.player[Snake]

    def update(self):
        for pos in self.snake.grid_positions:
            rect = self._square_to_pygame_rect(pos)
            pygame.draw.rect(
                self.window.display,
                (255, 255, 255),
                rect)
        yield

    def _square_to_pygame_rect(self, pos):
        in_dsp_pos = self._get_in_display_pos(pos.x, pos.y)
        rect = pygame.Rect(
            in_dsp_pos[0],
            in_dsp_pos[1],
            self.grid.size,
            self.grid.size)
        return rect

    def _get_in_display_pos(self, x: float, y: float) -> float:
        return (
            self.grid.size * x,
            self.grid.size * y) 
