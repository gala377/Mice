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

    delta: float
    last_frame: float

    def update_delta(self):
        now = time.time()
        self.delta = now - self.last_frame
        self.last_frame = now
