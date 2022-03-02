from settings import *
from tile import Tile
from player import Player
from enemy import Enemy
from debug import debug
from magic import PlayerMagic
from ui import UI


class Level:
    def __init__(self):
        # get the display surface anywhere
        self.display_surface = pygame.display.get_surface()

        # sprite group setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        # player
        self.player = None
        self.player_magic = PlayerMagic()

        # sprite setup
        self.create_map()

        # user interface
        self.ui = UI()

    def create_map(self):
        layouts = {
            'boundary': import_csv_layout(get_path(catalog='map/map_data', file_name='ground_level_FloorBlocks.csv')),
            'entities': import_csv_layout(get_path(catalog='map/map_data', file_name='ground_level_Entities.csv'))
        }
        for style, layer in layouts.items():
            for row_index, row in enumerate(layer):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * tilesize
                        y = row_index * tilesize
                        if style == 'boundary':
                            Tile((x, y), self.obstacle_sprites, 'invisible')
                        if style == 'entities':
                            if col == '0':
                                self.player = Player((x, y), self.visible_sprites, self.obstacle_sprites)
                            else:
                                monster_name = None
                                monster_type = None
                                if col == '1':
                                    monster_name = 'Ghost'
                                    monster_type = 'Undead'
                                    Enemy((x, y), monster_name, monster_type, self.visible_sprites,
                                          self.obstacle_sprites)

    def cast_magic(self, style):
        if style == 'heal':
            self.player_magic.heal(self.player, [self.visible_sprites])
        if style == 'fire_magic':
            pass

    def run(self):
        # update and draw the game
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.visible_sprites.enemy_update(self.player)
        self.ui.display(self.player)


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        # general setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        # creating the floor
        self.floor_surf = pygame.image.load(get_path(catalog='map/map_data', file_name='ground_level.png')).convert()

        self.floor_surf = pygame.transform.rotozoom(self.floor_surf, 0, 2)
        self.floor_rect = self.floor_surf.get_rect(topleft=(0, 0))

    def custom_draw(self, player):
        # getting the offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # drawing the floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)

        for sprite in sorted(self.sprites(), key=lambda x: x.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

    def enemy_update(self, player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, 'sprite_type') and
                         sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)
