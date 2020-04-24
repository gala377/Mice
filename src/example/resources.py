from mice import resource
from mice.common.components import Image, Transform

from example.components import Grid, DebugView


@resource
class grid:
    components = [Grid(25), DebugView()]


@resource
class ball:
    components = [Image("resources/intro_ball.gif"), Transform(0, 0)]
