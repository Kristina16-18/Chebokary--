import pygame
import time
import menu_pause
import const
import after_level
import login

pygame.init()
pygame.mixer.init()
pygame.display.set_caption("Runner")
screen = pygame.display.set_mode((const.menu_width, const.menu_height))
jump_counter = const.START_JUMP_COUNTER
score = 0 
isJump = False

class Character(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.images = [const.load_image("p2.png"), 
                       const.load_image("p3.png"),
                       const.load_image("p4.png"),
                       const.load_image("p5.png"), 
                       const.load_image("p6.png"), 
                       const.load_image("p7.png")]
        self.x, self.y = const.START_CHARACTER_X, const.START_CHARACTER_Y
        self.width, self.height = self.images[5].get_width(), self.images[5].get_height()
        for i in range(6):
            self.images[i] =  pygame.transform.scale(self.images[i], (self.width, self.height))
        self.count = 0
        
    def move(self):  
        screen.blit(character.images[character.count], (character.x, character.y))
        self.count += 1
        if self.count + 1 > len(self.images):
            self.count = 0
        

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.images = [const.load_image("bmm.png", -1), 
                       const.load_image("bmm.png", -1),
                       const.load_image("bmm.png", -1), 
                       const.load_image("bmm.png", -1)]
        self.x, self.y = const.START_OBSTACLE_X, const.START_OBSTACLE_Y
        self.width, self.height = 90, 120
        for i in range(4):
            self.images[i] =  pygame.transform.scale(self.images[i], (self.width, self.height))
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
        self.images = [const.load_image("c1.png"), 
                       const.load_image("c2.png"), 
                       const.load_image("c3.png"),
                       const.load_image("c4.png")]
        self.x, self.y = const.START_COIN_X, const.START_COIN_Y
        self.width, self.height = 50, 60
        for i in range(4):
            self.images[i] =  pygame.transform.scale(self.images[i], (self.width, self.height))
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
        screen = pygame.display.set_mode((const.menu_width, const.menu_height))
        const.over = True
        after_level.game_over()
    
def jump():
    global isJump, jump_counter
    if jump_counter >= -const.START_JUMP_COUNTER:
        character.y -= jump_counter
        jump_counter -= const.START_JUMP_COUNTER / 10
    else:
        jump_counter = const.START_JUMP_COUNTER
        isJump = False


def main():
    global isJump 
    screen = pygame.display.set_mode((const.WIDTH, const.HEIGHT))
    while const.running:
        const.clock.tick(const.FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                const.running = False
        keys = pygame.key.get_pressed()
        if not isJump:
            if keys[pygame.K_SPACE]:
                isJump = True
                # pygame.mixer.music.load("jump.ogg")
                # pygame.mixer.music.play()
        else:
            jump()
        if keys[pygame.K_p]:
                screen = pygame.display.set_mode((const.menu_width, const.menu_height))
                menu_pause.game_loop()

        scrolling_background()
        obstacle.move()
        coin.move()
        show_score()
        collision()
        character.move()

        pygame.display.update() 
    pygame.quit()
    quit()

if __name__ == '__main__':
    menu_pause.intro_loop()
