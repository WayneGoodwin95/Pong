import pygame as pg
import json


class Menu():

    def __init__(self, game):
        self.game = game
        self.run_display = True

        self.menu_margin_y = self.game.DISPLAY_H / 5  # 20%
        self.menu_item_height = self.game.DISPLAY_H / 10  # 10%

    def blit_screen(self):
        self.game.window.blit(self.game.display, (0, 0))
        pg.display.update()
        self.game.reset_keys()

    def resize_main(self):
        self.menu_margin_y = self.game.DISPLAY_H / 5  # 20%
        self.menu_item_height = self.game.DISPLAY_H / 10  # 10%


class MainMenu(Menu):

    def __init__(self, game):
        Menu.__init__(self, game)

        self.state = 0

        self.start_y = self.menu_margin_y + self.menu_item_height
        self.create_user_y = self.start_y + self.menu_item_height
        self.select_user_y = self.create_user_y + self.menu_item_height
        self.options_y = self.select_user_y + self.menu_item_height
        self.credits_y = self.options_y + self.menu_item_height
        self.quit_y = self.credits_y + self.menu_item_height

        self.menu_list = [{'name': "Start", 'x': self.game.mid_w, 'y': self.start_y, 'state': True},
                          {'name': "Create User", 'x': self.game.mid_w, 'y': self.create_user_y, 'state': False},
                          {'name': "Select User", 'x': self.game.mid_w, 'y': self.select_user_y, 'state': False},
                          {'name': "Options", 'x': self.game.mid_w, 'y': self.options_y, 'state': False},
                          {'name': "Credits", 'x': self.game.mid_w, 'y': self.credits_y, 'state': False},
                          {'name': "Quit", 'x': self.game.mid_w, 'y': self.quit_y, 'state': False}]

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.settings.BLACK)
            for i in range(len(self.menu_list)):
                self.game.draw_text(self.menu_list[i]['name'], self.game.fontsize_medium, self.menu_list[i]['x'], self.menu_list[i]['y'], self.menu_list[i]['state'])
            self.blit_screen()

    def move_cursor(self):
        if self.game.DOWN_KEY:
            self.menu_list[self.state]['state'] = False
            if self.state >= len(self.menu_list) - 1:
                self.state = 0
            elif not self.state >= len(self.menu_list):
                self.state += 1
            self.menu_list[self.state]['state'] = True
        elif self.game.UP_KEY:
            self.menu_list[self.state]['state'] = False
            if self.state <= 0:
                self.state = len(self.menu_list) - 1
            elif not self.state <= 0:
                self.state -= 1
            self.menu_list[self.state]['state'] = True

    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            if self.state == 0:
                self.game.ball.lives = self.game.lives
                self.game.scoreboard.update_scoreboard()
                self.game.playing = True
            elif self.state == 1:
                self.game.curr_menu = self.game.create_user
            elif self.state == 2:
                self.game.curr_menu = self.game.select_user
                pass
            elif self.state == 3:
                self.game.curr_menu = self.game.options
            elif self.state == 4:
                self.game.curr_menu = self.game.credits
            elif self.state == 5:
                self.game.running = False
            self.run_display = False

    def resize(self):
        self.menu_margin_y = self.game.DISPLAY_H / 5  # 20%
        self.menu_item_height = self.game.DISPLAY_H / 10  # 10%
        self.start_y = self.menu_margin_y + self.menu_item_height
        self.create_user_y = self.start_y + self.menu_item_height
        self.select_user_y = self.create_user_y + self.menu_item_height
        self.options_y = self.select_user_y + self.menu_item_height
        self.credits_y = self.options_y + self.menu_item_height
        self.quit_y = self.credits_y + self.menu_item_height

        for i in range(len(self.menu_list)):
            self.menu_list[i]['x'] = self.game.mid_w

        self.menu_list[0]['y'] = self.start_y
        self.menu_list[1]['y'] = self.create_user_y
        self.menu_list[2]['y'] = self.select_user_y
        self.menu_list[3]['y'] = self.options_y
        self.menu_list[4]['y'] = self.credits_y
        self.menu_list[5]['y'] = self.quit_y


class CreateUserMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

        self.state_x, self.state_y = 0, 0
        self.new_username = ''
        self.textbox_status = True
        self.save_status = False
        self.back_status = False

        self.new_username_y = self.menu_margin_y + self.menu_item_height * 1.5
        self.save_x = self.game.mid_w / 2
        self.back_x = self.save_x * 3
        self.save_back_y = self.new_username_y + self.menu_item_height * 1.5

        self.textbox_rect = pg.Rect(self.game.mid_w, self.new_username_y, self.back_x, self.menu_item_height)
        self.textbox_rect.midleft = (self.save_x / 2, self.new_username_y)
        self.textbox_color = self.game.settings.GREY

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.settings.BLACK)
            self.game.draw_text('Create Username', self.game.fontsize_medium, self.game.mid_w, self.menu_margin_y, False)
            pg.draw.rect(self.game.display, self.textbox_color, self.textbox_rect)
            self.game.draw_text(self.new_username, self.game.fontsize_medium, self.game.mid_w, self.new_username_y, self.textbox_status)
            self.game.draw_text('Save', self.game.fontsize_medium, self.save_x, self.save_back_y, self.save_status)
            self.game.draw_text('Back', self.game.fontsize_medium, self.back_x, self.save_back_y, self.back_status)
            self.blit_screen()

    def move_cursor(self):
        if self.game.DOWN_KEY or self.game.UP_KEY:
            self.change_state(self.state_x, self.state_y, False)
            if self.state_y == 0:
                self.state_y = 1
                self.state_x = 0
            elif self.state_y == 1:
                self.state_y = 0
                self.state_x = 0
            self.change_state(self.state_x, self.state_y, True)
        elif self.game.RIGHT_KEY and self.state_y == 1 or self.game.LEFT_KEY and self.state_y == 1:
            self.change_state(self.state_x, self.state_y, False)
            if self.state_x == 0:
                self.state_x = 1
            elif self.state_x == 1:
                self.state_x = 0
            self.change_state(self.state_x, self.state_y, True)

    def change_state(self, state_x, state_y, status):
        if state_y == 0:
            self.textbox_status = True
        elif state_y == 1:
            self.textbox_status = False
            if state_x == 0:
                self.save_status = status
            elif state_x == 1:
                self.back_status = status

    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            if self.state_x == 0 and self.state_y == 1:
                if self.new_username.upper() in self.game.users:
                    self.new_username = "already exists"
                else:
                    self.game.users[self.new_username.upper()] = {'username': self.new_username.upper(), 'score': 0}
                    self.game.writefile()
                    self.game.highscore_list.append(self.new_username.upper())
                    self.game.curr_menu = self.game.main_menu
                    self.run_display = False
            elif self.state_x == 1 and self.state_y == 1:
                self.new_username = ""
                self.change_state(self.state_x, self.state_y, False)
                self.change_state(0, 0, True)
                self.game.curr_menu = self.game.main_menu
            self.run_display = False
        elif self.game.BACK_KEY:
            if self.textbox_status:
                self.new_username = self.new_username[:-1]
            elif not self.textbox_status:
                self.new_username = ""
                self.change_state(self.state_x, self.state_y, False)
                self.change_state(0, 0, True)
                self.game.curr_menu = self.game.main_menu
                self.run_display = False

    def resize(self):
        self.menu_margin_y = self.game.DISPLAY_H / 5  # 20%
        self.menu_item_height = self.game.DISPLAY_H / 10  # 10%
        self.new_username_y = self.menu_margin_y + self.menu_item_height * 1.5
        self.save_x = self.game.mid_w / 2
        self.back_x = self.save_x * 3
        self.save_back_y = self.new_username_y + self.menu_item_height * 1.5

        self.textbox_rect.update(self.game.mid_w, self.new_username_y, self.back_x, self.menu_item_height)
        self.textbox_rect.midleft = (self.save_x / 2, self.new_username_y)


class SelectUserMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 0
        self.num_dis_users = 3

    def display_menu(self):
        self.run_display = True

        self.game.users = self.game.readfile()
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.settings.BLACK)
            self.game.draw_text('Select Username', self.game.fontsize_medium, self.game.mid_w, self.menu_margin_y, False)
            self.draw_user_list()

            self.blit_screen()

    def draw_user_list(self):
        if self.state < len(self.game.highscore_list) - 2:
            for i in range(3):
                if i == 0:
                    self.status = True
                else:
                    self.status = False
                self.game.draw_text(self.game.highscore_list[self.state + i].upper(), self.game.fontsize_medium, self.game.mid_w, self.menu_margin_y + (self.menu_item_height * 2*(i + 1)), self.status)
        elif self.state == len(self.game.highscore_list) - 2:
            for i in range(3):
                if i == 1:
                    self.status = True
                else:
                    self.status = False
                self.game.draw_text(self.game.highscore_list[self.state - 1 + i].upper(), self.game.fontsize_medium, self.game.mid_w, self.menu_margin_y + (self.menu_item_height * 2*(i + 1)), self.status)
        elif self.state == len(self.game.highscore_list) - 1:
            for i in range(-2, 1):
                if i == 0:
                    self.status = True
                else:
                    self.status = False
                self.game.draw_text(self.game.highscore_list[self.state + i].upper(), self.game.fontsize_medium, self.game.mid_w,
                                    self.menu_margin_y + (self.menu_item_height * 2*(i + 3)), self.status)

    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state < len(self.game.highscore_list) - 1:
                self.state += 1
        elif self.game.UP_KEY:
            if self.state > 0:
                self.state -= 1

    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            self.game.selected_user = self.game.highscore_list[self.state].upper()
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        elif self.game.BACK_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False

    def resize(self):
        self.menu_margin_y = self.game.DISPLAY_H / 5  # 20%
        self.menu_item_height = self.game.DISPLAY_H / 10  # 10%
        pass


class OptionsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

        self.state_y = 0
        self.state_x = 0

        # Create y co-ordinates for titles
        self.theme_y = self.menu_margin_y + self.menu_item_height * 2
        self.theme_options_y = self.theme_y + self.menu_item_height
        self.bat_color_y = self.theme_options_y + self.menu_item_height * 2
        self.bat_options_y = self.bat_color_y + self.menu_item_height

        # find y co-ordinate of each option

        # find center x co-ordinate of each option
        self.lightmode_center_x = self.game.DISPLAY_W / 4
        self.darkmode_center_x = self.lightmode_center_x * 3

        # To get middle of one third of screen we divide by 6
        # mid point of each third is 1/6, 3/6, 5/6
        self.red_bat_center_x = self.game.DISPLAY_W / 6
        self.pink_bat_center_x = self.red_bat_center_x * 3
        self.blue_bat_center_x = self.red_bat_center_x * 5

        self.theme_list = [{'name': "Light Mode", 'x': self.lightmode_center_x, 'y': self.theme_options_y, 'state': True},
                           {'name': "Dark Mode", 'x': self.darkmode_center_x, 'y': self.theme_options_y, 'state': False}]

        self.bat_color_list = [{'name': "Red Bat", 'x': self.red_bat_center_x, 'y': self.bat_options_y, 'state': False},
                               {'name': "Pink Bat", 'x': self.pink_bat_center_x, 'y': self.bat_options_y, 'state': False},
                               {'name': "Blue Bat", 'x': self.blue_bat_center_x, 'y': self.bat_options_y, 'state': False}]

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.settings.BLACK)
            self.game.draw_text('Options', self.game.fontsize_medium, self.game.mid_w, self.menu_margin_y, False)
            self.game.draw_text('Theme', self.game.fontsize_medium, self.game.mid_w, self.theme_y, False)
            self.game.draw_text('Bat Color', self.game.fontsize_medium, self.game.mid_w, self.bat_color_y, False)
            for i in range(len(self.theme_list)):
                self.game.draw_text(self.theme_list[i]['name'], self.game.fontsize_small, self.theme_list[i]['x'], self.theme_list[i]['y'], self.theme_list[i]['state'])
            for i in range(len(self.bat_color_list)):
                self.game.draw_text(self.bat_color_list[i]['name'], self.game.fontsize_small, self.bat_color_list[i]['x'], self.bat_color_list[i]['y'], self.bat_color_list[i]['state'])
            self.blit_screen()

    def move_cursor(self):
        if self.game.DOWN_KEY or self.game.UP_KEY:
            self.change_state(self.state_x, self.state_y, False)
            if self.state_y == 0:
                self.state_y = 1
                self.state_x = 0
            elif self.state_y == 1:
                self.state_y = 0
                self.state_x = 0
            self.change_state(self.state_x, self.state_y, True)
        if self.game.LEFT_KEY and self.state_y == 0 or self.game.RIGHT_KEY and self.state_y == 0:
            self.change_state(self.state_x, self.state_y, False)
            if self.state_x == 0:
                self.state_x = 1
            elif self.state_x == 1:
                self.state_x = 0
            self.change_state(self.state_x, self.state_y, True)
        elif self.game.RIGHT_KEY and self.state_y == 1:
            self.change_state(self.state_x, self.state_y, False)
            if self.state_x >= 2:
                self.state_x = 0
            elif self.state_x <=2:
                self.state_x += 1
            self.change_state(self.state_x, self.state_y, True)
        elif self.game.LEFT_KEY and self.state_y == 1:
            self.change_state(self.state_x, self.state_y, False)
            if self.state_x <= 0:
                self.state_x = 2
            elif self.state_x > 0:
                self.state_x -= 1
            self.change_state(self.state_x, self.state_y, True)

    def change_state(self, state_x, state_y, status):
        if state_y == 0:
            self.theme_list[state_x]['state'] = status
        elif state_y == 1:
            self.bat_color_list[state_x]['state'] = status

    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            if self.state_x == 0 and self.state_y == 0:
                # enable light mode
                self.game.darkmode, self.game.lightmode = False, True
                self.game.bg_color = self.game.settings.WHITE
                self.game.obstacle.color = self.game.settings.BLACK
                self.game.scoreboard.text_color = self.game.settings.BLACK
                self.game.scoreboard.line_color = self.game.settings.BLACK
                self.game.ball.color = self.game.settings.RED
                self.game.bat.bat_color = self.game.settings.BLACK
            if self.state_x == 1 and self.state_y == 0:
                # enable dark mode
                self.game.darkmode, self.game.lightmode = True, False
                self.game.bg_color = self.game.settings.BLACK
                self.game.obstacle.color = self.game.settings.GREEN
                self.game.scoreboard.text_color = self.game.settings.WHITE
                self.game.scoreboard.line_color = self.game.settings.WHITE
                self.game.ball.color = self.game.settings.YELLOW
                self.game.bat.color = self.game.settings.PINK
            elif self.state_x == 0 and self.state_y == 1:
                self.game.bat.color = self.game.settings.DARK_GREEN
            elif self.state_x == 1 and self.state_y == 1:
                self.game.bat.color = self.game.settings.PINK
            elif self.state_x == 2 and self.state_y == 1:
                self.game.bat.color = self.game.settings.BLUE
            self.run_display = False
        elif self.game.BACK_KEY:
            self.change_state(self.state_x, self.state_y, False)
            self.change_state(0, 0, True)
            self.game.curr_menu = self.game.main_menu
            self.run_display = False

    def resize(self):
        self.menu_margin_y = self.game.DISPLAY_H / 5  # 20%
        self.menu_item_height = self.game.DISPLAY_H / 10  # 10%
        # Create y co-ordinates for titles
        self.theme_y = self.menu_margin_y + self.menu_item_height * 2
        self.theme_options_y = self.theme_y + self.menu_item_height
        self.bat_color_y = self.theme_options_y + self.menu_item_height * 2
        self.bat_options_y = self.bat_color_y + self.menu_item_height

        # find y co-ordinate of each option

        # find center x co-ordinate of each option
        self.lightmode_center_x = self.game.DISPLAY_W / 4
        self.darkmode_center_x = self.lightmode_center_x * 3

        # To get middle of one third of screen we divide by 6
        # mid point of each third is 1/6, 3/6, 5/6
        self.red_bat_center_x = self.game.DISPLAY_W / 6
        self.pink_bat_center_x = self.red_bat_center_x * 3
        self.blue_bat_center_x = self.red_bat_center_x * 5

        for i in range(len(self.theme_list)):
            self.theme_list[i]['y'] = self.theme_options_y
        self.theme_list[0]['x'] = self.lightmode_center_x
        self.theme_list[1]['x'] = self.darkmode_center_x
        for i in range(len(self.bat_color_list)):
            self.bat_color_list[i]['y'] = self.bat_options_y
        self.bat_color_list[0]['x'] = self.red_bat_center_x
        self.bat_color_list[1]['x'] = self.pink_bat_center_x
        self.bat_color_list[2]['x'] =self.blue_bat_center_x


class CreditsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 0

    def display_menu(self):
        self.run_display = True

        while self.run_display:
            self.game.check_events()
            if self.game.START_KEY or self.game.BACK_KEY:
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
            self.game.display.fill(self.game.settings.BLACK)
            self.game.draw_text('Credits', self.game.fontsize_medium, self.game.mid_w, self.menu_margin_y, False)
            self.game.draw_text('Made by Wayne Goodwin', self.game.fontsize_small, self.game.mid_w, self.menu_margin_y + self.menu_item_height, False)
            self.blit_screen()

    def resize(self):
        self.menu_margin_y = self.game.DISPLAY_H / 5  # 20%
        self.menu_item_height = self.game.DISPLAY_H / 10  # 10%
        pass
