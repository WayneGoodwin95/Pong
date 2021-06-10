import pygame as pg


class Scoreboard():

    def __init__(self, game):
        """Initialise button attributes."""
        self.game = game
        self.screen_rect = self.game.display.get_rect()

        # Set the dimensions and properties of the button.
        self.width = self.game.DISPLAY_W
        self.height = self.game.scoreboard_height
        self.bg_color = self.game.bg_color
        self.text_color = self.game.text_color
        self.fontsize = self.game.fontsize_medium
        self.font = pg.font.SysFont(None, self.fontsize)
        self.line_color = self.game.line_color
        self.start_line = (0, self.height)
        self.end_line = (self.width, self.height)
        self.line_width = int(self.game.DISPLAY_H / 200)

        # Build the button's rect object and place above button.
        self.rect = pg.Rect(0, 0, self.width, self.height)

        # The button message needs to be prepped only once
        self.score_msg = 'Score: ' + str(self.game.score)
        self.highscore_msg = 'High Score: ' + str(self.game.highscore)
        self.player_msg = self.game.selected_user + ': ' + str(self.game.ball.lives)

    def resize(self):
        self.screen_rect = self.game.display.get_rect()

        # Set the dimensions and properties of the button.
        self.width = self.game.DISPLAY_W
        self.height = int(self.game.DISPLAY_H / 10)
        self.fontsize = self.game.fontsize_medium
        self.font = pg.font.SysFont(None, self.fontsize)
        self.start_line = (0, self.height)
        self.end_line = (self.width, self.height)
        self.line_width = int(self.game.DISPLAY_H / 200)

        # Build the button's rect object and place above button.
        self.rect.update(0, 0, self.width, self.height)

    def update_scoreboard(self):
        self.score_msg = 'Score: ' + str(self.game.score)
        self.highscore_msg = 'High Score: ' + str(self.game.highscore)
        self.player_msg = self.game.selected_user + ': ' + str(self.game.ball.lives)

    def prep_scoreboard(self):
        """Turn msg into a rendered image and center text on the button."""
        self.score_msg_image = self.font.render(self.score_msg, True, self.text_color, None)
        self.score_msg_image_rect = self.score_msg_image.get_rect()
        self.score_msg_image_rect.midright = self.rect.midright

        """Turn msg into a rendered image and center text on the button."""
        self.highscore_msg_image = self.font.render(self.highscore_msg, True, self.text_color, None)
        self.highscore_msg_image_rect = self.highscore_msg_image.get_rect()
        self.highscore_msg_image_rect.center = self.rect.center

        """Turn msg into a rendered image and center text on the button."""
        self.player_msg_image = self.font.render(self.player_msg, True, self.text_color, None)
        self.player_msg_image_rect = self.player_msg_image.get_rect()
        self.player_msg_image_rect.midleft = self.rect.midleft

    def draw_scoreboard(self):
        # Draw blank button and then draw message.
        self.game.display.blit(self.score_msg_image, self.score_msg_image_rect)
        self.game.display.blit(self.highscore_msg_image, self.highscore_msg_image_rect)
        self.game.display.blit(self.player_msg_image, self.player_msg_image_rect)
        pg.draw.line(self.game.display, self.line_color, self.start_line, self.end_line, self.line_width)