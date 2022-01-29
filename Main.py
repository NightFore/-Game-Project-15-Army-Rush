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
        self.game = self
        self.load()
        self.new()

    def load(self):
        self.main_dict = self.main.main_dict
        self.settings_dict = self.main_dict["settings"]
        self.button_dict = self.main.button_dict

    def new(self):
        self.players = pygame.sprite.Group()
        self.castles = pygame.sprite.Group()
        self.buttons = pygame.sprite.Group()
        self.buttons_unit = pygame.sprite.Group()

    def draw(self):
        pass

    def update(self):
        self.dt = self.main.dt

    def new_game(self):
        self.player = Player(self.main, self.players, self.main_dict, data="players", item=1)
        self.enemy = Enemy(self.main, self.players, self.main_dict, data="players", item=2)

        data = "production"
        # Unit Production
        item = "unit"
        for id in self.main_dict[item]:
            sprite = Button(self, self.buttons_unit, self.button_dict, data=data, item=item)
            sprite.variable = [self.player, id]

            # WIP
            self.main.update_sprite_rect(sprite, 320*(id-1), 650)


    def unit_production(self, args):
        """
        args = [player: class, id: int]
        """
        player = args[0]
        id = args[1]
        unit = self.main_dict["unit"][id]

        # Check resources
        check_gold = player.current_gold >= unit["cost_gold"]
        check_mana = player.current_mana >= unit["cost_mana"]
        check_supply = player.current_supply + unit["cost_supply"] <= player.max_supply

        # Production
        if check_gold and check_mana and check_supply:
            print("%s have been produced!" % unit["name"])
            player.current_gold -= unit["cost_gold"]
            player.current_mana -= unit["cost_mana"]
            player.current_supply += unit["cost_supply"]
            Unit(self.main, player.units, self.main_dict, data="unit", item=id, parent=player)
        else:
            print("You don't have enough resources!")

    def resources_production(self, player):
        player.current_gold += player.gain_gold * self.dt
        player.current_mana += player.gain_mana * self.dt

    def unit_move(self, sprite):
        sprite.pos += sprite.vel * self.dt
        self.main.update_sprite_rect(sprite)


class Player(pygame.sprite.Sprite):
    def __init__(self, main, group, dict=None, data=None, item=None, parent=None, variable=None, action=None):
        init_class(self, main, group, dict, data, item, parent, variable, action, surface=True)

    def init(self):
        self.units = pygame.sprite.Group()
        self.castle = Castle(self.main, self.game.castles, self.main.main_dict, data="castle", item=self.item, parent=self)
        self.load_interface()

    def load(self):
        # Gold
        self.current_gold = 250
        self.gain_gold = 1

        # Mana
        self.current_mana = 0
        self.gain_mana = 5

        # Supply
        self.current_supply = 0
        self.max_supply = 10

    def load_interface(self):
        # Initialization
        self.ui_data = "interface_box"
        self.ui_item = 1
        self.ui_object = self.dict[self.ui_data][self.ui_item]
        self.ui_settings = self.dict["settings"][self.ui_data]

        # Box
        self.ui_pos = self.ui_object["pos"]
        self.ui_size = self.ui_settings["size"]
        self.ui_border_size = self.ui_settings["border_size"]
        self.ui_color = self.ui_settings["color"]
        self.ui_border_color = self.ui_settings["border_color"]
        self.ui_align = self.ui_settings["align"]
        self.ui_rect = [self.ui_pos[0], self.ui_pos[1], self.ui_size[0], self.ui_size[1]]

        # Font
        self.ui_font = self.main.font_dict[self.ui_settings["font"]]
        self.ui_font_color = self.ui_settings["font_color"]

    def draw_interface(self):
        # Box
        self.main.draw_surface(self.ui_align, self.ui_rect, self.ui_color, self.ui_border_size, self.ui_border_color)

        # Text
        self.wip_text_pos = [500, 250]
        self.main.draw_text("Gold: %i" % self.current_gold, self.ui_font, self.ui_font_color, self.wip_text_pos, self.ui_align)

    def new(self):
        pass

    def draw(self):
        self.draw_interface()

    def update(self):
        self.game.resources_production(self)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, main, group, dict=None, data=None, item=None, parent=None, variable=None, action=None):
        init_class(self, main, group, dict, data, item, parent, variable, action, surface=True)

    def init(self):
        self.units = pygame.sprite.Group()
        self.castle = Castle(self.main, self.game.castles, self.main.main_dict, data="castle", item=self.item, parent=self)

    def load(self):
        # Gold
        self.current_gold = 250
        self.gain_gold = 10

        # Mana
        self.current_mana = 0
        self.gain_mana = 5

        # Supply
        self.current_supply = 0
        self.max_supply = 10

    def new(self):
        self.last_spawn = pygame.time.get_ticks()

    def draw(self):
        pass

    def update(self):
        self.game.resources_production(self)

        if pygame.time.get_ticks() - self.last_spawn >= 2500:
            self.game.unit_production((self, self.item))
            self.last_spawn = pygame.time.get_ticks()


