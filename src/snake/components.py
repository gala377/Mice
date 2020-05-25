from typing import Tuple, MutableSequence
from dataclasses import dataclass
from enum import Enum

from mice import component


@component
@dataclass
class Grid:
    size: float
    

@component
@dataclass
class GridPosition:
    x: int
    y: int


@component
@dataclass
class SquareSprite:
    color: Tuple[int, int, int]
    size: float


@component
@dataclass
class GameState:
    state: str = "running"
    spawn_food: bool = True



@component
@dataclass
class Snake:

    grid_positions: MutableSequence[GridPosition]
    head: GridPosition


@component
class Food: ...


class MoveDirection(Enum):
    UP = 0;
    RIGHT = 1;
    DOWN = 2;
    LEFT = 3;

@component
@dataclass
class AttempedMove:
    direction: MoveDirection = MoveDirection.RIGHT