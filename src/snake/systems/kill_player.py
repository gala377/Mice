from mice import system
from mice.common.components import Window

from ..components import GridPosition, Grid


@system()
class KillPlayer:

    def create(self):
        self.player_pos = self.resources.player[GridPosition]
        self.x_limit = self._pos_limit(
            self.resources.world_grid[Grid].size,
            self.resources.window[Window].width)
        self.y_limit = self._pos_limit(
            self.resources.world_grid[Grid].size,
            self.resources.window[Window].height)

    def _pos_limit(self, grid_size, screen_size) -> int:
        return screen_size//grid_size


    def update(self):
        if self.player_pos.x >= self.x_limit:
            print("I died")
        if self.player_pos.y >= self.y_limit:
            print("I died")
        if self.player_pos.x < 0:
            print("I died")
        if self.player_pos.y < 0:
            print("I died")
        yield