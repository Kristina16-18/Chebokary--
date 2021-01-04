import pygame
import time

pygame.init()
pygame.mixer.init()
# Game Varialbes..
Width, Height = 1400, 500
bg_x = 0
gameDisplay = pygame.display.set_mode((Width, Height))
pygame.display.set_caption("Runner")

FPS = 10
animate_player = True
player_y = 300
player_x = 400
player_img_count = 0
isJump = False
velocity = 11
obstacle_count = 0
obstacle_x = 1700
obstacle_y = 300
coin_x = 1500
coin_y = 280
coin_count = 0
bg = pygame.transform.scale(pygame.image.load("images/SAW0.jpg"), (Width, Height))
score = 0

# Animating
playerimg = [pygame.image.load("images/p2.png"), pygame.image.load("images/p3.png"),
             pygame.image.load("images/p4.png"),
             pygame.image.load("images/p5.png"), pygame.image.load("images/p6.png"), pygame.image.load("images/p7.png"),
             pygame.image.load("images/p8.png"),
             pygame.image.load("images/p9.png"), pygame.image.load("images/p10.png")]
obstacle1 = [pygame.image.load("images/bmm.png"), pygame.image.load("images/bmm.png"),
             pygame.image.load("images/bmm.png"), pygame.image.load("images/bmm.png")]
coin = [pygame.image.load("images/c1.png"), pygame.image.load("images/c2.png"), pygame.image.load("images/c3.png"),
        pygame.image.load("images/c4.png")]

player_height = playerimg[player_img_count].get_height()
player_width = playerimg[player_img_count].get_width()
coin_height = coin[coin_count].get_height()
coin_width = coin[coin_count].get_width()
obstacle_height = obstacle1[obstacle_count].get_height()
obstacle_width = obstacle1[obstacle_count].get_width()


def coin_animation():
    global coin_x
    global coin_count
    gameDisplay.blit(coin[coin_count], (coin_x, coin_y))
    coin_count += 1
    if coin_count + 1 > 3:
        coin_count = 0
    coin_x -= 10
    if coin_x < -100:
        coin_x = 1500


def obstacles():
    global obstacle_x
    global obstacle_count
    gameDisplay.blit(obstacle1[obstacle_count], (obstacle_x, obstacle_y))
    obstacle_count += 1
    if obstacle_count + 1 > 3:
        obstacle_count = 0
    # Movement of obstacle ..
    obstacle_x -= 10
    if obstacle_x < -100:
        obstacle_x = 1700


def scrolling_background():
    global bg_x
    relative_x = bg_x % bg.get_rect().width
    gameDisplay.blit(bg, (relative_x - bg.get_rect().width, 0))
    if relative_x < Width:
        gameDisplay.blit(bg, (relative_x, 0))
    bg_x -= 10


# Collisions and showing score..
def show_score():
    score_obj = pygame.font.SysFont('comicsans', 50, True)
    score_txt = score_obj.render("Score: " + str(score), 1, (0, 0, 0))
    gameDisplay.blit(score_txt, (1000, 10))


def collision():
    global coin_x
    global score
    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
    coin_rect = pygame.Rect(coin_x, coin_y, coin_width, coin_height)
    blade_rect = pygame.Rect(obstacle_x + 20, obstacle_y + 20, obstacle_width - 20, obstacle_height)
    if player_rect.colliderect(coin_rect):
        # pygame.mixer.music.load("coin.mp3")
        # pygame.mixer.music.play()
        coin_x = 1500
        score += 1
    if player_rect.colliderect(blade_rect):
        # pygame.mixer.music.load("die.mp3")
        # pygame.mixer.music.play()
        time.sleep(2)
        quit()


clock = pygame.time.Clock()
run = True
# Gameloop:-
while run:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    keys = pygame.key.get_pressed()
    if not isJump:
        if keys[pygame.K_SPACE]:
            isJump = True
            # pygame.mixer.music.load("jump.ogg")
            # pygame.mixer.music.play()
    else:
        if velocity >= -11:
            gravity = 1
            if velocity < 0:
                gravity = -1
            player_y -= (velocity ** 2) * 1 / 2 * gravity
            velocity -= 1
        else:
            velocity = 11
            isJump = False

    scrolling_background()
    obstacles()
    coin_animation()
    show_score()
    collision()
    gameDisplay.blit(playerimg[player_img_count], (player_x, player_y))
    player_img_count += 1
    if player_img_count + 1 > 9:
        player_img_count = 0

    pygame.display.update()

pygame.quit()
quit()