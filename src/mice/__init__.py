# flake8: noqa

__version__ = "0.1.0"


from ecs.component import Component
from ecs.system import System

from mice.game import Game
from mice.world_builder import WorldBuilder

from mice_common.autoregister import system, component, resource, register
