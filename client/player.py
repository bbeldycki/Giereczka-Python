import pygame
from entity import EntitySprite
from settings import *


class Player(EntitySprite):
    def __init__(self, entity, color=(0, 0, 255)):
        super().__init__(entity=entity, color=color)



