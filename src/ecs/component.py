import time

from typing import Any
from dataclasses import dataclass

# A marker class
Component = Any


@dataclass
class Transform:
    x: float
    y: float


@dataclass
class Time:

    delta: float = 0
    last_frame: float = 0

    def update(self):
        if self.last_frame == 0:
            self.last_frame = time.time()
        now = time.time()
        self.delta = now - self.last_frame
        self.last_frame = now
