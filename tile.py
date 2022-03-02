import pygame
from settings import *


class Tile(pygame.sprite.Sprite):
    def __init__(self, position, groups, sprite_type, surface=pygame.Surface((tilesize, tilesize))):
        super().__init__(groups)
        self.sprite_type = sprite_type
        self.image = surface
        self.rect = self.image.get_rect(topleft=position)

