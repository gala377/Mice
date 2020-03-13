import pygame


class Window:
    def __init__(self, width: int, height: int):
        self.window = pygame.display.set_mode((width, height))
