import pygame as pg
import random


class Obstacle():
    def __init__(self, game):
        self.game = game
        self.color = self.game.obstacle_color

        self.y = self.game.DISPLAY_H / 3
        self.height = int(self.game.DISPLAY_H / 200)
        self.length = 0
        self.lowest_x = 0
        self.highest_x = int(self.game.DISPLAY_W - (self.game.DISPLAY_W / 5))
        self.longest_length = int(self.game.DISPLAY_W / 5)
        self.shortest_length = int(self.game.DISPLAY_W / 10)
        self.start_x = 0
        self.end_x = 0

        self.create_rect()

    def create_rect(self):
        self.start_x = random.randrange(self.lowest_x, self.highest_x)
        self.length = random.randrange(self.shortest_length, self.longest_length)
        self.end_x = self.start_x + self.length
        self.center_x = int(self.start_x + (self.length / 2))
        self.center_y = self.y
        self.rect = pg.Rect(self.center_x, self.center_y, self.length, self.height)

    def resize(self):
        self.y = int(self.game.DISPLAY_H / 3)
        self.height = int(self.game.DISPLAY_H / 200)
        self.highest_x = int(self.game.DISPLAY_W - (self.game.DISPLAY_W / 5))
        self.longest_length = int(self.game.DISPLAY_W / 5)
        self.shortest_length = int(self.game.DISPLAY_W / 10)
        if not self.game.playing:
            self.create_rect()
        elif self.game.playing:
            self.start_x = int(self.start_x * self.game.resize_percentage)
            self.end_x = int(self.end_x * self.game.resize_percentage)
            self.length = self.end_x - self.start_x
            self.center_x = int(self.start_x + (self.length / 2))
            self.center_y = self.y
            self.rect.update(self.center_x, self.center_y, self.length, self.height)

    def draw_obstacle(self):
        """Draw the bat at its current location"""
        pg.draw.rect(self.game.display, self.color, self.rect)