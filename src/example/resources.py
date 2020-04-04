from mice import WorldBuilder
from example.components import Grid, DebugView


def add_resources(w: WorldBuilder):
    add_grid_resource(w)


GRID_RES_NAME = "GRID"


def add_grid_resource(w: WorldBuilder):
    w.add_resource(GRID_RES_NAME, [Grid(100), DebugView()])
