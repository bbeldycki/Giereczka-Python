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

        self.rect.centerx = self.position[0]
        self.rect.centery = self.position[1]

    def move(self, speed) -> None:
        # Movement
        if speed != (0, 0):
            self.stats['moving'] = True

            new_position = (self.entity['position'][0] + speed[0],
                            self.entity['position'][1] + speed[1])

            self.entity['position'] = new_position

            if speed[0] > 0:
                self.entity['direction'] = 'right'
            else:
                self.entity['direction'] = 'left'

            if speed[1] > 0:
                self.entity['direction'] = 'down'
            else:
                self.entity['direction'] = 'up'
        else:
            self.stats['moving'] = False

        self.rect.x = self.entity['position'][0]
        self.rect.y = self.entity['position'][1]
