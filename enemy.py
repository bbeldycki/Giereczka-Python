import math

import pygame

from settings import *
from entity import Entity


class Enemy(Entity):
    def __init__(self, position, enemy_name, enemy_type, groups, obstacle_sprites):
        # general setup
        super().__init__(groups)
        self.sprite_type = 'enemy'
        self.position = position
        self.enemy_name = enemy_name
        self.enemy_type = enemy_type

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
        self.import_enemy_graphics(self.enemy_name)
        self.image = self.animations[self.facing_direction + '_idle'][0]
        self.rect = self.image.get_rect(topleft=self.position)

        # movement
        self.obstacle_sprites = obstacle_sprites

        # stats
        self.stats = monsters['enemy1']
        self.health = self.stats['health']
        self.experience = self.stats['experience']
        self.speed = self.stats['speed']

    def import_enemy_graphics(self, name):
        enemy_catalog = f'graphics/Enemy/{name}/'
        for animation in self.animations.keys():
            full_path = enemy_catalog + animation
            self.animations[animation] = import_all_images_from_catalog(full_path)

    def get_player_distance_and_direction(self, player):
        enemy_vector = pygame.math.Vector2(self.rect.center)
        player_vector = pygame.math.Vector2(player.rect.center)
        distance = (player_vector - enemy_vector).magnitude()
        if distance > 0:
            direction = (player_vector - enemy_vector).normalize()
            return distance, direction
        else:
            direction = pygame.math.Vector2()
            return distance, direction

    def get_status(self, player):
        distance_to_player = self.get_player_distance_and_direction(player)[0]
        if distance_to_player <= self.stats['spot_radius']:
            self.is_moving = True
            self.direction = self.get_player_distance_and_direction(player)[1]
            if self.direction.y == -1:
                self.facing_direction = 'up'
            elif self.direction.y == 1:
                self.facing_direction = 'down'
            elif self.direction.x == -1:
                self.facing_direction = 'left'
            elif self.direction.x == 1:
                self.facing_direction = 'right'
        else:
            self.is_moving = False
            self.direction = pygame.math.Vector2()

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
        self.move(self.speed)
        self.animate()

    def enemy_update(self, player):
        self.get_status(player)