class Unit(pygame.sprite.Sprite):
    def __init__(self, main, group, dict=None, data=None, item=None, parent=None, variable=None, action=None):
        init_class(self, main, group, dict, data, item, parent, variable, action, surface=True)

    def init(self):
        self.vel.x *= self.parent.vel.x
        self.align = self.parent.align
        self.main.update_sprite_rect(self, self.parent.pos[0], self.parent.pos[1])

    def load(self):
        pass

    def new(self):
        pass

    def draw(self):
        """
        if self.current_health != self.max_health:
            draw health bar
        """
        pass

    def update(self):
        """
        if:
            self.check_range()
        """
        self.game.unit_move(self)

    def check_range(self):
        """
        for enemy in self.enemy.units:
            if collide(self.hit_rect, enemy.hit_rect):
                if self.attack_speed < self.time - self.last_attack:
                    self.game.attack_target(self, enemy)
        """
        pass


class Castle(pygame.sprite.Sprite):
    def __init__(self, main, group, dict=None, data=None, item=None, parent=None, variable=None, action=None):
        init_class(self, main, group, dict, data, item, parent, variable, action, surface=True)

    def init(self):
        self.align = self.parent.align
        self.main.update_sprite_rect(self, self.parent.pos[0], self.parent.pos[1])

    def load(self):
        pass

    def new(self):
        pass

    def draw(self):
        pass

    def update(self):
        pass


MAIN_DICT = {
    "game": {
        "project_title": "Army Rush", "screen_size": (1280, 720), "FPS": 60,
        "default_music_volume": 5, "default_sound_volume": 75,
        "key_repeat": (100, 30)},

    "settings": {
        "interface_box": {"size": [310, 210], "border_size": [6, 6], "align": "nw",
                          "color": DARKGREY, "border_color": LIGHTSKYGREY,
                          "font": "LiberationSerif", "font_color": WHITE},
        "players": {},
        "unit": {"size": [50, 50], "align": "sw", "vel": [50, 0], "acc": [0, 0]},
        "castle": {"size": [250, 250], "align": "sw"},
    },

    "interface_box": {
        1: {"pos": [960, 140]},
    },

    "players": {
        1: {"pos": [20, 500], "vel": [1, 0], "align": "sw"},
        2: {"pos": [1260, 500], "vel": [-1, 0], "align": "se"},
    },

    "castle": {
        1: {},
        2: {}
    },

    "unit": {
        1: {"name": "Peasant", "cost_gold": 50, "cost_mana": 0, "cost_supply": 1},
        2: {"name": "Squire", "cost_gold": 100, "cost_mana": 0, "cost_supply": 1},
        3: {"name": "Archer", "cost_gold": 125, "cost_mana": 0, "cost_supply": 1},
        4: {"name": "Priest", "cost_gold": 150, "cost_mana": 25, "cost_supply": 1},
    },


    # Background Dict
    "background": {
        None: None,
        "default": {
            "color": DARK_SKY_BLUE,
            "image": None,
        },
    },


    # Music Dict
    "music": {
        "default": None,
    },


    # Sound Dict
    "sound": {
    },


    # Font Dict
    "font": {
        "default": {"ttf": None, "size": 100},
        "LiberationSerif": {"ttf": "LiberationSerif-Regular.ttf", "size": 40}
    },


    # Menu Dict
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


    # Button Dict
    "button": {
        "settings": {
            "default": {
                "align": "nw", "size": (280, 50),
                "border": True, "border_size": (5, 5), "border_color": BLACK,
                "text_align": "center", "font": "LiberationSerif", "font_color": WHITE,
                "inactive_color": LIGHT_SKY_BLUE, "active_color": DARK_SKY_BLUE,
                "sound_action": None, "sound_active": None, "sound_inactive": None},
            "icon": {
                "align": "nw", "size": (320, 50),
                "border": True, "border_size": (5, 5), "border_color": BLACK,
                "text_align": "center", "font": "LiberationSerif", "font_color": WHITE,
                "inactive_color": LIGHT_SKY_BLUE, "active_color": DARK_SKY_BLUE,
                "sound_action": None, "sound_active": None, "sound_inactive": None},
        },
        "main_menu": {
            "new_game": {"settings": "default", "pos": [20, 20], "text": "New Game", "action": "self.game.new_game"},
            "Test": {"settings": "default", "pos": [20, 90], "text": "Test", "action": None},
            "exit": {"settings": "default", "pos": [20, 160], "text": "Exit", "action": "self.main.quit_game"},
        },
        "production": {
            "unit": {"settings": "icon", "pos": [0, 0], "action": "self.game.unit_production"},
        }
    },
}
