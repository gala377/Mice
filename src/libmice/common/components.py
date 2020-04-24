import time

from dataclasses import dataclass

from libmice.autoregister import component


@component
@dataclass
class Transform:
    x: float
    y: float


@component
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
