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
        self.position = position
        self.image = self.animations[self.facing_direction + '_idle'][0]
        self.rect = self.image.get_rect(topleft=self.position)

        # player attack
        self.attacking = False
        self.attack_cooldown = 2000
        self.attack_time = 0

        # obstacles
        self.obstacle_sprites = obstacle_sprites

        # stats
        self.stats = {
            'health': 100,
            'mana': 100,
            'exp': 100,
            'speed': 10
        }
        self.health = self.stats['health']
        self.mana = self.stats['mana']
        self.exp = 10
        self.speed = self.stats['speed']

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
        else:
            self.direction.y = 0

        if keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.facing_direction = 'left'
            check_if_moving_or_changing_direction()
        elif keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.facing_direction = 'right'
            check_if_moving_or_changing_direction()
        else:
            self.direction.x = 0
        # attack input
        if keys[pygame.K_SPACE] and not self.attacking:
            self.attacking = True
            self.attack_time = pygame.time.get_ticks()
        # magic input
        if keys[pygame.K_v] and not self.attacking:
            self.attacking = True
            self.attack_time = pygame.time.get_ticks()

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
        self.cooldowns()
        self.animate()
        self.move(self.speed)

