from mice import (
    Game,
    WorldBuilder,
)

import snake.components
import snake.resources
import snake.systems


Game(WorldBuilder(), (720, 480)).start()