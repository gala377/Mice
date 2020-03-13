from typing import Any
from dataclasses import dataclass

# A marker class
Component = Any


@dataclass
class Transform:
    x: float
    y: float
