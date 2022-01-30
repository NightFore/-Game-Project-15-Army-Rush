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

        # Debug
        self.wip_check_new_game = False

    def draw(self):
        pass

    def update(self):
        self.dt = self.main.dt

        if self.wip_check_new_game:
            for unit in self.player.units:
                if not self.unit_attack(unit, self.enemy.units):
                    self.unit_move(unit)
            for unit in self.enemy.units:
                if not self.unit_attack(unit, self.player.units):
                    self.unit_move(unit)

    def new_game(self):
        self.wip_check_new_game = True

        self.main.update_menu()
        self.player = Player(self.main, self.players, self.main_dict, data="players", item=1)
        self.enemy = Enemy(self.main, self.players, self.main_dict, data="players", item=2)

        # Unit Production
        data = "production"
        item = "unit"
        for id in self.main_dict[item]:
            sprite = Button(self, self.buttons_unit, self.button_dict, data=data, item=item)
            sprite.variable = [self.player, id]

            # WIP
            self.main.update_sprite_rect(sprite, 320*(id-1), 650)

        # Buttons (Quit & Pause)
        data = "interface"
        for item in self.game.button_dict[data]:
            Button(self, self.game.buttons, self.game.button_dict, data=data, item=item)


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

    def unit_attack(self, unit, enemies):
        collided = collide_rect_sprites(unit.rect, enemies)
        if collided:
            if pygame.time.get_ticks() - unit.last_attack >= unit.delay_attack:
                unit.last_attack = pygame.time.get_ticks()
                for enemy in collided:
                    enemy.current_health -= unit.attack
            return True
        return False

