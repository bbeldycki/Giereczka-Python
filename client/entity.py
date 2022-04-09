from settings import *
import pygame


class EntitySprite(pygame.sprite.Sprite):
    def __init__(self, entity, color=(0, 255, 0)) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.entity = entity
        self.color = color
        self.id = self.entity['id']
        self.position = self.entity['position']
        self.direction = self.entity['direction']
        self.stats = self.entity['stats']
        self.frame_index = 0  # TODO change in the future
        self.animation_speed = 0.2  # TODO change in the future

        self.image = pygame.Surface((SIZE, SIZE))
        self.rect = self.image.get_rect()
        self.rect.centerx = self.position[0]
        self.rect.centery = self.position[1]

    def move(self, speed) -> None:
        # Movement
        if self.stats['moving']:
            if self.direction == 'down':
                self.entity['position'][1] = self.entity['position'][1] + speed
            elif self.direction == 'up':
                self.entity['position'][1] = self.entity['position'][1] - speed
            if self.direction == 'right':
                self.entity['position'][0] = self.entity['position'][0] + speed
            elif self.direction == 'left':
                self.entity['position'][0] = self.entity['position'][0] - speed

        self.rect.x = self.entity['position'][0]
        self.rect.y = self.entity['position'][1]
