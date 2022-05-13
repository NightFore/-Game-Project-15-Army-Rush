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
        # Game Initialization
        self.main = main
        self.game = self
        self.init_dict()
        self.load()
        self.new()

    def init_dict(self):
        self.main_dict = self.main.main_dict
        self.settings_dict = self.main_dict["settings"]
        self.button_dict = self.main.button_dict

    def load(self):
        pass

    def new(self):
        # Sprites
        self.players = pygame.sprite.Group()
        self.castles = pygame.sprite.Group()
        self.units = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()

        # Interface
        self.buttons = pygame.sprite.Group()
        self.buttons_unit = pygame.sprite.Group()

    def draw(self):
        pass

    def update(self):
        # Main
        self.dt = self.main.dt

        # Game
        for unit in self.units:
            self.sprite_action(unit, unit.parent, unit.parent.enemy, action=True)
            self.sprite_move(unit, unit.collide)
        for projectile in self.projectiles:
            self.sprite_action(projectile, projectile.parent.parent, projectile.parent.parent.enemy)
            self.sprite_move(projectile)

    def new_game(self):
        # Initialization
        self.main.update_menu()

        # Players
        self.player = Player(self.main, self.players, self.main_dict, data="players", item=1)
        self.enemy = Enemy(self.main, self.players, self.main_dict, data="players", item=2)
        self.player.enemy = self.enemy
        self.enemy.enemy = self.player

        # Buttons (Unit Production)
        data, item = "production", "unit"
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
        """ args = [player: class, id: int] """

        # Initialization
        player, id = args[0], args[1]
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
            Unit(self.main, (self.units, player.units), self.main_dict, data="unit", item=id, parent=player)

    def resources_production(self, player):
        # Resources over time
        player.current_gold += player.gain_gold * self.dt
        player.current_mana += player.gain_mana * self.dt

    def sprite_action(self, sprite, player, enemy, action=False):
        # Collision
        collided_allies = collide_rect_sprites(sprite.hit_rect, player.units)
        collided_enemies = collide_rect_sprites(sprite.hit_rect, enemy.units)
        if sprite.hit_rect.colliderect(enemy.castle.rect) and enemy.castle.current_health > 0:
            collided_enemies.append(enemy.castle)

        # Action
        if action:
            action = pygame.time.get_ticks() - sprite.last_action >= sprite.delay_action

        # Melee
        if sprite.action_type == 1:
            sprite.collide = collided_enemies
            if sprite.collide and action:
                sprite.last_action = pygame.time.get_ticks()
                for target in collided_enemies:
                    target.current_health -= sprite.attack
                    target.health_check()

        # Ranged Attack
        elif sprite.action_type == 2:
            sprite.collide = collided_enemies
            if sprite.collide and action:
                sprite.last_action = pygame.time.get_ticks()
                Projectile(self, self.projectiles, self.main_dict, data="projectile", item=sprite.item, parent=sprite)

        # Magic Attack
        elif sprite.action_type == 3:
            sprite.collide = collided_enemies
            if sprite.collide and action:
                pass

        # Magic Support
        elif sprite.action_type == 4:
            if collided_allies and action:
                sprite.collide = collided_allies

        # Projectile
        elif sprite.action_type == 5:
            if collided_enemies:
                # Distance
                target_dist_list = []
                for target in collided_enemies:
                    target_dist_list.append(abs(sprite.rect[0] - target.rect[0]))

                # Minimum Distance
                min_dist = target_dist_list[0]
                min_target = collided_enemies[0]
                for index, target_dist in enumerate(target_dist_list):
                    if target_dist < min_dist:
                        min_dist = target_dist
                        min_target = collided_enemies[index]
                min_target.current_health -= sprite.parent.attack
                min_target.health_check()
                sprite.kill()



    def sprite_move(self, sprite, collide=False):
        if not collide:
            sprite.pos += sprite.vel * self.dt
            self.main.update_sprite_rect(sprite)


def collide_rect_sprites(rect, sprites):
    """
    Return a list of all "sprites" colliding with "rect"
    """
    sprites_collided = []
    for sprite in sprites:
        if rect.colliderect(sprite.rect):
            sprites_collided.append(sprite)
    return sprites_collided

def init_interface(self, data, item=None):
    # Initialization
    self.ui_data = data
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

    # Rect & Text Pos
    self.ui_rect = []
    self.ui_text_pos = []
    if item is None:
        for index, item in enumerate(self.dict[self.ui_data]):
            ui_pos = self.dict[self.ui_data][item]["pos"]
            self.ui_rect.append([ui_pos[0], ui_pos[1], self.ui_size[0], self.ui_size[1]])
            self.ui_text_pos.append(init_sprite_text_rect(self.ui_rect[index]))
    else:
        ui_pos = self.dict[self.ui_data][item]["pos"]
        self.ui_rect.append([ui_pos[0], ui_pos[1], self.ui_size[0], self.ui_size[1]])
        self.ui_text_pos.append(init_sprite_text_rect(self.ui_rect[0]))



def draw_interface(self, ui_text):
    # Rect
    for rect in self.ui_rect:
        self.main.draw_surface(rect, self.ui_color, self.ui_border_size, self.ui_border_color, self.ui_align)

    # Text
    for index, pos in enumerate(self.ui_text_pos):
        self.main.draw_text(ui_text[index], self.ui_font, self.ui_font_color, pos, self.ui_text_align)


