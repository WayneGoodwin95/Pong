import pygame as pg


class GameOverScreen():

    def __init__(self, game):
        self.game = game
        self.bg_color = self.game.settings.BLACK
        self.game_over_msg = 'GAME OVER'
        self.replay_msg = 'PRESS ENTER KEY TO PLAY AGAIN'
        self.margin = self.game.DISPLAY_H / 5
        self.item_height = self.game.DISPLAY_H / 10
        self.top_three_sb = {'1':   {'msg': '',     'x': 0, 'y': 0, 'state': False},
                             '2':   {'msg': '',     'x': 0, 'y': 0, 'state': False},
                             '3':   {'msg': '',     'x': 0, 'y': 0, 'state': False}}

    def run_game_over(self):
        # get the top 3 high scores
        self.top_three()
        self.resize()
        self.game.reset_game()

        while self.game.game_over_key:
            # TO-DO: run game over menu
            self.game.check_events()
            self.game.display.fill(self.bg_color)
            self.game.draw_text(self.game_over_msg, self.game.fontsize_medium, self.game.mid_w, self.margin, False)
            for i in range(1, 4):
                self.game.draw_text(self.top_three_sb[str(i)]['msg'], self.game.fontsize_small, self.top_three_sb[str(i)]['x'],
                                    self.top_three_sb[str(i)]['y'], self.top_three_sb[str(i)]['state'])
            self.game.draw_text(self.replay_msg, self.game.fontsize_xsmall, self.game.mid_w, self.margin + (self.item_height * 6), True)
            self.game.window.blit(self.game.display, (0, 0))
            pg.display.update()
            pg.time.wait(16)

    def top_three(self):
        for i in range(3):
            name = self.game.highscore_list[i]
            score = str(self.game.users[name]['score'])
            msg = name + '   ' + score
            self.top_three_sb[str(i + 1)]['msg'] = msg

    def resize(self):
        self.margin = int(self.game.DISPLAY_H / 5)
        self.item_height = int(self.game.DISPLAY_H / 10)

        for i in range(1, 4):
            self.top_three_sb[str(i)]['x'] = self.game.mid_w
            self.top_three_sb[str(i)]['y'] = self.margin + (self.item_height * (i + 1))



