from mice import system
from mice.common.components import Window

from ..components import GridPosition, Grid, GameState, Snake


@system()
class KillPlayer:

    def create(self):
        self.player_pos = self.resources.player[Snake].head
        self.x_limit = self._pos_limit(
            self.resources.game[Grid].size,
            self.resources.window[Window].width)
        self.y_limit = self._pos_limit(
            self.resources.game[Grid].size,
            self.resources.window[Window].height)

    def _pos_limit(self, grid_size, screen_size) -> int:
        return screen_size//grid_size


    def update(self):
        if self.resources.game[GameState].state == "running":
            if self.player_pos.x >= self.x_limit:
                self._end_game()
            elif self.player_pos.y >= self.y_limit:
                self._end_game()
            elif self.player_pos.x < 0:
                self._end_game()
            elif self.player_pos.y < 0:
                self._end_game()
        yield

    def _end_game(self):
        print("Player died")
        self.resources.game[GameState].state = "end"