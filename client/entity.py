from settings import *


class Entity(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.direction = pygame.math.Vector2()
        self.frame_index = 0
        self.animation_speed = 0.2

        # entity movement status
        self.is_moving = False

        # facing direction
        self.facing_direction = 'down'
