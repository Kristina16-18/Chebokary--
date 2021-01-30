import pygame
import time
import sqlite3
import main, menu_pause, const, registration

start_input_for_name = False
start_input_for_password = False
user_name = ''
user_password = ''
user_repeat_password = ''
text_tick_name = -40
text_tick_password = -40
name_error = False
password_error = False


class User:
    def __init__(self):
        self.name = ''
        self.password = ''
        self.score = 0


user = User()

def name_login():
    global start_input_for_name, start_input_for_password, user_name, user_password, text_tick_name, text_tick_password, name_error

    input_rect = pygame.Rect(402, 200, 150, 35)

    smalltext = pygame.font.Font("freesansbold.ttf", 15)
    textsurf = smalltext.render('Имя пользователя:', True, const.BLACK)
    textrect = textsurf.get_rect()
    textrect.x, textrect.y = input_rect.x - 152, input_rect.y + 7.5
    const.registration_screen.blit(textsurf, textrect)

    pygame.draw.rect(const.menu_display, (255, 255, 255), input_rect)
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    # Захват окна
    if input_rect.collidepoint(mouse[0], mouse[1]) and click[0]:
        start_input_for_name = True
        text_tick_name = 30
        
        start_input_for_password = False
        text_tick_password = -40
    
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
        const.menu_display.blit(textsurf, textrect)

    text_tick_name -= 1
    if text_tick_name == -30:
        text_tick_name = 30

    if const.login_pressed:
        try:
            con = sqlite3.connect("users.sqlite")
            cur = con.cursor()
            names = cur.execute('SELECT name FROM data').fetchall()
            names = [i[0] for i in names]
            if user_name not in names:
                raise Exception
        except Exception:
            name_error = True

def password_login():
    global start_input_for_name, start_input_for_password, user_name, user_password, text_tick_name, text_tick_password, user, password_error, name_error

    input_rect = pygame.Rect(402, 240, 150, 35)

    smalltext = pygame.font.Font("freesansbold.ttf", 15)
    textsurf = smalltext.render('Пароль:', True, const.BLACK)
    textrect = textsurf.get_rect()
    textrect.x, textrect.y = input_rect.x - 152, input_rect.y + 7.5
    const.registration_screen.blit(textsurf, textrect)

    pygame.draw.rect(const.menu_display, (255, 255, 255), input_rect)
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    # Захват окна
    if input_rect.collidepoint(mouse[0], mouse[1]) and click[0]:
        start_input_for_password = True
        text_tick_password = 30
        
        start_input_for_name = False
        text_tick_name = -40
    
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
        const.menu_display.blit(textsurf, textrect)

    text_tick_password -= 1
    if text_tick_password == -30:
        text_tick_password = 30

    if const.login_pressed:
        global name_error
        try:
            con = sqlite3.connect("users.sqlite")
            cur = con.cursor()
            password = cur.execute('''SELECT password FROM data
            WHERE name = ?''', (user_name, )).fetchall()
            password = str(password[0][0])
            if name_error:
                raise Exception
            if user_password != password:
                raise Exception
            else:
                score = cur.execute('''SELECT score FROM data
                WHERE name = ?''', (user_name, )).fetchall()
                user.score = int(score[0][0])
                after_login()
        except Exception as e:
            if not name_error:
                password_error = True
            error()

def error():
    global name_error, password_error
    if name_error:
        status_label('Пользователь не найден')
        name_error = False
    elif password_error:
        status_label('Пароль неверный')
        password_error = False
    const.login_pressed = False

def status_label(msg):
    input_rect = pygame.Rect(300, 390, 200, 35)
    pygame.draw.rect(const.registration_screen, (255, 255, 255), input_rect)
    smalltext = pygame.font.Font("freesansbold.ttf", 10)
    textsurf = smalltext.render(msg, True, const.RED)
    textrect = textsurf.get_rect()
    textrect.x, textrect.y = input_rect.x + 10, input_rect.y + 7.5
    const.registration_screen.blit(textsurf, textrect)
    pygame.display.update()
    time.sleep(2)

def after_login():
    global user_name, user_password, text_tick_name, text_tick_password
    con = sqlite3.connect("users.sqlite")
    cur = con.cursor()
    status_label('Вы успешно вошли!')
    user.name = user_name
    user.password = user_password
    const.login_pressed = False
    user_name, user_password = '', ''
    text_tick_name, text_tick_password = -40, -40
