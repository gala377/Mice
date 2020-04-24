# flake8: noqa

from typing import Tuple, Sequence

from mice import (
    Game,
    WorldBuilder,
)

# imports needed for autoregister to kick in
import example.components
import example.systems
import example.resources


def main():
    w = WorldBuilder()
    game = Game(w, (720, 480))
    game.start()


if __name__ == "__main__":
    main()
