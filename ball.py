import pygame as pg
import random


class Ball():
    """ball class"""
    def __init__(self, game):
        self.game = game
        # get the screen rect
        self.screen_rect = self.game.display.get_rect()

        # Initialise Ball properties
        self.radius = self.game.DISPLAY_H / 40
        self.diameter = self.radius * 2
        self.color = self.game.settings.RED
        self.magic_time_color = self.game.settings.DARK_GREEN
        self.x_pos = random.randrange(100, self.game.DISPLAY_W - 100)
        self.y_pos = self.game.DISPLAY_H * 0.15
        self.x_dir = random.choice([-1, 1])
        self.y_dir = 1

        self.lives = self.game.lives

        self.speed_increase = 1.1

        # Initialise the ball velocity
        self.speed = self.game.DISPLAY_W / 200
        self.curr_speed = self.speed
        self.x_velocity = self.x_dir * self.curr_speed
        self.y_velocity = self.y_dir * self.curr_speed

        # create ball rect and find the center
        self.rect = pg.Rect(self.x_pos, self.y_pos, self.diameter, self.diameter)
        self.center = self.rect.center

    def increment_speed(self):
        self.x_velocity *= self.speed_increase
        self.y_velocity *= self.speed_increase

    def resize(self):
        print('x vel: ' + str(self.x_velocity))
        print('y vel: ' + str(self.y_velocity))
        self.radius *= self.game.resize_percentage
        self.diameter *= self.game.resize_percentage
        self.screen_rect = self.game.display.get_rect()
        self.speed = self.speed * self.game.resize_percentage
        print('speed: ' + str(self.speed))
        self.curr_speed = self.curr_speed * self.game.resize_percentage
        print('curr speed: ' + str(self.curr_speed))
        print('xdir: ' + str(self.x_dir))
        print('ydir: ' + str(self.y_dir))
        self.x_velocity = self.x_dir * self.curr_speed
        self.y_velocity = self.y_dir * self.curr_speed
        print('x vel: ' + str(self.x_velocity))
        print('y vel: ' + str(self.y_velocity))

        if not self.game.playing:
            self.x_pos = random.randrange(100, self.game.DISPLAY_W - 100)
            self.y_pos = int(self.game.DISPLAY_H * 0.15)
        elif self.game.playing:
            self.x_pos = int(self.x_pos * self.game.resize_percentage)
            self.y_pos = int(self.y_pos * self.game.resize_percentage)

        self.rect.update(self.x_pos, self.y_pos, self.diameter, self.diameter)
        self.center = self.rect.center
        self.rect.centerx, self.rect.centery = self.x_pos, self.y_pos

    def move_ball(self):
        """Update the balls position and rect"""
        self.x_pos += self.x_velocity
        self.y_pos += self.y_velocity
        self.rect.centerx = self.x_pos
        self.rect.centery = self.y_pos

    def reset_ball(self):
        self.x_pos = random.randrange(100, self.game.DISPLAY_W - 100)
        self.y_pos = self.game.DISPLAY_H * 0.15
        self.rect.centerx = self.x_pos
        self.rect.centery = self.y_pos
        self.x_velocity = random.choice([-1, 1]) * self.speed
        self.y_velocity = self.speed
        self.lives = self.game.lives

    def new_life(self):
        self.x_pos = random.randrange(100, self.game.DISPLAY_W - 100)
        self.y_pos = self.y_pos = self.game.DISPLAY_H * 0.15
        self.x_dir *= random.choice([-1, 1])
        self.y_dir = 1
        self.x_velocity = self.x_dir *self.curr_speed
        self.y_velocity = self.y_dir * self.curr_speed

    def draw_ball(self):
        """Draw the ball to the screen"""
        if self.game.magic_time:
            pg.draw.circle(self.game.display, self.magic_time_color, self.rect.center,
                           self.radius, 0)
        else:
            pg.draw.circle(self.game.display, self.color, self.rect.center,
                           self.radius, 0)