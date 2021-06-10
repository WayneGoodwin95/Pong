import pygame as pg
from menu import *
import event_functions as ef
from settings import Settings
from bat import Bat
from ball import Ball
from obsticle import Obstacle
from scoreboard import Scoreboard
from game_over import GameOverScreen

from collections import OrderedDict
from operator import getitem

import json


class Game():

    def __init__(self):
        pg.init()

        # create variables for game states
        self.running = True
        self.playing = False
        self.game_over_key = False

        self.UP_KEY, self.DOWN_KEY, self.LEFT_KEY, self.RIGHT_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False, False, False

        self.DISPLAY_W, self.DISPLAY_H = 480, 270
        self.mid_w, self.mid_h = self.DISPLAY_W / 2, self.DISPLAY_H / 2
        self.display = pg.Surface((self.DISPLAY_W, self.DISPLAY_H))
        self.window = pg.display.set_mode((self.DISPLAY_W, self.DISPLAY_H), pg.RESIZABLE)
        self.resize_percentage = 0
        self.font_name = '8bit_wonder/8-BIT WONDER.TTF'
        # The default font if dont want to download above font
        #self.font_name = pygame.font.get_default_font()

        self.settings = Settings()

        #colors for objects
        self.darkmode = False
        self.lightmode = True
        self.bat_color = self.settings.BLACK
        self.obstacle_color = self.settings.BLACK
        self.ball_color = self.settings.RED
        self.bg_color = self.settings.WHITE
        self.text_color = self.settings.BLACK
        self.fontsize_large = 24
        self.fontsize_medium = 20
        self.fontsize_small = 16
        self.fontsize_xsmall = 12
        self.scoreboard_height = self.DISPLAY_H / 10
        self.line_color = self.settings.BLACK

        self.file_name = 'usernames.json'
        self.users = self.readfile()
        self.user_list = []
        self.selected_user = 'PLAYER'

        self.lives = 3
        self.score = 0

        self.highscore_list, self.highscore, self.highscore_player = self.get_highscore_list()

        # Initialising game objects
        self.bat = Bat(self)
        self.ball = Ball(self)
        self.obstacle = Obstacle(self)
        self.scoreboard = Scoreboard(self)

        self.menu = Menu(self)
        self.main_menu = MainMenu(self)
        self.options = OptionsMenu(self)
        self.credits = CreditsMenu(self)
        self.create_user = CreateUserMenu(self)
        self.select_user = SelectUserMenu(self)
        self.curr_menu = self.main_menu

        self.game_over_screen = GameOverScreen(self)

        self.dt = 16/1000
        self.timer = 0
        self.magic_timer = 0
        self.magic_time = False

    def game_loop(self):
        while self.playing:
            self.display.fill(self.bg_color)
            self.check_events()
            self.update_game()
            self.window.blit(self.display, (0, 0))
            pg.display.update()
            self.reset_keys()
            pg.time.wait(16)
            self.timer += self.dt
            self.check_magic_time()

    def check_events(self):
        ef.check_events(self)

    def update_game(self):
        ef.check_ball_collisions(self)
        self.ball.move_ball()
        self.bat.move_bat()
        self.scoreboard.prep_scoreboard()
        self.ball.draw_ball()
        self.bat.draw_bat()
        self.scoreboard.draw_scoreboard()
        self.obstacle.draw_obstacle()

    def reset_game(self):
        self.bat.reset_bat()
        self.obstacle.create_rect()
        self.score = 0
        self.magic_time = False
        self.magic_timer = 0
        self.dt = 0
        self.ball.reset_ball()
        self.scoreboard.update_scoreboard()

    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.LEFT_KEY, self.RIGHT_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False, False, False

    def draw_text(self, text, size, x, y, state):
        font = pg.font.Font(self.font_name, size)
        if not state:
            text_surface = font.render(text, True, self.settings.WHITE)
        elif state:
            text_surface = font.render(text, True, self.settings.YELLOW)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.display.blit(text_surface, text_rect)

    def readfile(self):
        try:
            with open(self.file_name) as f_obj:
                users = json.load(f_obj)
        except FileNotFoundError:
            print('reading file not found')
        else:
            f_obj.close()
            print(users)
            return users

    def writefile(self):
        try:
            with open(self.file_name, 'w') as f_obj:
                json.dump(self.users, f_obj, indent=6)
        except FileNotFoundError:
            print('writing file not found')
        else:
            print(self.users)

    def get_highscore_list(self):
        my_dict = self.users.copy()
        sorted_keys = sorted(my_dict, key=lambda x: (my_dict[x]['score']), reverse=True)
        highscore = self.users[sorted_keys[0]]['score']
        highscore_player = self.users[sorted_keys[0]]['username']
        return sorted_keys, highscore, highscore_player

    def check_magic_time(self):
        if self.timer >= 15:
            self.magic_time = True
            self.magic_timer += self.dt
            if self.magic_timer >= 5:
                self.magic_timer = 0
                self.timer = 0
                self.magic_time = False

    def resize_displays(self):
        self.display = pg.Surface((self.DISPLAY_W, self.DISPLAY_H))
        self.window = pg.display.set_mode((self.DISPLAY_W, self.DISPLAY_H), pg.RESIZABLE)

    def resize_fonts(self):
        self.fontsize_large = int(self.fontsize_large * self.resize_percentage)
        self.fontsize_medium = int(self.fontsize_medium * self.resize_percentage)
        self.fontsize_small = int(self.fontsize_small * self.resize_percentage)
        self.fontsize_xsmall = int(self.fontsize_xsmall * self.resize_percentage)


