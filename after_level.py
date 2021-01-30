import pygame
import const 
import main
import login
import menu_pause
import sqlite3


def game_over():
    const.over = True
    while const.over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                # sys.exit()
        const.menu_display.blit(const.instruction_background, (0, 0))
        largetext = pygame.font.Font('freesansbold.ttf', 115)
        TextSurf,TextRect = text_objects("GAME OVER", largetext)
        TextRect.center = ((const.menu_width / 2),(const.menu_height / 4))
        const.menu_display.blit(TextSurf,TextRect)
        show_score()
        button("RESTART", 50, 450, 150, 50, const.BLUE, const.BRIGHT_BLUE,"play")
        button("MAIN MENU", 550, 450, 200, 50, const.RED, const.BRIGHT_RED, "menu")
        pygame.display.update()
        const.clock.tick(30)

def button(msg, x, y, w, h, ic, ac, action = None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(const.menu_display, ac, (x, y, w, h))
        if click[0] == 1 and action != None:
            if action == "play":
                main.score = 0
                const.bg_x = 0
                main.character.x, main.character.y = const.START_CHARACTER_X, const.START_CHARACTER_Y
                main.obstacle.x, main.obstacle.y = const.START_OBSTACLE_X, const.START_OBSTACLE_Y
                main.coin.x, main.coin.y = const.START_COIN_X, const.START_COIN_Y
                main.isJump = False
                main.jump_counter = const.START_JUMP_COUNTER
                constdown()
            elif action == "menu":
                menu_pause.intro_loop()
    else:
        pygame.draw.rect(const.menu_display, ic, (x, y, w, h))
    smalltext = pygame.font.Font("freesansbold.ttf", 20)
    textsurf,textrect = text_objects(msg, smalltext)
    textrect.center = ((x + (w / 2)),(y + (h / 2)))
    const.menu_display.blit(textsurf, textrect)

def text_objects(text,font):
    textsurface = font.render(text, True, const.BLACK)
    return textsurface, textsurface.get_rect()

def show_score():
    con = sqlite3.connect("users.sqlite")
    cur = con.cursor()
    largetext = pygame.font.Font('freesansbold.ttf', 25)
    TextSurf,TextRect = text_objects("Набранное число монет: {}".format(main.score), largetext)
    TextRect.center = ((const.menu_width / 2),(const.menu_height / 2))
    const.menu_display.blit(TextSurf,TextRect)
    if login.user.score <= main.score:
        cur.execute('''UPDATE data
        SET score = ?
        WHERE name = ?''', (main.score, login.user.name)).fetchall()
        con.commit()
        login.user.score = main.score
        largetext = pygame.font.Font('freesansbold.ttf', 50)
        TextSurf,TextRect = text_objects("НОВЫЙ РЕКОРД!", largetext)
        TextRect.center = ((const.menu_width / 2), (const.menu_height / 3 + 15))
        const.menu_display.blit(TextSurf,TextRect)

        largetext = pygame.font.Font('freesansbold.ttf', 25)
        TextSurf,TextRect = text_objects("Рекорд: {}".format(main.score), largetext)
        TextRect.center = ((const.menu_width / 2), (const.menu_height / 2 + 55))
        const.menu_display.blit(TextSurf,TextRect)
    else:        
        largetext = pygame.font.Font('freesansbold.ttf', 25)
        TextSurf,TextRect = text_objects("Рекорд: {}".format(login.user.score), largetext)
        TextRect.center = ((const.menu_width / 2), (const.menu_height / 2 + 80))
        const.menu_display.blit(TextSurf,TextRect)

def constdown():
    const.over = False
    main.score = 0
    const.bg_x = 0
    const.running = True
    main.main()
