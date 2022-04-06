from settings import *
import pygame


class EntitySprite(pygame.sprite.Sprite):
    def __init__(self, entity, color=(0, 255, 0)):
        pygame.sprite.Sprite.__init__(self)
        self.entity = entity
        self.id = self.entity['id']
        self.position = self.entity['position']
        self.speed = pygame.math.Vector2()
        self.direction = self.entity['direction']
        self.stats = self.entity['stats']

        self.image = pygame.Surface((64, 64))
        self.foreground = None
        self.color = color
        self.rect = self.image.get_rect()

        self.rect.centerx = self.position[0]
        self.rect.centery = self.position[1]

    def update(self):
        # Movement
        if self.speed != (0, 0):
            self.stats['moving'] = True

            new_position = (self.entity['position'][0] + self.speed[0],
                            self.entity['position'][1] + self.speed[1])

            self.entity['position'] = new_position

            if self.speed[0] > 0:
                self.entity['direction'][0] = 1
            else:
                self.entity['direction'][0] = -1

            if self.speed[1] > 0:
                self.entity['direction'][1] = 1
            else:
                self.entity['direction'][1] = -1
        else:
            self.stats['moving'] = False

        self.rect.x = self.entity['position'][0]
        self.rect.y = self.entity['position'][1]
