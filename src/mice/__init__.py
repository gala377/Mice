# flake8: noqa

__version__ = "0.1.0"


import pygame_plugin.components
import pygame_plugin.systems

from ecs.component import Component
from ecs.genid import GenId
from ecs.entity import Entity

from libmice.systems.abc import System

from mice.game import Game
from mice.world_builder import WorldBuilder

from libmice.autoregister import component, resource, register
from libmice.systems.func import system, resource_system
