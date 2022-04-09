import pygame
from entity import EntitySprite
from settings import *


class Player(EntitySprite):
    def __init__(self, entity, color=(0, 0, 255)) -> None:
        super().__init__(entity=entity, color=color)
        self.animations = {
            'up': [],
            'down': [],
            'left': [],
            'right': [],
            'up_idle': [],
            'down_idle': [],
            'left_idle': [],
            'right_idle': []
        }
        self.import_player_assets()

        # player position and direction when appear on screen
        self.position = self.entity['position']
        self.speed = self.entity['stats']['movement_speed']
        self.image = self.animations[self.direction + '_idle'][0]
        self.rect = self.image.get_rect(topleft=self.position)

    def import_player_assets(self) -> None:
        player_catalog = 'graphics/Player/'
        for animation in self.animations.keys():
            full_path = player_catalog + animation
            self.animations[animation] = import_all_images_from_catalog(full_path)

    def input(self) -> None:
        # function to check if we will move or we just want to look in another direction
        def check_if_moving_or_changing_direction():
            if keys[pygame.K_RCTRL] or keys[pygame.K_LCTRL]:
                self.stats['moving'] = False
            else:
                self.stats['moving'] = True

        # all keys that we can get
        keys = pygame.key.get_pressed()

        # movement input
        if keys[pygame.K_UP]:
            self.direction = 'up'
            self.entity['direction'] = 'up'
            check_if_moving_or_changing_direction()
        elif keys[pygame.K_DOWN]:
            self.direction = 'down'
            self.entity['direction'] = 'down'
            check_if_moving_or_changing_direction()

        if keys[pygame.K_LEFT]:
            self.direction = 'left'
            self.entity['direction'] = 'left'
            check_if_moving_or_changing_direction()
        elif keys[pygame.K_RIGHT]:
            self.direction = 'right'
            self.entity['direction'] = 'right'
            check_if_moving_or_changing_direction()

    def animate(self) -> None:
        if self.stats['moving']:
            animation = self.animations[self.direction]
            # loop over frame index
            self.frame_index += self.animation_speed
            if self.frame_index >= len(animation):
                self.frame_index = 0
            self.image = animation[int(self.frame_index)]
            # self.image = pygame.transform.rotozoom(animation[int(self.frame_index)], 0, 2)
            self.rect = self.image.get_rect(center=self.rect.center)
        else:
            animation = self.animations[self.direction + '_idle']
            self.image = animation[0]
            # self.image = pygame.transform.rotozoom(animation[0], 0, 2)
            self.rect = self.image.get_rect(center=self.rect.center)

    def update(self) -> None:
        self.input()
        print(self.direction)
        self.animate()
        self.move(self.speed)
