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
        self.game_dict = self.main.main_dict["game"]
        self.settings_dict = self.game_dict["settings"]
        self.button_dict = self.main.button_dict

    def new(self):
        self.players = pygame.sprite.Group()
        self.buttons = pygame.sprite.Group()
        self.buttons_unit = pygame.sprite.Group()

    def draw(self):
        pass

    def update(self):
        self.dt = self.main.dt

    def new_game(self):
        self.player = Player(self.main, self.players, self.game_dict)
        self.enemy = Enemy(self.main, self.players, self.game_dict)

        data = "production"
        # Unit Production
        item = "unit"
        for id in self.game_dict[item]:
            sprite = Button(self, self.buttons_unit, self.button_dict, data=data, item=item)
            sprite.variable = [self.player, id]

            # WIP
            self.main.update_sprite_rect(sprite, 0 + 320*(id-1), 500)


    def unit_production(self, args):
        """
        args = [player: class, id: int]
        """
        player = args[0]
        id = args[1]
        unit = self.game_dict["unit"][id]

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
            Unit(self.main, player.units, self.game_dict, data="unit", item=id, parent=player)
        else:
            print("You don't have enough resources!")

    def resources_production(self, player):
        player.current_gold += player.gain_gold * self.dt
        player.current_mana += player.gain_mana * self.dt

    def unit_move(self, sprite):
        sprite.pos += sprite.vel * self.dt
        self.main.update_sprite_rect(sprite)

class Player(pygame.sprite.Sprite):
    def __init__(self, main, group, dict, data=None, item=None, parent=None, variable=None, action=None):
        init_sprite(self, main, group, dict, data, item, parent, variable, action)
        self.units = pygame.sprite.Group()

        # WIP (Update: init_sprite → init_class)
        self.rect = [0, 0, 0, 0]

    def init(self):
        # Gold
        self.current_gold = 250
        self.gain_gold = 1

        # Mana
        self.current_mana = 0
        self.gain_mana = 5

        # Supply
        self.current_supply = 0
        self.max_supply = 10

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

class Enemy(pygame.sprite.Sprite):
    def __init__(self, main, group, dict, data=None, item=None, parent=None, variable=None, action=None):
        init_sprite(self, main, group, dict, data, item, parent, variable, action)
        self.units = pygame.sprite.Group()

        # WIP (Update: init_sprite → init_class)
        self.rect = [0, 0, 0, 0]

    def init(self):
        # Gold
        self.current_gold = 250
        self.gain_gold = 10

        # Mana
        self.current_mana = 0
        self.gain_mana = 5

        # Supply
        self.current_supply = 0
        self.max_supply = 10

        self.last_wip = pygame.time.get_ticks()
        self.delay_wip = 500

    def load(self):
        pass

    def new(self):
        pass

    def get_keys(self):
        pass

    def draw(self):
        pass

    def update(self):
        self.game.resources_production(self)

        if pygame.time.get_ticks() - self.last_wip >= 2500:
            print("ok")
            self.game.unit_production((self, 1))
            self.last_wip = pygame.time.get_ticks()


class Unit(pygame.sprite.Sprite):
    def __init__(self, main, group, dict, data=None, item=None, parent=None, variable=None, action=None):
        init_sprite(self, main, group, dict, data, item, parent, variable, action)

    def init(self):
        self.rect = [50, 350, 50, 50]
        self.pos = self.rect[0], self.rect[1]
        self.size = self.rect[2], self.rect[3]
        self.vel = vec(50, 0)
        self.align = "nw"
        self.surface = pygame.Surface(self.size)

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
        self.game.unit_move(self)
        """
        if:
            self.check_range()
        else:
            self.move()
        """
        pass

    def check_range(self):
        """
        for enemy in self.enemy.units:
            if collide(self.hit_rect, enemy.hit_rect):
                if self.attack_speed < self.time - self.last_attack:
                    self.game.attack_target(self, enemy)
        """
        pass

    def move(self):
        pass


def unit_attack(sprite_1, sprite_2):
    sprite_2 -= sprite_1.attack
    if sprite_2.health <= 0:
        if sprite_1.parent == self.game.player:
            self.game.player += sprite_2.gain_experience
        sprite_2.kill()



MAIN_DICT = {
    # Game Dict
    "game": {
        "settings": {
            "project_title": "Army Rush",
            "screen_size": (1280, 720),
            "FPS": 60,
            "key_repeat": (100, 30),
            "default_music_volume": 5,
            "default_sound_volume": 75
        },

        "unit": {
            1: {"name": "Peasant", "cost_gold": 50, "cost_mana": 0, "cost_supply": 1},
            2: {"name": "Squire", "cost_gold": 100, "cost_mana": 0, "cost_supply": 1},
            3: {"name": "Archer", "cost_gold": 125, "cost_mana": 0, "cost_supply": 1},
            4: {"name": "Priest", "cost_gold": 150, "cost_mana": 25, "cost_supply": 1},
        }
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
