from typing import Tuple, Sequence

import random

from mice import system
from mice.common.components import Window

from snake.components import *


@system()
class SpawnFood:

    def create(self):
        self.player = self.resources.player[Snake]
        self.grid = self.resources.game[Grid]
        self.game_state = self.resources.game[GameState]
        self.window = self.resources.window[Window]

    def update(self):
        if self.game_state.spawn_food:
            pos = self._rand_pos()
            self.entity_storage.create_entity(
                Food(),
                SquareSprite((255, 255, 255), self.grid.size),
                pos)
            self.game_state.spawn_food = False
        yield

    def _rand_pos(self) -> GridPosition:
        choices = self._possible_pos_choices()
        (x, y) = random.choice(choices)
        return GridPosition(x, y)

    def _possible_pos_choices(self) -> Sequence[Tuple[int, int]]:
        choices = []
        for x in range(self.window.width//self.grid.size):
            for y in range(self.window.height//self.grid.size):
                for gp in self.player.grid_positions:
                    if gp.x == x and gp.y == y:
                        break
                else:
                    choices.append((x, y))
        return choices
        
