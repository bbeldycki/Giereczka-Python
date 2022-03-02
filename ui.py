import pygame
from settings import *


class UI:
    def __init__(self):
        # general resources
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(ui_font, ui_font_size)

        # bar setup
        self.health_bar_rect = pygame.Rect(10, 10, hp_bar_width, bar_height)
        self.mana_bar_rect = pygame.Rect(10, 35, mana_bar_width, bar_height)
        self.exp_bar_rect = pygame.Rect(10, 60, exp_bar_width, bar_height)

    def show_bar(self, current_amount, max_amount, bg_rect, color) -> None:
        # draw background
        pygame.draw.rect(self.display_surface, ui_bg_color, bg_rect)

        # convering stat to pixels
        ratio = current_amount / max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width

        # drawing the bars
        pygame.draw.rect(self.display_surface, color, current_rect)
        pygame.draw.rect(self.display_surface, ui_border_color, bg_rect, 3)

    def spell_box(self, left, top) -> object:
        bg_rect = pygame.Rect(left, top, spell_box_size, spell_box_size)
        pygame.draw.rect(self.display_surface, ui_bg_color, bg_rect)
        pygame.draw.rect(self.display_surface, ui_border_color, bg_rect, 5)
        return bg_rect

    def spell_graphix(self, spell_index):
        bg_rect = self.spell_box(300, 500)
        # self.display_surface.blit(spell_surf, spell_rect)

    def show_exp(self, exp) -> None:
        text_surf = self.font.render(str(int(exp)), False, text_color)
        x = self.display_surface.get_size()[0] - 10
        y = self.display_surface.get_size()[1] - 10
        text_rect = text_surf.get_rect(bottomright=(x, y))
        pygame.draw.rect(self.display_surface, ui_bg_color, text_rect.inflate(10, 10))
        self.display_surface.blit(text_surf, text_rect)

    def display(self, player) -> None:
        self.show_bar(player.health, player.stats['health'], self.health_bar_rect, hp_bar_color)
        self.show_bar(player.mana, player.stats['mana'], self.mana_bar_rect, mana_bar_color)
        self.show_bar(player.exp, player.stats['exp'], self.exp_bar_rect, exp_bar_color)
        self.show_exp(player.exp)

        # self.spell_box(300, 500)
        # self.spell_box(360, 500)
