import pygame

WIDTH, HEIGHT = 1400, 500
FPS = 15
clock = pygame.time.Clock() 

START_CHARACTER_X = 400
START_CHARACTER_Y = 300

START_JUMP_COUNTER = 15 + FPS

START_OBSTACLE_X = 1700
START_OBSTACLE_Y = 300

START_COIN_X = 1500
START_COIN_Y = 280

bg = pygame.transform.scale(pygame.image.load("/Users/lizak/Desktop/project 2.0/Chebokary--/images/SAW0.jpg"), (WIDTH, HEIGHT))
