from typing import Tuple
from dataclasses import dataclass

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