import pygame

from typing import Any, MutableMapping


class Window:
    def __init__(self, width: int, height: int):
        self.display = pygame.display.set_mode((width, height))


class Image:

    _cache: MutableMapping[str, Any] = {}

    def __init__(self, path: str):
        img = self._cache.get(path, None)
        if img is None:
            img = pygame.image.load(path)
            self._cache[path] = img
        self.img = img
        self.rect = self.img.get_rect()
