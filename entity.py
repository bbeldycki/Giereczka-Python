import pygame
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

    def move(self, speed):
        if self.is_moving:
            if self.direction.magnitude() != 0:
                self.direction = self.direction.normalize()

            self.rect.x += self.direction.x * speed
            self.collision('horizontal')
            self.rect.y += self.direction.y * speed
            self.collision('vertical')

    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(self.rect):
                    # case we moving right
                    if self.direction.x > 0:
                        self.rect.right = sprite.rect.left
                    # case we moving left
                    if self.direction.x < 0:
                        self.rect.left = sprite.rect.right
        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(self.rect):
                    # case we moving down
                    if self.direction.y > 0:
                        self.rect.bottom = sprite.rect.top
                    # case we moving up
                    if self.direction.y < 0:
                        self.rect.top = sprite.rect.bottom