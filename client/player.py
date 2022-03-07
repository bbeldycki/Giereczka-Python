import pygame
from entity import Entity
from settings import *


class Player(Entity):
    def __init__(self, position, groups, obstacle_sprites):
        super().__init__(groups)
        # graphics setup
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
        self.actual_position = list(position)
        self.next_position = self.actual_position
        self.image = self.animations[self.facing_direction + '_idle'][0]
        self.rect = self.image.get_rect(topleft=self.actual_position)

        # player attack
        self.attacking = False
        self.attack_cooldown = 2000
        self.attack_time = 0

        # obstacles
        self.obstacle_sprites = obstacle_sprites

    def import_player_assets(self):
        player_catalog = 'graphics/Player/'
        for animation in self.animations.keys():
            full_path = player_catalog + animation
            self.animations[animation] = import_all_images_from_catalog(full_path)

    def input(self):
        # function to check if we will move or we just want to look in another direction
        def check_if_moving_or_changing_direction():
            if keys[pygame.K_RCTRL] or keys[pygame.K_LCTRL]:
                self.is_moving = False
            else:
                self.is_moving = True

        # all keys that we can get
        keys = pygame.key.get_pressed()

        if self.direction.x == 0 and self.direction.y == 0:
            self.is_moving = False
        # movement input
        if keys[pygame.K_UP]:
            self.direction.y = -1
            self.facing_direction = 'up'
            check_if_moving_or_changing_direction()
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
            self.facing_direction = 'down'
            check_if_moving_or_changing_direction()
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.facing_direction = 'left'
            check_if_moving_or_changing_direction()
        elif keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.facing_direction = 'right'
            check_if_moving_or_changing_direction()
        else:
            self.direction.x = 0
            self.direction.y = 0

    def try_to_move(self):
        if self.is_moving:
            if self.direction.x != 0:
                self.next_position[0] = int(self.actual_position[0] + self.direction.x)
            elif self.direction.y != 0:
                self.next_position[1] = int(self.actual_position[1] + self.direction.y)

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False

    def animate(self):
        if self.is_moving:
            animation = self.animations[self.facing_direction]
            # loop over frame index
            self.frame_index += self.animation_speed
            if self.frame_index >= len(animation):
                self.frame_index = 0
            self.image = animation[int(self.frame_index)]
            self.image = pygame.transform.rotozoom(animation[int(self.frame_index)], 0, 2)
            self.rect = self.image.get_rect(center=self.rect.center)
        else:
            animation = self.animations[self.facing_direction + '_idle']
            self.image = animation[0]
            self.image = pygame.transform.rotozoom(animation[0], 0, 2)
            self.rect = self.image.get_rect(center=self.rect.center)

    def update(self):
        self.input()
        self.try_to_move()
        # self.cooldowns()
        self.animate()

