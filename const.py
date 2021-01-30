import pygame
import os

pygame.init()
menu_width, menu_height = 800, 600
menu_display = pygame.display.set_mode((menu_width, menu_height))


def load_image(name, colorkey=None):
    fullname = os.path.join('images', name)
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image

#main
WIDTH, HEIGHT = 1400, 500
FPS = 15
clock = pygame.time.Clock() 

START_CHARACTER_X = 0.25 * WIDTH
START_CHARACTER_Y = 0.6 * HEIGHT

START_JUMP_COUNTER = 15 + FPS

START_OBSTACLE_X = 1700
START_OBSTACLE_Y = 270

START_COIN_X = 1500
START_COIN_Y = 280
bg = pygame.transform.scale(load_image("SAW0.jpg"), (WIDTH, HEIGHT))
bg_x = 0
running = False

#menu_pause
GRAY = (119, 118, 110)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 200)
YELLOW = (255, 255, 224)
BRIGHT_RED = (255, 0, 0)
BRIGHT_GREEN = (0, 255, 0)
BRIGHT_BLUE = (0, 0, 255)
BRIGHT_YELLOW = (255, 255, 0)
intro_background = load_image("background.png")
instruction_background = load_image("sfs.jpg")
pause = False

#game_over
over = False

#registration
registration_screen = pygame.display.set_mode((menu_width, menu_height))
login_pressed = False
registration_pressed = False
create_pressed = False
