import pygame
import random
from pygame.locals import *
from os import path
from Class import *
from Function import *
from Settings import *
from ScaledGame import *

class Game:
    def __init__(self, main):
        self.main = main
        self.game_dict = self.main.main_dict["game"]
        self.settings_dict = self.game_dict["settings"]
        self.init_game()

    def init_game(self):
        pass

    def draw(self):
        pass

    def update(self):
        pass

    def new_game(self):
        pass

class Player(pygame.sprite.Sprite):
    def __init__(self, main, group, dict, data, item, parent=None, variable=None, action=None):
        # Initialization -------------- #
        init_sprite(self, main, group, dict, data, item, parent, variable, action)

    def init(self):
        pass

    def load(self):
        pass

    def new(self):
        pass

    def get_keys(self):
        pass

    def draw(self):
        pass

    def update(self):
        pass



MAIN_DICT = {
    "background": {
        None: None,
        "default": {
            "color": DARK_SKY_BLUE,
            "image": None,
        },
    },
    "music": {
        None: None,
        "default": None,
    },
    "sound": {
    },
    "font": {
        "LiberationSerif": {"ttf": "LiberationSerif-Regular.ttf", "size": 40}
    },
    "menu": {
        "main_menu": {
            "background": "default",
            "music": "default",
        },
        "pause_menu": {
            "background": None,
            "music": None,
        },
        "battle_menu": {
            "background": None,
            "music": None,
        }
    },
    "button": {
        "settings": {
            "default": {
                "align": "nw", "size": (280, 50),
                "border": True, "border_size": (5, 5), "border_color": BLACK,
                "text_align": "center", "font": "LiberationSerif", "font_color": WHITE,
                "inactive_color": LIGHT_SKY_BLUE, "active_color": DARK_SKY_BLUE,
                "sound_action": None, "sound_active": None, "sound_inactive": None},
        },
        "main_menu": {
            "new_game": {"settings": "default", "pos": [20, 20], "text": "New Game", "action": "self.game.new_game"},
            "select_level": {"settings": "default", "pos": [20, 90], "text": "Select Level", "action": None},
            "exit": {"settings": "default", "pos": [20, 160], "text": "Exit", "action": "self.main.quit_game"},
        },
    },
    "game": {
        "settings": {
            "interface": {
                "box_border_size": [6, 6], "stat_border_size": [3, 3],
                "box_color": DARKGREY, "hp_color": RED, "bp_color": BLUE,
                "box_border_color": LIGHTSKYGREY, "stat_border_color": BLACK,
                "ui_align": "nw"
            },
        },
    },
}
