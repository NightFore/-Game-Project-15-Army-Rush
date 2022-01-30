import pygame
import os
import random
from Settings import *
from os import path
vec = pygame.math.Vector2

"""
    Sprite (Tools)
"""
def load_dict_item(self, item, no_item=None):
    if item in self.object:
        return self.object[item]
    elif item in self.settings:
        return self.settings[item]
    else:
        return no_item

"""
    Initialization
"""
def init_class(self, main, group, dict, data, item, parent, variable, action, surface=False, text=False):
    # Sprite Initialization
    init_sprite(self, main, group, dict, data, item, parent, variable, action)
    if surface:
        init_sprite_surface(self)
    if text:
        init_sprite_text(self)

    # Class Initialization
    self.init()
    self.load()
    self.new()


def init_sprite(self, main, group, dict, data, item, parent, variable, action):
    """
    main, game
    groups, group
    dict, data, item
    object, settings,
    parent, variable, action
    """

    # Classes
    self.main = main.main
    self.game = self.main.game

    # Groups
    self.groups = self.main.all_sprites, group
    pygame.sprite.Sprite.__init__(self, self.groups)

    # Dicts
    self.dict = dict
    self.data = data
    self.item = item

    # Object
    if self.data is not None and self.item is not None:
        self.object = self.dict[self.data][self.item]

        # Settings
        if "settings" in self.object:
            self.settings = self.dict["settings"][self.object["settings"]]
        elif self.data in self.main.settings_dict:
            self.settings = self.main.settings_dict[self.data]
        else:
            print("Settings not initialized")
            self.settings = {}

    # Variables
    self.parent = parent
    self.variable = variable
    self.action = action


def init_sprite_text(self, text=None):
    """
    text, text_pos, text_align
    font, font_color
    """

    # Text
    self.text = text if text is not None else load_dict_item(self, "text", None)
    self.text_pos = load_dict_item(self, "text_pos", init_sprite_text_rect(self.rect))
    self.text_align = load_dict_item(self, "text_align", self.align)

    # Font
    self.font = self.main.font_dict[load_dict_item(self, "font", None)]
    self.font_color = load_dict_item(self, "font_color", None)

    # Check
    if self.font is None:
        print("Font not initialized")
    if self.font_color is None:
        print("Font color not initialized")

