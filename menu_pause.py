import pygame
import const 
import main, login
import registration

enter = True

def intro_loop():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                sys.exit()
        const.menu_display.blit(const.intro_background,(0, 0))
        pygame.draw.rect(const.menu_display, const.BRIGHT_YELLOW, (150, 40, 500, 110))
        largetext = pygame.font.Font('freesansbold.ttf', 115)
        TextSurf,TextRect = text_objects("RUNNER", largetext)
        TextRect.center = (400, 100)
        const.menu_display.blit(TextSurf, TextRect)

        button("don't have an account? create a new", 300, 350, 200, 30, const.YELLOW, const.BRIGHT_YELLOW,"reg")
        button("LOGIN", 350, 290, 100, 40, const.YELLOW, const.BRIGHT_YELLOW,"login")
        button("START", 100, 520, 100, 50, const.GREEN, const.BRIGHT_GREEN,"play")
        button("QUIT", 600, 520, 100, 50, const.RED, const.BRIGHT_RED, "quit")
        button("INSTRUCTION", 300, 520, 200, 50, const.BLUE, const.BRIGHT_BLUE,"intro")
        login.name_login()
        login.password_login()
        registration.registration()
        error()
        pygame.display.update()
        const.clock.tick(50)

def button(msg, x, y, w, h, ic, ac, action = None):
    global enter
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(const.menu_display, ac, (x, y, w, h))
        if click[0] == 1 and action != None:
            if action == "play":
                if login.user.name == '':
                    enter = False
                else:
                    main.score = 0
                    const.bg_x = 0
                    main.character.x, main.character.y = const.START_CHARACTER_X, const.START_CHARACTER_Y
                    main.obstacle.x, main.obstacle.y = const.START_OBSTACLE_X, const.START_OBSTACLE_Y
                    main.coin.x, main.coin.y = const.START_COIN_X, const.START_COIN_Y
                    main.isJump = False
                    main.jump_counter = const.START_JUMP_COUNTER
                    constdown()
            if action == "quit":
                pygame.quit()
                quit()
                sys.exit()
            elif action == "intro":
                introduction()
            elif action == "menu":
                intro_loop()
            elif action == "login":
                const.login_pressed = True
            elif action == "reg":
                const.registration_pressed = True
            elif action == "pause":
                paused()
            elif action == "unpause":
                unpaused()
                constdown()
    else:
        pygame.draw.rect(const.menu_display, ic, (x, y, w, h))
    if msg == "don't have an account? create a new":
        smalltext = pygame.font.Font("freesansbold.ttf", 10)
    else:
        smalltext = pygame.font.Font("freesansbold.ttf", 20)
    textsurf, textrect = text_objects(msg, smalltext)
    textrect.center = ((x + (w / 2)),(y + (h / 2)))
    const.menu_display.blit(textsurf, textrect)

def error():
    global enter
    if not enter:
        login.status_label('Вы не вошли в аккаунт.')
    enter = True

def introduction():
    introduction = True
    while introduction:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                #sys.exit()
        const.menu_display.blit(const.instruction_background,(0, 0))
        largetext = pygame.font.Font('freesansbold.ttf', 80)
        smalltext = pygame.font.Font('freesansbold.ttf', 20)
        mediumtext = pygame.font.Font('freesansbold.ttf', 40)

        textSurf, textRect = text_objects("В этой игре самые простые правила:", smalltext)
        textRect.center = ((350),(200))
        TEXTSURF, TEXTRECT = text_objects("Нужно собирать монетки, избегать кактусов и наслаждаться!", smalltext)
        TEXTRECT.center = ((350),(250))
        TextSurf, TextRect = text_objects("INSTRUCTION", largetext)
        TextRect.center = ((400),(100))
        const.menu_display.blit(TextSurf,TextRect)
        const.menu_display.blit(TEXTSURF, TEXTRECT)
        const.menu_display.blit(textSurf,textRect)

        stextSurf,stextRect = text_objects("Space: Прыжок", smalltext)
        stextRect.center = ((400),(400))
        ptextSurf,ptextRect = text_objects("P : Пауза", smalltext)
        ptextRect.center = ((150),(375))
        const.menu_display.blit(stextSurf, stextRect)
        const.menu_display.blit(ptextSurf, ptextRect)
        button("BACK", 600, 450, 100, 50, const.BLUE,const.BRIGHT_BLUE, "menu")
        pygame.display.update()
        const.clock.tick(30)

def paused():
    while const.pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                # sys.exit()
        const.menu_display.blit(const.instruction_background, (0, 0))
        largetext = pygame.font.Font('freesansbold.ttf', 115)
        TextSurf,TextRect = text_objects("PAUSED", largetext)
        TextRect.center = ((const.menu_width / 2),(const.menu_height / 2))
        const.menu_display.blit(TextSurf,TextRect)
        button("CONTINUE", 100, 450, 150, 50,const.GREEN, const.BRIGHT_GREEN,"unpause")
        button("RESTART", 550, 450, 150, 50, const.BLUE, const.BRIGHT_BLUE,"play")
        button("MAIN MENU", 300, 450, 200, 50, const.RED, const.BRIGHT_RED, "menu")
        pygame.display.update()
        const.clock.tick(30)

def unpaused():
    const.pause = False

def text_objects(text,font):
    textsurface = font.render(text, True, const.BLACK)
    return textsurface, textsurface.get_rect()

def message_display(text):
    largetext = pygame.font.Font("freesansbold.ttf",80)
    textsurf,textrect = text_objects(text,largetext)
    textrect.center = ((const.menu_width / 2), (const.menu_height / 2))
    const.menu_display.blit(textsurf,textrect)
    pygame.display.update()
    # time.sleep(3)
    game_loop()

def game_loop():
    bumped = False
    while not bumped:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        const.pause = True
        paused()
        pygame.display.update()
        const.clock.tick(60)

def constdown():
    const.running = True
    main.main()
# intro_loop()
# game_loop()
