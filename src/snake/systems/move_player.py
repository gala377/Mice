import pygame
import sys

from copy import copy

from mice import system
from mice.common.components import Time

from ..components import (
    GridPosition,
    Grid,
    GameState,
    Snake,
    MoveDirection,
)


@system()
class MovePlayer:

    ONE_MOVE_PER = 0.1

    def create(self):
        self.player = self.resources.player[Snake]
        self.grid_size = self.resources.game[Grid].size
        self.timer = self.resources.timer[Time]
        self._time = 0
        self.direction = MoveDirection.RIGHT
        self.game_state = self.resources.game[GameState]
        self.last_direction = self.direction
        self.buffered_direction = self.direction

    def update(self):
        if self.game_state.state == "running":
            self._move_player()
            self._read_direction()
        yield

    def _move_player(self):
        self._time += self.timer.delta
        if self._time > self.ONE_MOVE_PER:
            self.last_direction = self.direction
            self.direction = self.buffered_direction
            if self.direction == MoveDirection.LEFT:
                self.player.head.x -= 1
            elif self.direction == MoveDirection.RIGHT:
                self.player.head.x += 1
            elif self.direction == MoveDirection.UP:
                self.player.head.y -= 1
            elif self.direction == MoveDirection.DOWN:
                self.player.head.y += 1
            self._shift_snake()
            self._time = 0

    def _shift_snake(self):
        self.player.grid_positions = [copy(self.player.head)] + self.player.grid_positions[:-1]

    def _read_direction(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.last_direction != MoveDirection.RIGHT:
            self.buffered_direction = MoveDirection.LEFT
            return
        if keys[pygame.K_RIGHT] and self.last_direction != MoveDirection.LEFT:
            self.buffered_direction = MoveDirection.RIGHT
            return
        if keys[pygame.K_UP] and self.last_direction != MoveDirection.DOWN:
            self.buffered_direction = MoveDirection.UP
            return
        if keys[pygame.K_DOWN] and self.last_direction != MoveDirection.UP:
            self.buffered_direction = MoveDirection.DOWN
            return
