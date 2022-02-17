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

        # Attack
        if self.wip_check_new_game:
            for unit in self.player.units:
                if not self.unit_attack(unit, self.enemy.units, self.enemy.castle):
                    self.unit_move(unit)
            for unit in self.enemy.units:
                if not self.unit_attack(unit, self.player.units, self.player.castle):
                    self.unit_move(unit)

    def new_game(self):
        # Debug
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
            player.current_gold -= unit["cost_gold"]
            player.current_mana -= unit["cost_mana"]
            player.current_supply += unit["cost_supply"]
            Unit(self.main, player.units, self.main_dict, data="unit", item=id, parent=player)

    def resources_production(self, player):
        player.current_gold += player.gain_gold * self.dt
        player.current_mana += player.gain_mana * self.dt

    def unit_move(self, sprite):
        sprite.pos += sprite.vel * self.dt
        self.main.update_sprite_rect(sprite)

    def unit_attack(self, unit, enemies, castle):
        collided = collide_rect_sprites(unit.hit_rect, enemies)
        collided_castle = unit.hit_rect.colliderect(castle.rect) and castle.current_health > 0
        if collided or collided_castle:
            if pygame.time.get_ticks() - unit.last_attack >= unit.delay_attack:
                unit.last_attack = pygame.time.get_ticks()
                # Units
                if collided:
                    for enemy in collided:
                        enemy.current_health -= unit.attack
                        if enemy.current_health <= 0:
                            enemy.parent.current_supply -= enemy.cost_supply
                            enemy.kill()
                            if unit.parent == self.player:
                                self.player.gain_exp += enemy.gain_exp
                # Castle
                if collided_castle:
                    castle.current_health -= unit.attack
                    if castle.current_health <= 0:
                        castle.kill()
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
        self.current_gold = 500
        self.gain_gold = 20

        # Mana
        self.current_mana = 0
        self.gain_mana = 5

        # Supply
        self.current_supply = 0
        self.max_supply = 10

        # Experience
        self.current_exp = 0
        self.gain_exp = 0

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
        self.pos[0] = self.parent.pos[0]
        self.pos[1] = self.parent.pos[1] + random.randint(-15, 15)
        self.vel.x *= self.parent.vel.x * random.uniform(0.95, 1.05)
        self.align = self.parent.align
        self.main.update_sprite_rect(self, self.pos[0], self.pos[1])

    def load(self):
        self.name = self.object["name"]
        self.gain_exp = self.object["gain_exp"]
        self.cost_supply = self.object["cost_supply"]

        self.max_health = self.object["max_health"]
        self.current_health = self.max_health

        self.attack = self.object["attack"]
        self.delay_attack = self.object["delay_attack"]
        self.last_attack = pygame.time.get_ticks()

        # Debug Range
        self.range = self.object["range"]
        self.hit_rect = [0, 0, self.rect[2] + 2*self.range, 2]
        self.hit_rect = self.main.align_rect(self.hit_rect, init_sprite_text_rect(self.rect), "center")

    def new(self):
        pass

    def draw(self):
        """
        if self.current_health != self.max_health:
            draw health bar
        """
        # Debug Range
        pygame.draw.rect(self.main.gameDisplay, RED, self.hit_rect, 1)

    def update(self):
        self.hit_rect = self.main.align_rect(self.hit_rect, init_sprite_text_rect(self.rect), "center")


class Castle(pygame.sprite.Sprite):
    def __init__(self, main, group, dict=None, data=None, item=None, parent=None, variable=None, action=None):
        init_class(self, main, group, dict, data, item, parent, variable, action, surface=True)

    def init(self):
        self.align = self.parent.align
        self.main.update_sprite_rect(self, self.parent.pos[0], self.parent.pos[1])

    def load(self):
        self.max_health = 5000
        self.current_health = self.max_health

    def new(self):
        # Initialization
        self.ui_data = "interface_castle"
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

        ui_item = self.parent.item
        ui_object = self.dict[self.ui_data][ui_item]
        ui_pos = ui_object["pos"]
        self.ui_rect = [ui_pos[0], ui_pos[1], self.ui_size[0], self.ui_size[1]]
        self.ui_text_pos = init_sprite_text_rect(self.ui_rect)

    def draw(self):
        self.main.draw_surface(self.ui_rect, self.ui_color, self.ui_border_size, self.ui_border_color, self.ui_align)
        self.main.draw_text("Health: %i/%i" % (self.current_health, self.max_health), self.ui_font, self.ui_font_color, self.ui_text_pos, self.ui_text_align)

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
        "interface_castle": {"size": [250, 50], "border_size": [6, 6], "align": "nw",
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

    "interface_castle": {
        1: {"pos": [20, 520]},
        2: {"pos": [1010, 520]}

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
        1: {"name": "Scout", "size": [50, 50], "vel": [200, 0],
            "cost_gold": 50, "cost_mana": 0, "cost_supply": 1,
            "max_health": 25, "attack": 5, "delay_attack": 2500,
            "gain_exp": 10, "range": 5, "attack_type": 1},

        2: {"name": "Squire", "size": [70, 100], "vel": [125, 0],
            "cost_gold": 100, "cost_mana": 0, "cost_supply": 1,
            "max_health": 100, "attack": 10, "delay_attack": 1000,
            "gain_exp": 25, "range": 20, "attack_type": 1},

        3: {"name": "Archer", "size": [40, 60], "vel": [90, 0],
            "cost_gold": 125, "cost_mana": 5, "cost_supply": 1,
            "max_health": 65, "attack": 8, "delay_attack": 2000,
            "gain_exp": 30, "range": 200, "attack_type": 2},

        4: {"name": "Priest", "size": [50, 70], "vel": [80, 0],
            "cost_gold": 150, "cost_mana": 25, "cost_supply": 1,
            "max_health": 50, "attack": 5, "delay_attack": 1500,
            "gain_exp": 40, "range": 10, "attack_type": 3},
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
