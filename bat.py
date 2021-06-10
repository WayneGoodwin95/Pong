import pygame as pg


class Bat():
    """Bat class"""
    def __init__(self, game):

        # Initialise bat properties
        self.game = game
        self.height = self.game.DISPLAY_H / 70
        self.width = self.game.DISPLAY_W / 15
        self.color = self.game.bat_color
        self.moving_right = False
        self.moving_left = False
        self.speed = self.game.DISPLAY_W / 50
        # find screen rect and create bat rect
        self.screen_rect = self.game.display.get_rect()
        self.rect = pg.Rect(self.screen_rect.centerx, (self.screen_rect.bottom - (self.game.DISPLAY_H / 20)),
                            self.width, self.height)

        self.draw_bat()

    def resize(self):
        # find screen rect and create bat rect
        self.screen_rect = self.game.display.get_rect()

        self.height = self.game.DISPLAY_H / 70
        self.width = self.game.DISPLAY_W / 15
        self.speed *= self.game.resize_percentage

        self.rect.centerx *= self.game.resize_percentage
        self.x_pos = self.rect.centerx
        self.rect.update(self.x_pos, 0, self.width, self.height)
        self.rect.centery = int(self.screen_rect.bottom - (self.game.DISPLAY_H / 20))


    def move_bat(self):
        """Update the bats position left or right"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.rect.centerx += self.speed
        if self.moving_left and self.rect.left > self.screen_rect.left:
            self.rect.centerx -= self.speed

    def reset_bat(self):
        """Reset the bats position to the bottom center of screen"""
        self.rect.centerx = self.screen_rect.centerx

    def draw_bat(self):
        """Draw the bat at its current location"""
        pg.draw.rect(self.game.display, self.color, self.rect)