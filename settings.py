from os.path import realpath, join
from os import walk
from csv import reader
import pygame

width = 1216
height = 800
fps = 50
tilesize = 64

# UI
# ui bars
bar_height = 20
hp_bar_width = 200
mana_bar_width = 200
exp_bar_width = 200
spell_box_size = 50
item_box_size = 50
ui_font = realpath(join('graphics', 'Font', 'arial.ttf'))
ui_font_size = 18

# general colors
water_color = '#71ddee'
ui_bg_color = '#222222'
ui_border_color = '#111111'
text_color = '#EEEEEE'
# ui colors
hp_bar_color = 'red'
mana_bar_color = 'blue'
exp_bar_color = 'yellow'
ui_border_color_active = 'gold'

# enemies
monsters = {
    'enemy1': {
        'health': 100,
        'experience': 100,
        'speed': 1,
        'resistance': 10,
        'attack_radius': 100,
        'spot_radius': 300
    }
}


# utility functions
def get_path(catalog, file_name):
    return realpath(join('graphics', catalog, file_name))


def import_csv_layout(path):
    terrain = []
    with open(path) as level_map:
        layout = reader(level_map, delimiter=',')
        for row in layout:
            terrain.append(list(row))
        return terrain


def import_all_images_from_catalog(path):
    surface_image_list = []
    for _, __, img_files in walk(path):
        for image in img_files:
            full_path = join(path, image)
            surface_image_list.append(pygame.image.load(full_path).convert_alpha())
    return surface_image_list