def collide_rect_sprites(rect, sprites):
    """
    Return a list of all "sprites" colliding with "rect"
    """
    sprites_collided = []
    for sprite in sprites:
        if rect.colliderect(sprite.rect):
            sprites_collided.append(sprite)
    return sprites_collided



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
        self.gain_gold = 10

        # Mana
        self.current_mana = 0
        self.gain_mana = 1

        # Supply
        self.current_supply = 0
        self.max_supply = 10

        # Experience
        self.current_exp = 0
        self.gain_exp = 10000

    def load_interface(self):
        # Initialization
        self.ui_data = "interface_box"
        self.ui_settings = self.dict["settings"][self.ui_data]

        # Box
        self.ui_size = self.ui_settings["size"]
        self.ui_border_size = self.ui_settings["border_size"]
        self.ui_color = self.ui_settings["color"]
        self.ui_border_color = self.ui_settings["border_color"]
        self.ui_align = self.ui_settings["align"]

        # Font
        self.ui_text_align = self.ui_settings["text_align"]
        self.ui_font = self.main.font_dict[self.ui_settings["font"]]
        self.ui_font_color = self.ui_settings["font_color"]

        # Experience
        ui_item = 1
        ui_object = self.dict[self.ui_data][ui_item]
        ui_pos = ui_object["pos"]
        self.ui_rect_1 = [ui_pos[0], ui_pos[1], self.ui_size[0], self.ui_size[1]]
        self.ui_text_pos_1 = init_sprite_text_rect(self.ui_rect_1)

        # Gold
        ui_item = 2
        ui_object = self.dict[self.ui_data][ui_item]
        ui_pos = ui_object["pos"]
        self.ui_rect_2 = [ui_pos[0], ui_pos[1], self.ui_size[0], self.ui_size[1]]
        self.ui_text_pos_2 = init_sprite_text_rect(self.ui_rect_2)

        # Mana
        ui_item = 3
        ui_object = self.dict[self.ui_data][ui_item]
        ui_pos = ui_object["pos"]
        self.ui_rect_3 = [ui_pos[0], ui_pos[1], self.ui_size[0], self.ui_size[1]]
        self.ui_text_pos_3 = init_sprite_text_rect(self.ui_rect_3)

        # Supply
        ui_item = 4
        ui_object = self.dict[self.ui_data][ui_item]
        ui_pos = ui_object["pos"]
        self.ui_rect_4 = [ui_pos[0], ui_pos[1], self.ui_size[0], self.ui_size[1]]
        self.ui_text_pos_4 = init_sprite_text_rect(self.ui_rect_4)


    def draw_interface(self):
        self.main.draw_surface(self.ui_rect_1, self.ui_color, self.ui_border_size, self.ui_border_color, self.ui_align)
        self.main.draw_surface(self.ui_rect_2, self.ui_color, self.ui_border_size, self.ui_border_color, self.ui_align)
        self.main.draw_surface(self.ui_rect_3, self.ui_color, self.ui_border_size, self.ui_border_color, self.ui_align)
        self.main.draw_surface(self.ui_rect_4, self.ui_color, self.ui_border_size, self.ui_border_color, self.ui_align)
        self.main.draw_text("EXP: %i" % self.gain_exp, self.ui_font, self.ui_font_color, self.ui_text_pos_1, self.ui_text_align)
        self.main.draw_text("Gold: %i" % self.current_gold, self.ui_font, self.ui_font_color, self.ui_text_pos_2, self.ui_text_align)
        self.main.draw_text("Mana: %i" % self.current_mana, self.ui_font, self.ui_font_color, self.ui_text_pos_3, self.ui_text_align)
        self.main.draw_text("Supply: %i/%i" % (self.current_supply, self.max_supply), self.ui_font, self.ui_font_color, self.ui_text_pos_4, self.ui_text_align)

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
        # WIP
        self.current_health = 10
        self.attack = 1
        self.last_attack = pygame.time.get_ticks()
        self.delay_attack = 1000

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
        pass

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
    # Init (Settings) ----------------- #
    "game": {
        "project_title": "Army Rush", "screen_size": (1280, 720), "FPS": 60,
        "default_music_volume": 5, "default_sound_volume": 75,
        "key_repeat": (100, 30)},


    # Game (Settings) ----------------- #
    "settings": {
        "interface_box": {"size": [180, 50], "border_size": [6, 6], "align": "nw",
                          "font": "LiberationSerif_30", "text_align": "center",
                          "color": DARKGREY, "border_color": LIGHTSKYGREY, "font_color": WHITE},
        "players": {},
        "unit": {"size": [50, 50], "align": "sw", "vel": [100, 0], "acc": [0, 0]},
        "castle": {"size": [250, 250], "align": "sw"},
    },


    # Game (Interface) ---------------- #
    "interface_box": {
        1: {"pos": [390, 10]},
        2: {"pos": [710, 10]},
        3: {"pos": [900, 10]},
        4: {"pos": [1090, 10]},
    },


    # Game (Player) ------------------- #
    "players": {
        1: {"pos": [20, 500], "vel": [1, 0], "align": "sw"},
        2: {"pos": [1260, 500], "vel": [-1, 0], "align": "se"},
    },


    # Game (Castle) ------------------- #
    "castle": {
        1: {},
        2: {}
    },


    # Game (Unit) --------------------- #
    "unit": {
        1: {"name": "Peasant", "cost_gold": 50, "cost_mana": 0, "cost_supply": 1},
        2: {"name": "Squire", "cost_gold": 100, "cost_mana": 0, "cost_supply": 1},
        3: {"name": "Archer", "cost_gold": 125, "cost_mana": 0, "cost_supply": 1},
        4: {"name": "Priest", "cost_gold": 150, "cost_mana": 25, "cost_supply": 1},
    },


    # Background Dict ----------------- #
    "background": {
        None: None,
        "default": {
            "color": DARK_SKY_BLUE,
            "image": None,
        },
    },


    # Music Dict ---------------------- #
    "music": {
        "default": None,
    },


    # Sound Dict ---------------------- #
    "sound": {
    },


    # Font Dict ----------------------- #
    "font": {
        "default": {"ttf": None, "size": 100},
        "LiberationSerif": {"ttf": "LiberationSerif-Regular.ttf", "size": 40},
        "LiberationSerif_30": {"ttf": "LiberationSerif-Regular.ttf", "size": 30}
    },


    # Menu Dict ----------------------- #
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


    # Button Dict --------------------- #
    "button": {
        "settings": {
            "default": {
                "size": (280, 50), "border_size": (5, 5), "align": "nw",
                "font": "LiberationSerif", "font_color": WHITE, "text_align": "center",
                "inactive_color": LIGHT_SKY_BLUE, "active_color": DARK_SKY_BLUE, "border_color": BLACK,
                "sound_action": None, "sound_active": None, "sound_inactive": None},
            "production": {
                "size": (320, 50), "border_size": (5, 5), "align": "nw",
                "font": "LiberationSerif", "font_color": WHITE, "text_align": "center",
                "inactive_color": LIGHT_SKY_BLUE, "active_color": DARK_SKY_BLUE, "border_color": BLACK,
                "sound_action": None, "sound_active": None, "sound_inactive": None},
            "interface": {
                "size": (180, 50), "border_size": (6, 6), "align": "nw",
                "font": "LiberationSerif_30", "font_color": WHITE, "text_align": "center",
                "border_color": DARKSKYGREY, "inactive_color": DARKGREY, "active_color": LIGHTGREY,
                "sound_action": None, "sound_active": None, "sound_inactive": None},
        },
        "main_menu": {
            "new_game": {"settings": "default", "pos": [10, 70], "text": "New Game", "action": "self.game.new_game"},
        },
        "production": {
            "unit": {"settings": "production", "pos": [0, 0], "action": "self.game.unit_production"},
        },
        "interface": {
            "quit": {"settings": "interface", "pos": [10, 10], "text": "Quit", "action": "self.main.quit_game"},
            "pause": {"settings": "interface", "pos": [200, 10], "text": "Pause", "action": "self.main.pause_game"},
        }
    },
}
