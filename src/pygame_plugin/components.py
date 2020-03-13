import pygame


class Window:
    def __init__(self, width: int, height: int):
        self.display = pygame.display.set_mode((width, height))


class Image:
    def __init__(self, path: str):
        self.img = pygame.image.load(path)
        self.rect = self.img.get_rect()
