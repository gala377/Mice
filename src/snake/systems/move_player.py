import pygame
import sys

from enum import Enum

from mice import system
from mice.common.components import Time

from ..components import (
    GridPosition,
    Grid,
)


class MoveDirection(Enum):
    UP = 0;
    RIGHT = 1;
    DOWN = 2;
    LEFT = 3;

@system()
class MovePlayer:

    ONE_MOVE_PER = 0.1

    def create(self):
        self.player_pos = self.resources.player[GridPosition]
        self.grid_size = self.resources.world_grid[Grid].size
        self.timer = self.resources.timer[Time]
        self._time = 0
        self.direction = MoveDirection.RIGHT 

    def update(self):
        self._move_player()
        self._read_direction()
        yield

    def _move_player(self):
        self._time += self.timer.delta
        if self._time > self.ONE_MOVE_PER:
            if self.direction == MoveDirection.LEFT:
                self.player_pos.x -= 1
            elif self.direction == MoveDirection.RIGHT:
                self.player_pos.x += 1
            elif self.direction == MoveDirection.UP:
                self.player_pos.y -= 1
            elif self.direction == MoveDirection.DOWN:
                self.player_pos.y += 1
            self._time = 0

    def _read_direction(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.direction = MoveDirection.LEFT
        elif keys[pygame.K_RIGHT]:
            self.direction = MoveDirection.RIGHT
        elif keys[pygame.K_UP]:
            self.direction = MoveDirection.UP
        elif keys[pygame.K_DOWN]:
            self.direction = MoveDirection.DOWN