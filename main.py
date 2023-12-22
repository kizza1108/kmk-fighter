import pygame
from pygame import mixer
from fighter import Fighter
from tkinter import messagebox

winner = ''


def run_fighter_game(player1, player2, stage, p1_name, p2_name, db):

    mixer.init()
    pygame.init()

    # create game window
    SCREEN_WIDTH = 1000
    SCREEN_HEIGHT = 600

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("KMK-Fighting")

    # set framerate
    clock = pygame.time.Clock()
    FPS = 60

    # define colours
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    WHITE = (255, 255, 255)

    # define game variables
    intro_count = 3
    last_count_update = pygame.time.get_ticks()
    score = [0, 0]  # player scores. [P1, P2]
    round_num = 0
    round_over = False
    ROUND_OVER_COOLDOWN = 2000

    # define fighter variables
    WARRIOR_SIZE = 162
    WARRIOR_SCALE = 4
    WARRIOR_OFFSET = [72, 56]
    WARRIOR_DATA = [WARRIOR_SIZE, WARRIOR_SCALE, WARRIOR_OFFSET]
    WIZARD_SIZE = 190
    WIZARD_SCALE = 2
    WIZARD_OFFSET = [72, 44]
    WIZARD_DATA = [WIZARD_SIZE, WIZARD_SCALE, WIZARD_OFFSET]

    HUMAN_SIZE = 126
    HUMAN_SCALE = 3.5
    HUMAN_OFFSET = [62, 34]
    HUMAN_DATA = [HUMAN_SIZE, HUMAN_SCALE, HUMAN_OFFSET]

    SAMURAI_SIZE = 200
    SAMURAI_SCALE = 3
    SAMURAI_OFFSET = [72, 63]
    SAMURAI_DATA = [SAMURAI_SIZE, SAMURAI_SCALE, SAMURAI_OFFSET]

    HUNTRESS_SIZE = 150
    HUNTRESS_SCALE = 4
    HUNTRESS_OFFSET = [55, 49]
    HUNTRESS_DATA = [HUNTRESS_SIZE, HUNTRESS_SCALE, HUNTRESS_OFFSET]

    KING_SIZE = 155
    KING_SCALE = 2
    KING_OFFSET = [72, 30]
    KING_DATA = [KING_SIZE, KING_SCALE, KING_OFFSET]

    # load music and sounds
    pygame.mixer.music.load("assets/audio/music.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1, 0.0, 5000)
    sword_fx = pygame.mixer.Sound("assets/audio/sword.wav")
    sword_fx.set_volume(0.5)
    magic_fx = pygame.mixer.Sound("assets/audio/magic.wav")
    magic_fx.set_volume(0.75)

    # load background image
    bg_image = pygame.image.load("assets/images/background/background" + str(stage) + ".png").convert_alpha()

    # load spritesheets
    human_sheet = pygame.image.load("assets/images/human/Sprites/Human1.png").convert_alpha()
    samurai_sheet = pygame.image.load("assets/images/Samurai/Sprites/samurai.png").convert_alpha()
    huntress_sheet = pygame.image.load("assets/images/Huntress/Sprites/huntress.png").convert_alpha()
    king_sheet = pygame.image.load("assets/images/King/Sprites/king.png").convert_alpha()
    warrior_sheet = pygame.image.load("assets/images/warrior/Sprites/warrior.png").convert_alpha()
    wizard_sheet = pygame.image.load("assets/images/wizard/Sprites/wizard.png").convert_alpha()

    # load victory image
    victory_img = pygame.image.load("assets/images/icons/victory1.png").convert_alpha()

    # define number of steps in each animation
    HUMAN_ANIMATION_STEPS = [10, 8, 3, 7, 6, 3, 10]
    SAMURAI_ANIMATION_STEPS = [8, 8, 2, 6, 6, 4, 6]
    HUNTRESS_ANIMATION_STEPS = [8, 8, 2, 5, 5, 3, 8]
    KING_ANIMATION_STEPS = [6, 8, 2, 6, 6, 4, 10]
    WARRIOR_ANIMATION_STEPS = [4, 8, 2, 4, 4, 3, 8]
    WIZARD_ANIMATION_STEPS = [6, 8, 2, 8, 8, 4, 7]

    # define font
    count_font = pygame.font.Font("assets/fonts/turok.ttf", 80)
    score_font = pygame.font.Font("assets/fonts/turok.ttf", 30)

    # function for drawing text
    def draw_text(text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        screen.blit(img, (x, y))

    # function for drawing background
    def draw_bg():
        scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(scaled_bg, (0, 0))

    # function for drawing fighter health bars
    def draw_health_bar(health, x, y):
        ratio = health / 100
        pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 404, 34))
        pygame.draw.rect(screen, RED, (x, y, 400, 30))
        pygame.draw.rect(screen, GREEN, (x, y, 400 * ratio, 30))

    # create two instances of fighters
    # human
    load_player = [[HUMAN_DATA, human_sheet, HUMAN_ANIMATION_STEPS, sword_fx, 10],
                   [HUNTRESS_DATA, huntress_sheet, HUNTRESS_ANIMATION_STEPS, sword_fx, 12],
                   [KING_DATA, king_sheet, KING_ANIMATION_STEPS, sword_fx, 13],
                   [SAMURAI_DATA, samurai_sheet, SAMURAI_ANIMATION_STEPS, sword_fx, 15],
                   [WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx, 11],
                   [WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx, 16]]
    fighter_1 = Fighter(1, 200, 310, False, load_player[player1][0], load_player[player1][1], load_player[player1][2],
                        load_player[player1][3], load_player[player1][4])
    fighter_2 = Fighter(2, 700, 310, True, load_player[player2][0], load_player[player2][1], load_player[player2][2],
                        load_player[player2][3], load_player[player2][4])

    # game loop
    run = True
    while run:

        clock.tick(FPS)
        if round_num == 5:
            run = False
            if score[0] > score[1]:
                winner = 'Player 1 Wins'
            else:
                winner = 'Player 2 Wins'
            messagebox.showinfo("Winner", winner)
        # draw background
        draw_bg()

        # show player stats
        draw_health_bar(fighter_1.health, 20, 20)
        draw_health_bar(fighter_2.health, 580, 20)
        draw_text("P1: " + str(score[0]), score_font, RED, 20, 60)
        draw_text("P2: " + str(score[1]), score_font, RED, 580, 60)

        # update countdown
        if intro_count <= 0:
            # move fighters
            fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2, round_over)
            fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1, round_over)
        else:
            # display count timer
            draw_text(str(intro_count), count_font, RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
            # update count timer
            if (pygame.time.get_ticks() - last_count_update) >= 1000:
                intro_count -= 1
                last_count_update = pygame.time.get_ticks()

        # update fighters
        fighter_1.update()
        fighter_2.update()

        # draw fighters
        fighter_1.draw(screen)
        fighter_2.draw(screen)

        # check for player defeat
        if not round_over:
            if not fighter_1.alive:
                score[1] += 1
                round_over = True
                round_over_time = pygame.time.get_ticks()
                round_num += 1
                time = round((round_over_time / 1000), 1)
                db.insert_leaderboard([round_num, time, p1_name.upper(), p2_name.upper(), p2_name.upper()])


            elif not fighter_2.alive:
                score[0] += 1
                round_over = True
                round_over_time = pygame.time.get_ticks()
                round_num += 1
                time = round((round_over_time / 1000), 1)
                db.insert_leaderboard([round_num, time, p1_name.upper(), p2_name.upper(), p1_name.upper()])


        else:
            # display victory image
            screen.blit(victory_img, (360, 150))
            if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
                round_over = False
                intro_count = 3
                fighter_1 = Fighter(1, 200, 310, False, load_player[player1][0], load_player[player1][1],
                                    load_player[player1][2],
                                    load_player[player1][3],
                                    load_player[player1][4])
                fighter_2 = Fighter(2, 700, 310, True, load_player[player2][0], load_player[player2][1],
                                    load_player[player2][2],
                                    load_player[player2][3],
                                    load_player[player2][4])
        # event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # update display
        pygame.display.update()

    # exit pygame
    pygame.quit()


