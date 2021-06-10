import pygame as pg


def check_events(game):
    for event in pg.event.get():
        if event.type == pg.QUIT or event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            game.running, game.playing = False, False
            game.curr_menu.run_display = False
            game.game_over_key = False
        elif event.type == pg.VIDEORESIZE:
            check_resize(game, event)
        if game.curr_menu.run_display:
            check_menu_events(game, event)
        elif game.playing:
            check_game_events(game, event)
        elif game.game_over_key:
            check_replay(game, event)


# fix curr menu so that it has to be create user
def check_menu_events(game, event):
    if event.type == pg.KEYDOWN:
        if event.key == pg.K_RETURN:
            game.START_KEY = True
        if event.key == pg.K_BACKSPACE:
            game.BACK_KEY = True
        if event.key == pg.K_DOWN:
            game.DOWN_KEY = True
        if event.key == pg.K_UP:
            game.UP_KEY = True
        if event.key == pg.K_RIGHT:
            game.RIGHT_KEY = True
        if event.key == pg.K_LEFT:
            game.LEFT_KEY = True
        if game.curr_menu == game.create_user and not event.key == pg.K_BACKSPACE:
            if game.curr_menu.textbox_status:
                if len(game.curr_menu.new_username) < 16:
                    game.curr_menu.new_username += event.unicode


def check_game_events(game, event):
    if event.type == pg.KEYDOWN:
        if event.key == pg.K_p:
            # TO_DO - Pause Game and open in_game_menu
            pass
        if event.key == pg.K_a or event.key == pg.K_LEFT:
            game.bat.moving_left = True
        if event.key == pg.K_d or event.key == pg.K_RIGHT:
            game.bat.moving_right = True
    elif event.type == pg.KEYUP:
        if event.key == pg.K_a or event.key == pg.K_LEFT:
            game.bat.moving_left = False
        if event.key == pg.K_d or event.key == pg.K_RIGHT:
            game.bat.moving_right = False


def check_replay(game, event):
    if event.type == pg.KEYDOWN:
        if event.key == pg.K_RETURN:
            print('Replay')
            game.game_over_key = False
            game.playing = True
            game.game_loop()
        elif event.key == pg.K_BACKSPACE:
            game.game_over_key = False
            game.playing = False
            game.curr_menu = game.main_menu
            game.curr_menu.run_display


def check_resize(game, event):
    """Resize the screen for user input"""
    # get new screen width and height
    w, h = event.dict['size']
    # place aspect ratios in settings
    w_ratio = 16
    h_ratio = 9
    #find how many pixels in new screen size
    w_pxls = w / w_ratio
    h_pxls = h / h_ratio

    # ensure aspect ratio is maintained
    if w_pxls < h_pxls:
        w = int(h_pxls * w_ratio)
    elif h_pxls < w_pxls:
        h = int(w_pxls * h_ratio)
    if w <= 400 and h <= 225:
        print('screen lower than minimum')
        w = 400
        h = 225

    print('w: ' + str(w))
    print('h: ' + str(h))
    game.resize_percentage = round(w / game.DISPLAY_W, 2)
    print('rp: ' + str(game.resize_percentage))
    game.DISPLAY_H = h
    game.DISPLAY_W = w
    game.resize_displays()
    game.mid_h = h / 2
    game.mid_w = w / 2
    game.resize_fonts()


    game.ball.resize()
    game.bat.resize()
    game.obstacle.resize()
    game.scoreboard.resize()

    game.menu.resize_main()
    game.main_menu.resize()
    game.options.resize()
    game.credits.resize()
    game.create_user.resize()
    game.select_user.resize()
    game.game_over_screen.resize()


def check_ball_collisions(game):
    """Check if the ball touches any of the screen edges or collides with the bat"""
    screen_rect = game.display.get_rect()
    # Change x direction if the ball touches left or right side of screen
    if game.ball.rect.right >= screen_rect.right or game.ball.rect.left <= screen_rect.left:
        game.ball.x_velocity *= -1
        game.ball.x_dir *= -1

    # if the ball touches the bottom of the screen
    if game.ball.rect.bottom >= screen_rect.bottom:
        print('collision')
        if game.ball.lives >= 1:
            game.ball.lives -= 1
            game.scoreboard.update_scoreboard()
            game.bat.reset_bat()
            game.ball.new_life()
        if game.ball.lives == 0:
            if game.score > game.users[game.selected_user]['score']:
                game.users[game.selected_user]['score'] = game.score
                game.writefile()
            game.scoreboard.update_scoreboard()
            game.playing = False
            game.game_over_key = True
            game.game_over_screen.run_game_over()


    # ball collides with bat change the y direction
    if game.ball.rect.colliderect(game.bat.rect):
        if game.ball.rect.top <= game.bat.rect.bottom:
            game.ball.y_velocity *= -1
            game.ball.y_dir *= -1
            game.ball.rect.top = game.bat.rect.bottom + game.ball.radius
        # if game.ball.rect.bottom >= game.bat.rect.top:
        #     game.ball.y_velocity *= -1
        #     game.ball.y_dir *= -1
        #     game.ball.rect.bottom = game.bat.rect.top - game.ball.radius
        elif game.ball.rect.left <= game.bat.rect.right:
            game.ball.x_velocity *= -1
            game.ball.x_dir *= -1
            game.ball.rect.left = game.bat.rect.left - game.ball.radius
        elif game.ball.rect.right >= game.bat.rect.left:
            game.ball.x_velocity *= -1
            game.ball.x_dir *= -1
            game.ball.rect.right = game.bat.rect.left + game.ball.radius

    # if the ball hits the top of screen upate direction and add point
    if game.ball.rect.top <= game.DISPLAY_H * 0.10:
        game.ball.y_velocity *= -1
        game.ball.y_dir *= -1
        if game.score % 3 == 0:
            game.ball.increment_speed()
        if game.magic_time:
            game.score += 2
        elif not game.magic_time:
            game.score += 1
        if game.highscore < game.score:
            game.highscore = game.score
        game.scoreboard.update_scoreboard()

    if game.ball.rect.colliderect(game.obstacle.rect):
        if game.ball.rect.top or game.ball.rect.right or game.ball.rect.left <= game.obstacle.rect.bottom:
            game.ball.y_velocity *= -1
            game.ball.y_dir *= -1
            game.ball.rect.top = game.obstacle.rect.bottom + game.ball.radius
        elif game.ball.rect.bottom or game.ball.rect.right or game.ball.rect.left >= game.obstacle.rect.top:
            game.ball.y_velocity *= -1
            game.ball.y_dir *= -1
            game.ball.rect.bottom = game.obstacle.rect.top - game.ball.radius
        elif game.ball.rect.left or game.ball.rect.top or game.ball.rect.bottom <= game.obstacle.rect.right:
            game.ball.x_velocity *= -1
            game.ball.x_dir *= -1
            game.ball.rect.left = game.obstacle.rect.left - game.ball.radius
        elif game.ball.rect.right or game.ball.rect.top or game.ball.rect.bottom >= game.obstacle.rect.left:
            game.ball.x_velocity *= -1
            game.ball.x_dir *= -1
            game.ball.rect.right = game.obstacle.rect.left + game.ball.radius