# WIP (Change name)
def init_sprite_text_rect(rect):
    return [rect[0] + rect[2] // 2, rect[1] + rect[3] // 2]


"""
    Sprite (Surface)
"""
def init_sprite_surface(self):
    """
    pos, vel, acc,
    size, align, color
    border_size, border_color
    surface, surface_rect, rect
    """

    self.pos = vec(load_dict_item(self, "pos", [0, 0]).copy())
    self.vel = vec(load_dict_item(self, "vel", [0, 0]).copy())
    self.acc = vec(load_dict_item(self, "acc", [0, 0]).copy())

    self.size = load_dict_item(self, "size", [0, 0])
    self.align = load_dict_item(self, "align", "center")
    self.color = load_dict_item(self, "color")

    self.border_size = load_dict_item(self, "border_size", [0, 0])
    self.border_color = load_dict_item(self, "border_color")

    self.surface = pygame.Surface(self.size)
    self.surface_rect = (self.border_size[0], self.border_size[1], self.size[0] - 2*self.border_size[0], self.size[1] - 2*self.border_size[1])
    self.rect = self.main.align_rect(self.surface, self.pos, self.align)

def init_surface(surface, surface_rect, color, border_color=None):
    surface = surface.copy()
    if border_color is not None:
        surface.fill(border_color)
    pygame.draw.rect(surface, color, surface_rect)
    return surface



"""
    Sprite (Fix)
"""
def init_sprite_image(self, image_dir):
    # Pos
    if "pos" in self.settings:
        self.pos = self.settings["pos"].copy()
    else:
        self.pos = [0, 0]

    # Align
    if "align" in self.settings:
        self.align = self.settings["align"]
    else:
        self.align = "center"

    # Color Key
    if "color_key" in self.object:
        self.color_key = self.object["color_key"]
    else:
        self.color_key = None

    # Image
    if "scale_size" in self.object:
        self.scale_size = self.object["scale_size"]
    self.image = load_image(image_dir, self.object["image"], self.color_key, self.scale_size)

    # Surface & Rect
    self.size = self.image.get_size()
    self.surface = self.image
    self.surface_rect = self.surface.get_rect()
    self.rect = self.main.align_rect(self.surface, self.pos, self.align)

    # Time
    self.dt = self.main.dt





"""
    Sprite (Animated)
"""
def init_sprite_image_animated(self):
    # Load
    self.pos = self.settings["pos"]
    self.align = self.settings["align"]
    self.size = self.object["size"]
    if "color_key" in self.object:
        self.color_key = self.object["color_key"]
    else:
        self.color_key = None
    self.image_table = load_tile_table(path.join(self.main.graphic_folder, self.object["image"]), self.size[0], self.size[1], self.color_key)
    self.animation_time = self.settings["animation_time"]
    self.animation_loop = self.settings["animation_loop"]
    self.animation_reverse = self.settings["animation_reverse"]

    # Image
    if "scale_size" in self.object:
        self.scale_size = self.object["scale_size"]
        for table in range(len(self.image_table)):
            for image in range(len(self.image_table[table])):
                self.image_table[table][image] = pygame.transform.scale(self.image_table[table][image], self.scale_size)
    self.index_table, self.index_image = 0, 0
    self.images = self.image_table[self.index_table]
    self.image = self.images[self.index_image]

    # Surface & Rect
    self.surface = self.image
    self.surface_rect = self.surface.get_rect()
    self.rect = self.main.align_rect(self.surface, self.pos, self.align)

    # Time & Animation
    self.dt = self.main.dt
    self.current_time = 0
    self.loop_count = 0
    self.index_loop = 0
    self.index_increment = 1


def update_time_dependent(self):
    self.current_time += self.dt
    if self.current_time >= self.animation_time:
        if self.index_loop == len(self.images)-1:
            self.loop_count += 1
            self.index_loop = 0
            if self.animation_reverse:
                self.index_increment = -self.index_increment
        self.current_time = 0
        self.index_loop += 1
        self.index_image = (self.index_image + self.index_increment) % len(self.images)
        self.image = self.images[self.index_image]
        if not self.animation_loop and self.index_image == 0 and self.loop != 0:
            self.kill()
    self.image = pygame.transform.rotate(self.image, 0)





"""
    Sprite (Rect)
"""


def update_sprite_image(self, image, align=None):
    self.image = image
    if align is not None:
        self.image_align = align
    else:
        self.image_align = self.align
    self.image_rect = self.image.get_rect()
    self.image_rect = self.main.align_rect(self.image, self.pos, self.image_align)


"""
    Image
"""
def convert_image(image, color_key):
    if color_key is not None:
        image = image.convert()
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image

def load_image(image_path, image_dir, color_key=None, scale_size=None):
    if isinstance(image_dir, list):
        images = []
        for image in image_dir:
            image = pygame.image.load(path.join(image_path, image))
            if scale_size is not None:
                image = pygame.transform.scale(image, scale_size)
            images.append(convert_image(image, color_key))
        return images
    else:
        image = pygame.image.load(path.join(image_path, image_dir))
        if scale_size is not None:
            image = pygame.transform.scale(image, scale_size)
        return convert_image(image, color_key)


def load_tile_table(filename, width, height, color_key=None, reverse=False):
    if color_key is None:
        image = pygame.image.load(filename).convert_alpha()
    else:
        image = pygame.image.load(filename).convert()
        image.set_colorkey(color_key)
    image_width, image_height = image.get_size()
    tile_table = []
    if not reverse:
        for tile_y in range(int(image_height / height)):
            line = []
            tile_table.append(line)
            for tile_x in range(int(image_width / width)):
                rect = (tile_x * width, tile_y * height, width, height)
                line.append(image.subsurface(rect))
    else:
        for tile_x in range(int(image_width / width)):
            column = []
            tile_table.append(column)
            for tile_y in range(int(image_height / height)):
                rect = (tile_x * width, tile_y * height, width, height)
                column.append(image.subsurface(rect))
    return tile_table





"""
    Solver
"""
def quadratic_solver(max, x1, x2):
    b = max / ((x2-x1)*(1/2 + 1/(x1**2-x2**2)*((x2**2-3*x1**2)/4 + (x1*x2)/2)))
    a = b*(x2-x1)/(x1**2-x2**2)
    c = -a*x1**2 - b*x1
    return a, b, c

def quadratic_equation(x, coefficients):
    a = coefficients[0]
    b = coefficients[1]
    c = coefficients[2]
    return a*x**2 + b*x + c












"""
    Gameplay functions
"""
def collide_with_walls(sprite, group):
    # WIP - Center only
    sprite.hit_rect.centerx = sprite.pos.x
    hits = pygame.sprite.spritecollide(sprite, group, False, collide_hit_rect)
    if hits:
        if hits[0].rect.centerx > sprite.hit_rect.centerx:
            sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
        if hits[0].rect.centerx < sprite.hit_rect.centerx:
            sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
        sprite.vel.x = 0
        sprite.hit_rect.centerx = sprite.pos.x

    sprite.hit_rect.centery = sprite.pos.y
    hits = pygame.sprite.spritecollide(sprite, group, False, collide_hit_rect)
    if hits:
        if hits[0].rect.centery > sprite.hit_rect.centery:
            sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
        if hits[0].rect.centery < sprite.hit_rect.centery:
            sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
        sprite.vel.y = 0
        sprite.hit_rect.centery = sprite.pos.y
    sprite.rect.center = sprite.hit_rect.center

def collide_hit_rect(one, two):
    return one.rect.colliderect(two.rect)



"""
    Sprite update functions
"""
def update_bobbing(sprite):
    if sprite.bobbing:
        offset = BOB_RANGE * (sprite.tween(sprite.step / BOB_RANGE) - 0.5)
        sprite.rect.centery = sprite.pos.y + offset * sprite.dir
        sprite.step += BOB_SPEED
        if sprite.step > BOB_RANGE:
            sprite.step = 0
            sprite.dir *= -1



"""
    Miscellaneous
"""
def create_grid(locked_pos={}):
    grid = [[(0, 0, 0) for _ in range(10)] for _ in range(20)]
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_pos:
                c = locked_pos[(j, i)]
                grid[i][j] = c
    return grid


def load_file(path, image=False):
    file = []
    for file_name in os.listdir(path):
        if image:
            file.append(pygame.image.load(path + os.sep + file_name).convert_alpha())
        else:
            file.append(path + os.sep + file_name)
    return file


def transparent_surface(width, height, color, border, color_key=(0, 0, 0)):
    surface = pygame.Surface((width, height)).convert()
    surface.set_colorkey(color_key)
    surface.fill(color)
    surface.fill(color_key, surface.get_rect().inflate(-border, -border))
    return surface