class Player(pygame.sprite.Sprite):
    def __init__(self, main, group, dict=None, data=None, item=None, parent=None, variable=None, action=None):
        init_class(self, main, group, dict, data, item, parent, variable, action, surface=True, text=False)

    def init(self):
        self.castle = Castle(self.main, self.game.castles, self.main.main_dict, data="castle", item=self.item, parent=self)
        self.units = pygame.sprite.Group()
        init_interface(self, "interface_box")

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

    def new(self):
        pass

    def draw(self):
        ui_text = ["EXP: %i" % self.gain_exp, "Gold: %i" % self.current_gold, "Mana: %i" % self.current_mana, "Supply: %i/%i" % (self.current_supply, self.max_supply)]
        draw_interface(self, ui_text)

    def update(self):
        self.game.resources_production(self)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, main, group, dict=None, data=None, item=None, parent=None, variable=None, action=None):
        init_class(self, main, group, dict, data, item, parent, variable, action, surface=True, text=False)

    def init(self):
        self.castle = Castle(self.main, self.game.castles, self.main.main_dict, data="castle", item=self.item, parent=self)
        self.units = pygame.sprite.Group()

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
        init_class(self, main, group, dict, data, item, parent, variable, action, surface=True, text=False)

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
        self.action_type = self.object["action_type"]
        self.delay_action = self.object["delay_action"]
        self.last_action = pygame.time.get_ticks()

        # Debug Range
        self.range = self.object["range"]
        self.hit_rect = [0, 0, self.rect[2] + 2*self.range, self.rect[3]-20]
        self.hit_rect = self.main.align_rect(self.hit_rect, init_sprite_text_rect(self.rect), "center")

    def new(self):
        self.collide = False

    def draw(self):
        """
        if self.current_health != self.max_health:
            draw health bar
        """
        # Debug Range
        pygame.draw.rect(self.main.gameDisplay, RED, self.hit_rect, 1)

    def update(self):
        self.hit_rect = self.main.align_rect(self.hit_rect, init_sprite_text_rect(self.rect), "center")

    def health_check(self):
        if self.current_health <= 0:
            self.parent.current_supply -= self.cost_supply
            if self.parent == self.game.enemy:
                self.game.player.gain_exp += self.gain_exp
            self.kill()


class Castle(pygame.sprite.Sprite):
    def __init__(self, main, group, dict=None, data=None, item=None, parent=None, variable=None, action=None):
        init_class(self, main, group, dict, data, item, parent, variable, action, surface=True, text=False)

    def init(self):
        self.align = self.parent.align
        self.main.update_sprite_rect(self, self.parent.pos[0], self.parent.pos[1])
        init_interface(self, "interface_castle", item=self.parent.item)

    def load(self):
        self.max_health = self.object["max_health"]
        self.current_health = self.max_health

    def new(self):
        pass

    def draw(self):
        ui_text = ["Health: %i/%i" % (self.current_health, self.max_health)]
        draw_interface(self, ui_text)

    def update(self):
        pass

    def health_check(self):
        if self.current_health <= 0:
            self.kill()




class Projectile(pygame.sprite.Sprite):
    def __init__(self, main, group, dict=None, data=None, item=None, parent=None, variable=None, action=None):
        init_class(self, main, group, dict, data, item, parent, variable, action, surface=True, text=False)

    def init(self):
        x = int(self.parent.pos[0] + self.parent.rect[2])
        y = int(self.parent.pos[1] - self.parent.rect[3] / 2)
        self.main.update_sprite_rect(self, x, y)

    def load(self):
        pass

    def new(self):
        # WIP
        self.action_type = self.object["action_type"]
        self.hit_rect = self.rect


    def draw(self):
        pass

    def update(self):
        self.hit_rect = self.rect


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
        "interface_castle": {"size": [280, 50], "border_size": [6, 6], "align": "nw",
                             "font": "LiberationSerif_30", "text_align": "center",
                             "color": DARKGREY, "border_color": LIGHTSKYGREY, "font_color": WHITE},
        "players": {},
        "castle": {"size": [250, 250], "align": "sw"},
        "unit": {"size": [50, 50], "align": "sw", "vel": [100, 0], "acc": [0, 0]},
        "projectile": {"size": [40, 8], "align": "center", "vel": [200, 0], "acc": [0, 0]}
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
        2: {"pos": [980, 520]}

    },

    # Game (Player) ------------------- #
    "players": {
        1: {"pos": [20, 500], "vel": [1, 0], "align": "sw"},
        2: {"pos": [1260, 500], "vel": [-1, 0], "align": "se"},
    },


    # Game (Castle) ------------------- #
    "castle": {
        1: {"max_health": 16000},
        2: {"max_health": 5000}
    },


    # Game (Unit) --------------------- #
    "unit": {
        1: {"name": "Scout", "size": [50, 50], "vel": [200, 0],
            "cost_gold": 50, "cost_mana": 0, "cost_supply": 1,
            "max_health": 25, "attack": 5, "delay_action": 2500,
            "gain_exp": 10, "range": 5, "action_type": 1},

        2: {"name": "Squire", "size": [70, 100], "vel": [125, 0],
            "cost_gold": 100, "cost_mana": 0, "cost_supply": 1,
            "max_health": 100, "attack": 10, "delay_action": 1000,
            "gain_exp": 25, "range": 20, "action_type": 1},

        3: {"name": "Archer", "size": [40, 60], "vel": [90, 0],
            "cost_gold": 125, "cost_mana": 5, "cost_supply": 1,
            "max_health": 65, "attack": 12, "delay_action": 2000,
            "gain_exp": 30, "range": 200, "action_type": 2},

        4: {"name": "Priest", "size": [50, 70], "vel": [80, 0],
            "cost_gold": 150, "cost_mana": 25, "cost_supply": 1,
            "max_health": 50, "attack": 5, "delay_action": 1500,
            "gain_exp": 40, "range": 10, "action_type": 3},
    },


    # Game (Projectile) --------------------- #
    "projectile": {
        3: {"action_type": 5},
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
