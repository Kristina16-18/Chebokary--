import pygame
import time
import start_screen, const

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((const.WIDTH, const.HEIGHT))
pygame.display.set_caption("Runner")
jump_counter = const.START_JUMP_COUNTER
score = 0
const.bg_x = 0
animate_player = True 
isJump = False


class Character(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.images = [pygame.image.load("/Users/lizak/Desktop/project 2.0/Chebokary--/images/p2.png"), 
                       pygame.image.load("/Users/lizak/Desktop/project 2.0/Chebokary--/images/p3.png"),
                       pygame.image.load("/Users/lizak/Desktop/project 2.0/Chebokary--/images/p4.png"),
                       pygame.image.load("/Users/lizak/Desktop/project 2.0/Chebokary--/images/p5.png"), 
                       pygame.image.load("/Users/lizak/Desktop/project 2.0/Chebokary--/images/p6.png"), 
                       pygame.image.load("/Users/lizak/Desktop/project 2.0/Chebokary--/images/p7.png"),
                       pygame.image.load("/Users/lizak/Desktop/project 2.0/Chebokary--/images/p8.png"),
                       pygame.image.load("/Users/lizak/Desktop/project 2.0/Chebokary--/images/p9.png"), 
                       pygame.image.load("/Users/lizak/Desktop/project 2.0/Chebokary--/images/p10.png")]
        self.x, self.y = const.START_CHARACTER_X, const.START_CHARACTER_Y
        self.width, self.height = self.images[0].get_width(), self.images[0].get_height()
        self.count = 0
        
    def move(self):  
        screen.blit(character.images[character.count], (character.x, character.y))
        self.count += 1
        if self.count + 1 > len(self.images):
            self.count = 0
        


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.images = [pygame.image.load("/Users/lizak/Desktop/project 2.0/Chebokary--/images/bmm.png"), 
                                 pygame.image.load("/Users/lizak/Desktop/project 2.0/Chebokary--/images/bmm.png"),
                                 pygame.image.load("/Users/lizak/Desktop/project 2.0/Chebokary--/images/bmm.png"), 
                                 pygame.image.load("/Users/lizak/Desktop/project 2.0/Chebokary--/images/bmm.png")]
        self.x, self.y = const.START_OBSTACLE_X, const.START_OBSTACLE_Y
        self.width, self.height = self.images[0].get_width(), self.images[0].get_height()
        self.count = 0

    def move(self):
        if self.x < -self.width:
            self.x = const.START_OBSTACLE_X
        else:
            self.x -= const.FPS
        screen.blit(self.images[self.count], (self.x, self.y))
        self.count += 1
        if self.count + 1 > len(self.images):
            self.count = 0


class Coin(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.images = [pygame.image.load("/Users/lizak/Desktop/project 2.0/Chebokary--/images/c1.png"), 
                       pygame.image.load("/Users/lizak/Desktop/project 2.0/Chebokary--/images/c2.png"), 
                       pygame.image.load("/Users/lizak/Desktop/project 2.0/Chebokary--/images/c3.png"),
                       pygame.image.load("/Users/lizak/Desktop/project 2.0/Chebokary--/images/c4.png")]
        self.x, self.y = const.START_COIN_X, const.START_COIN_Y
        self.width, self.height = self.images[0].get_width(), self.images[0].get_height()
        self.count = 0

    def move(self):
        screen.blit(self.images[self.count], (self.x, self.y))
        self.count += 1
        if self.count + 1 > 3:
            self.count = 0
        self.x -= const.FPS
        if self.x < -100:
            self.x = 1500

all_sprites = pygame.sprite.Group()
character = Character(all_sprites)
obstacle = Obstacle(all_sprites)
coin = Coin(all_sprites)

def scrolling_background():
    relative_x = const.bg_x % const.bg.get_rect().width
    screen.blit(const.bg, (relative_x - const.bg.get_rect().width, 0))
    if relative_x < const.WIDTH:
        screen.blit(const.bg, (relative_x, 0))
    const.bg_x -= const.FPS 


def show_score():
    score_obj = pygame.font.SysFont('comicsans', 50, True)
    score_txt = score_obj.render("Score: " + str(score), 1, (0, 0, 0))
    screen.blit(score_txt, (1000, 10))


def collision():
    global score
    player_rect = pygame.Rect(character.x, character.y, character.width, character.height)
    coin_rect = pygame.Rect(coin.x, coin.y, coin.width, coin.height)
    blade_rect = pygame.Rect(obstacle.x + 20, obstacle.y + 20, obstacle.width - 20, obstacle.height)
    if player_rect.colliderect(coin_rect):
        # pygame.mixer.music.load("coin.mp3")
        # pygame.mixer.music.play()
        coin.x = const.START_COIN_X
        score += 1
    if player_rect.colliderect(blade_rect):
        # pygame.mixer.music.load("die.mp3")
        # pygame.mixer.music.play()
        time.sleep(2)
        quit()
    
def jump():
    global isJump, jump_counter
    if jump_counter >= -const.START_JUMP_COUNTER:
        character.y -= jump_counter
        jump_counter -= const.START_JUMP_COUNTER / 10
    else:
        jump_counter = const.START_JUMP_COUNTER
        isJump = False


if __name__ == '__main__':
    start_screen.start_screen()
    running = True
    while running:
        const.clock.tick(const.FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        keys = pygame.key.get_pressed()
        if not isJump:
            if keys[pygame.K_SPACE]:
                isJump = True
                # pygame.mixer.music.load("jump.ogg")
                # pygame.mixer.music.play()
        else:
            jump()

        scrolling_background()
        obstacle.move()
        coin.move()
        show_score()
        collision()
        character.move()

        pygame.display.update()
    pygame.quit()
    quit()