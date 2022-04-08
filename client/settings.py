from typing import Dict, Any
from os.path import realpath, join
from os import walk
from csv import reader
import pygame

SERVER_IP = '127.0.0.1'
SERVER_PORT = 5050
SERVER_TIMEOUT = 0.001
CLIENT_TIMEOUT = 0.001

WIDTH = 800
HEIGHT = 600
FPS = 60


# utility functions
def initialize_stats(**kwargs) -> Dict[str, Any]:
    stats = {
        'alive': True,
        'moving': False,
        'movement_speed': 10,
        'animating': False,
        'foreground_location': {'default': [(0, 0)]},
        'foreground_index': -1
    }

    for arg in kwargs:
        stats[arg] = kwargs[arg]

    return stats


def get_path(catalog: str, file_name: str) -> str:
    return realpath(join('graphics', catalog, file_name))


def import_all_images_from_catalog(path: str) -> list:
    surface_image_list = []
    for _, __, img_files in walk(path):
        for image in img_files:
            full_path = join(path, image)
            surface_image_list.append(pygame.image.load(full_path).convert_alpha())
    return surface_image_list
