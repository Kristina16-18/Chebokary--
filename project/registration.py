import pygame
import time
import sqlite3
import const 
import main, login, menu_pause

start_input_for_name = False
start_input_for_password = False
start_input_for_repeat_password = False
user_name = ''
user_password = ''
user_repeat_password = ''
text_tick_name = -40
text_tick_password = -40
text_tick_repeat_password = -40
name_error = False
password_error = False
repeat_password_error = False

def registration():
    while const.registration_pressed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                sys.exit()
        const.registration_screen.blit(const.intro_background,(0, 0))
        pygame.draw.rect(const.registration_screen, const.BRIGHT_YELLOW, (15, 40, 770, 110))
        largetext = pygame.font.Font('freesansbold.ttf', 95)
        TextSurf, TextRect = menu_pause.text_objects("REGISTRATION", largetext)
        TextRect.center = (400, 100)
        const.registration_screen.blit(TextSurf, TextRect)

        button("CREATE", 350, 300, 100, 50, const.RED, const.BRIGHT_RED, "create")
        button("BACK", 600, 520, 100, 50, const.BLUE, const.BRIGHT_BLUE, "menu")
        name_reg()
        password_reg()
        password_repeat_reg()
        pygame.display.update()
        const.clock.tick(50)

def button(msg, x, y, w, h, ic, ac, action = None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(const.registration_screen, ac, (x, y, w, h))
        if click[0] == 1 and action != None:
            if action == "menu":
                const.registration_pressed = False
                # events = pygame.event.get(pygame.MOUSEBUTTONUP)
                pygame.event.wait()
                # menu_pause.intro_loop()
            elif action == "create":
                const.create_pressed = True
    else:
        pygame.draw.rect(const.registration_screen, ic, (x, y, w, h))
    smalltext = pygame.font.Font("freesansbold.ttf", 20)
    textsurf, textrect = menu_pause.text_objects(msg, smalltext)
    textrect.center = ((x + (w / 2)),(y + (h / 2)))
    const.registration_screen.blit(textsurf, textrect)

def name_reg():
    global start_input_for_name, start_input_for_password, start_input_for_repeat_password, user_name, user_password,\
         user_repeat_password, text_tick_name, text_tick_password, text_tick_repeat_password, user, name_error

    input_rect = pygame.Rect(402, 180, 150, 35)

    smalltext = pygame.font.Font("freesansbold.ttf", 15)
    textsurf = smalltext.render('Имя пользователя:', True, const.BLACK)
    textrect = textsurf.get_rect()
    textrect.x, textrect.y = input_rect.x - 152, input_rect.y + 7.5
    const.registration_screen.blit(textsurf, textrect)

    pygame.draw.rect(const.registration_screen, (255, 255, 255), input_rect)
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    # Захват окна
    if input_rect.collidepoint(mouse[0], mouse[1]) and click[0]:
        start_input_for_name = True
        text_tick_name = 30
        
        start_input_for_password = False
        text_tick_password = -40

        start_input_for_repeat_password = False
        text_tick_repeat_password = -40
    
    # Добавление буквы
    if start_input_for_name:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                text_tick_name = 30
                if event.key == pygame.K_BACKSPACE:
                    user_name = user_name[:-1]
                else:
                    if len(user_name) < 15:
                        user_name += event.unicode

    # Печать
    if len(user_name) > 0 or text_tick_name > 0:
        smalltext = pygame.font.Font("freesansbold.ttf", 20)
        textsurf = smalltext.render(user_name + '|' * (text_tick_name > 0), True, const.BLACK)
        textrect = textsurf.get_rect()
        textrect.x, textrect.y = input_rect.x + 10, input_rect.y + 7.5
        const.registration_screen.blit(textsurf, textrect)

    text_tick_name -= 1
    if text_tick_name == -30:
        text_tick_name = 30

    if const.create_pressed:
        try:
            if user_name == '':
                raise Exception
            con = sqlite3.connect("users.sqlite")
            cur = con.cursor()
            names = cur.execute('SELECT name FROM data').fetchall()
            names = [i[0] for i in names]
            if user_name in names:
                raise Exception
            cur.execute('INSERT INTO data(name) VALUES(?)', (user_name, )).fetchall()
            con.commit()
        except Exception:
            #TD good exception rects
            name_error = True

def password_reg():
    global start_input_for_name, start_input_for_password, start_input_for_repeat_password, user_name, user_password,\
         user_repeat_password, text_tick_name, text_tick_password, text_tick_repeat_password, user, name_error, password_error  

    input_rect = pygame.Rect(402, 220, 150, 35)

    smalltext = pygame.font.Font("freesansbold.ttf", 15)
    textsurf = smalltext.render('Пароль:', True, const.BLACK)
    textrect = textsurf.get_rect()
    textrect.x, textrect.y = input_rect.x - 152, input_rect.y + 7.5
    const.registration_screen.blit(textsurf, textrect)

    pygame.draw.rect(const.registration_screen, (255, 255, 255), input_rect)
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    # Захват окна
    if input_rect.collidepoint(mouse[0], mouse[1]) and click[0]:
        start_input_for_password = True
        text_tick_password = 30
        
        start_input_for_name = False
        text_tick_name = -40

        start_input_for_repeat_password = False
        text_tick_repeat_password = -40
    
    # Добавление буквы
    if start_input_for_password:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                text_tick_password = 30
                if event.key == pygame.K_BACKSPACE:
                    user_password = user_password[:-1]
                else:
                    if len(user_password) < 15:
                        user_password += event.unicode
    
    # Печать
    if len(user_password) > 0 or text_tick_password > 0:
        smalltext = pygame.font.Font("freesansbold.ttf", 20)
        textsurf = smalltext.render('*' * len(user_password) + '|' * (text_tick_password > 0), True, const.BLACK)
        textrect = textsurf.get_rect()
        textrect.x, textrect.y = input_rect.x + 10, input_rect.y + 7.5
        const.registration_screen.blit(textsurf, textrect)

    text_tick_password -= 1
    if text_tick_password == -30:
        text_tick_password = 30

    if const.create_pressed:
        try:
            if user_password == '':
                raise Exception
            else:
                con = sqlite3.connect("users.sqlite")
                cur = con.cursor()
                login.user.score = 0
                cur.execute('''UPDATE data
                SET %s = 0
                WHERE name = ?'''%'score', (user_name, )).fetchall()
                con.commit()
        except Exception:
            if not name_error:
                password_error = True

def password_repeat_reg():
    global start_input_for_name, start_input_for_password, start_input_for_repeat_password, user_name, user_password,\
         user_repeat_password, text_tick_name, text_tick_password, text_tick_repeat_password, user, repeat_password_error, name_error, password_error

    input_rect = pygame.Rect(402, 260, 150, 35)

    smalltext = pygame.font.Font("freesansbold.ttf", 15)
    textsurf = smalltext.render('Повтор пароля:', True, const.BLACK)
    textrect = textsurf.get_rect()
    textrect.x, textrect.y = input_rect.x - 152, input_rect.y + 7.5
    const.registration_screen.blit(textsurf, textrect)
    
    pygame.draw.rect(const.registration_screen, (255, 255, 255), input_rect)
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    # Захват окна
    if input_rect.collidepoint(mouse[0], mouse[1]) and click[0]:
        start_input_for_repeat_password = True
        text_tick_repeat_password = 30
        
        start_input_for_name = False
        text_tick_name = -40

        start_input_for_password = False
        text_tick_password = -40
    
    # Добавление буквы
    if start_input_for_repeat_password:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                text_tick_repeat_password = 30
                if event.key == pygame.K_BACKSPACE:
                    user_repeat_password = user_repeat_password[:-1]
                else:
                    if len(user_repeat_password) < 15:
                        user_repeat_password += event.unicode
    
    # Печать
    if len(user_repeat_password) > 0 or text_tick_repeat_password > 0:
        smalltext = pygame.font.Font("freesansbold.ttf", 20)
        textsurf = smalltext.render('*' * len(user_repeat_password) + '|' * (text_tick_repeat_password > 0), True, const.BLACK)
        textrect = textsurf.get_rect()
        textrect.x, textrect.y = input_rect.x + 10, input_rect.y + 7.5
        const.registration_screen.blit(textsurf, textrect)

    text_tick_repeat_password -= 1
    if text_tick_repeat_password == -30:
        text_tick_repeat_password = 30

    if const.create_pressed:
        try:
            con = sqlite3.connect("users.sqlite")
            cur = con.cursor()
            if name_error:
                raise Exception
            elif user_repeat_password == '':
                raise Exception
            elif user_repeat_password != user_password:
                raise Exception
            else:
                cur.execute('''UPDATE data
                SET password = ?
                WHERE name = ?''', (user_password, user_name)).fetchall()
                con.commit()
                after_reg()
        except Exception:
            if not name_error and not password_error:
                repeat_password_error = True
            error()

def error():
    global name_error, password_error, repeat_password_error
    con = sqlite3.connect("users.sqlite")
    cur = con.cursor()
    if name_error:
        names = cur.execute('SELECT name FROM data').fetchall()
        names = [i[0] for i in names]
        if user_name in names:
            login.status_label('Имя пользователя недоступно.')
        else:
            login.status_label('Введите имя пользователя.')
        const.create_pressed = False
        name_error = False
    elif password_error:
        login.status_label('Введите пароль.')
        cur.execute('''DELETE from data
        where name = ?''', (user_name, )).fetchall()
        con.commit()
        const.create_pressed = False
        password_error = False
    elif repeat_password_error:
        if user_repeat_password == '':
            login.status_label('Введите повтор пароля.')
        else:
            login.status_label('Ваши пароли не совпадают.')
        cur.execute('''DELETE from data
        where name = ?''', (user_name, )).fetchall()
        con.commit()
        const.create_pressed = False
        repeat_password_error = False

def after_reg():
    global text_tick_name, text_tick_password, text_tick_repeat_password, user_name, user_password
    const.create_pressed = False
    login.status_label('Регистрация завершена!')
    user.name = user_name
    user.password = user_password
    user.score = 0
    user_name, user_password = '', ''
    text_tick_name, text_tick_password, text_tick_repeat_password = -40, -40, -40
