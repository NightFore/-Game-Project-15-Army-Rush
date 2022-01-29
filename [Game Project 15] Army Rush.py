import pygame
import random
from pygame.locals import *
from os import path
from Main import *
from Class import *
from Function import *
from Settings import *
from ScaledGame import *
vec = pygame.math.Vector2

class Main:
    def __init__(self):
        self.main = self
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.mixer.init()
        pygame.init()
        random.seed()
        self.load()
        self.new()
        self.game = Game(self)
        self.update_menu()

    def load(self):
        # Dictionaries
        self.main_dict = MAIN_DICT
        self.game_dict = self.main_dict["game"]
        self.settings_dict = self.main_dict["settings"]
        self.background_dict = self.main_dict["background"]
        self.music_dict = self.main_dict["music"]
        self.sound_dict = self.main_dict["sound"]
        self.font_dict = self.main_dict["font"]
        self.menu_dict = self.main_dict["menu"]
        self.button_dict = self.main_dict["button"]

        # Directories
        self.game_folder = path.dirname(__file__)
        self.data_folder = path.join(self.game_folder, "data")
        self.font_folder = path.join(self.data_folder, "font")
        self.graphic_folder = path.join(self.data_folder, "graphic")
        self.item_folder = path.join(self.data_folder, "item")
        self.music_folder = path.join(self.data_folder, "music")
        self.se_folder = path.join(self.data_folder, "sound")

        # Sound Effects
        self.sound_effects = {}
        for sound in self.sound_dict:
            self.sound_effects[sound] = pygame.mixer.Sound(path.join(self.se_folder, self.sound_dict[sound]))
            self.sound_effects[sound].set_volume(self.sound_volume / 100)

        # Fonts
        self.font = pygame.font.Font(None, 100)
        for font in self.font_dict:
            font_ttf = self.font_dict[font]["ttf"]
            font_size = self.font_dict[font]["size"]
            self.font_dict[font] = pygame.font.Font(path.join(self.font_folder, font_ttf), font_size)

        # Game Settings
        self.project_title = self.game_dict["project_title"]
        self.screen_size = self.screen_width, self.screen_height = self.game_dict["screen_size"]
        self.FPS = self.game_dict["FPS"]
        self.gameDisplay = ScaledGame(self.project_title, self.screen_size, self.FPS)

        # Volume Settings
        self.default_music_volume = self.game_dict["default_music_volume"]
        self.music_volume = self.default_music_volume
        self.default_sound_volume = self.game_dict["default_sound_volume"]
        self.sound_volume = self.default_sound_volume
        pygame.mixer.music.set_volume(self.music_volume/100)

        # Key Settings
        self.key_delay, self.key_interval = self.game_dict["key_repeat"]
        pygame.key.set_repeat(self.key_delay, self.key_interval)

    def new(self):
        # Game Initialization
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.playing = True
        self.menu = "main_menu"

        # Settings
        self.background_image = None
        self.background_color = None
        self.music = None

        # Pause
        self.paused = False
        self.pause_check = False
        self.dim_screen = pygame.Surface(self.gameDisplay.get_size()).convert_alpha()
        self.dim_screen.fill((100, 100, 100, 120))

        # Debug
        self.debug_color = CYAN
        self.debug_mode = True

    # Game Loop ----------------------- #
    def run(self):
        while self.playing:
            self.dt = self.gameDisplay.clock.tick(self.FPS) / 1000
            self.events()
            if not self.paused:
                self.update()
            self.draw()
        self.quit_game()

    def quit_game(self):
        pygame.quit()
        quit()

    def events(self):
        # Click: Left, Middle, Right, Scroll Up, Scroll Down
        self.click = [None, False, False, False, False, False]

        self.event = pygame.event.get()
        for event in self.event:
            # Mouse position & Rescaling to screen size
            self.mouse = pygame.mouse.get_pos()
            if self.gameDisplay.factor_w != 1 or self.gameDisplay.factor_h != 1:
                mouse_w = int((self.mouse[0] - self.gameDisplay.game_gap[0]) / self.gameDisplay.factor_w)
                mouse_h = int(self.mouse[1] / self.gameDisplay.factor_h)
                self.mouse = (mouse_w, mouse_h)


            # Mouse Click
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.click[event.button] = True

            # Keyboard
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Quit Game (Escape)
                    self.quit_game()
                if event.key == pygame.K_p:
                    # Pause
                    self.paused = True
                    pygame.mixer.music.pause()
                if event.key == pygame.K_h:
                    # Debug Mode
                    self.debug_mode = not self.debug_mode
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_p:
                    # Unpause
                    if not self.pause_check:
                        self.pause_check = True
                    else:
                        self.pause_check = False
                        self.paused = False
                        pygame.mixer.music.unpause()

            # Quit Game (Close Button)
            if event.type == pygame.QUIT:
                self.quit_game()

    def update(self):
        self.game.update()
        self.all_sprites.update()

    def draw(self):
        # Background ------------------ #
        if self.background_image is not None:
            self.gameDisplay.blit(self.background_image, (0, 0))
        if self.background_color is not None:
            self.gameDisplay.fill(self.background_color)

        # Game ------------------------ #
        self.game.draw()

        # Sprite --------------------- #
        for sprite in self.all_sprites:
            sprite.draw()
            if self.debug_mode:
                pygame.draw.rect(self.gameDisplay, CYAN, sprite.rect, 1)

        # Pause ----------------------- #
        if self.paused:
            self.gameDisplay.blit(self.dim_screen, (0, 0))
            self.draw_text("Game Paused", self.font, RED, (self.screen_width // 2, self.screen_height // 2), align="center")

        # Update ---------------------- #
        self.gameDisplay.update(self.event)

    def update_menu(self, menu=None):
        if menu is None:
            self.update_menu(self.menu)
        else:
            self.menu = menu
            self.clear_sprites()
            self.update_background(self.menu_dict[self.menu]["background"])
            self.update_music(self.menu_dict[self.menu]["music"])
            self.update_button(self.button_dict[self.menu], data=self.menu)

    def update_background(self, background):
        if isinstance(background, str):
            background = self.background_dict[background]
        if background is not None:
            if background["color"] is not None:
                self.background_color = background["color"]
            if background["image"] is not None:
                self.background_image = load_image(self.graphics_folder, background["image"])

    def update_music(self, music):
        if isinstance(music, str):
            music = self.music_dict[music]
        if music is not None:
            music = path.join(self.music_folder, music)
            if self.music != music:
                self.music = music
                pygame.mixer.music.load(self.music)
                pygame.mixer.music.play(-1)

    def update_button(self, buttons, data):
        for button in buttons:
            Button(self, self.game.buttons, self.button_dict, data=data, item=button)

    def update_volume(self, dv=0):
        self.music_volume = min(max(0, self.music_volume + dv), 100)
        pygame.mixer.music.set_volume(self.music_volume/100)

    def clear_sprites(self):
        for sprite in self.all_sprites:
            sprite.kill()

    def align_rect(self, surface, pos, align):
        rect = surface.get_rect()
        pos = (int(pos[0]), int(pos[1]))
        if align == "nw":
            rect.topleft = pos
        if align == "ne":
            rect.topright = pos
        if align == "sw":
            rect.bottomleft = pos
        if align == "se":
            rect.bottomright = pos
        if align == "n":
            rect.midtop = pos
        if align == "s":
            rect.midbottom = pos
        if align == "e":
            rect.midright = pos
        if align == "w":
            rect.midleft = pos
        if align == "center":
            rect.center = pos
        return rect

    def draw_text(self, text, font, color, pos, align="nw"):
        if text is not None and font is not None:
            if not isinstance(text, str):
                text = str(text)
            text_surface = font.render(text, True, color)
            text_rect = self.align_rect(text_surface, pos, align)
            self.gameDisplay.blit(text_surface, text_rect)

            # Debug Mode
            if self.debug_mode:
                pygame.draw.rect(self.gameDisplay, CYAN, text_rect, 1)

    def draw_surface(self, align, rect, color, border_size=[0, 0], border_color=None):
        # Initialization
        x, y, w, h = int(rect[0]), int(rect[1]), int(rect[2]), int(rect[3])
        border_w, border_h = border_size[0], border_size[1]
        if w - 2*border_w <= 0 or h - 2*border_h <= 0:
            w = max(w, 2*border_w + 1)
            h = max(h, 2*border_h + 1)

        # Border Surface
        if border_size != [0, 0] and border_color is not None:
            surface = pygame.Surface((w, h))
            surface_rect = self.align_rect(surface, (x, y), align)
            surface.fill(border_color)
            self.gameDisplay.blit(surface, surface_rect)

        # Main Surface
        surface = pygame.Surface((w - 2*border_w, h - 2*border_h))
        surface_rect = self.align_rect(surface, (x + border_w, y + border_h), align)
        surface.fill(color)
        self.gameDisplay.blit(surface, surface_rect)

    def update_sprite_rect(self, sprite, x=None, y=None):
        if x is None:
            x = sprite.pos[0]
        if y is None:
            y = sprite.pos[1]
        sprite.pos = [x, y]
        sprite.rect = self.align_rect(sprite.surface, (int(sprite.pos[0]), int(sprite.pos[1])), sprite.align)

m = Main()
while True:
    m.run()
