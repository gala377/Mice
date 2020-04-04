from typing import Iterator
import pygame

from mice import Game
from mice import system
from mice.system_helpers import GeneratorSystem, RunningSystem

from example.components import Grid, DebugView


@system
class GridView(GeneratorSystem):

    window_name: str
    grid_name: str

    default_args = [Game.WINDOW_RES, "grid"]

    def __init__(self, wn: str, gn: str):
        super().__init__()
        self.window_name = wn
        self.grid_name = gn

    @property
    def grids(self) -> Iterator[Grid]:
        grids_to_draw = zip(self.entity_storage[Grid], self.entity_storage[DebugView])
        grids_to_draw = filter(all, grids_to_draw)
        for grid, _ in grids_to_draw:
            if grid is not None:
                yield grid

    def __iter__(self) -> RunningSystem:
        [window] = self.resources[self.window_name].components
        yield None
        while True:
            for grid in self.grids:
                for i in range((window.height // grid.size) + 1):
                    pygame.draw.line(
                        window.display,
                        (0, 255, 0),
                        (0, i * grid.size),
                        (window.width, i * grid.size),
                    )
                for i in range((window.width // grid.size) + 1):
                    pygame.draw.line(
                        window.display,
                        (0, 0, 255),
                        (i * grid.size, 0),
                        (i * grid.size, window.height),
                    )
            yield None
