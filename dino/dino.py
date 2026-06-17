import pygame
import random

pygame.init()

screen_w = 800
screen_h = 400
screen = pygame.display.set_mode((screen_w, screen_h))
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
clock = pygame.time.Clock()
fps = 60
game_over = False
jump_score = 0
dino_p=pygame.image.load('DinoJump.png')
spike_p=pygame.image.load('SmallCactus1.png')
ground_p=pygame.image.load('Track.png')
dino_p = pygame.transform.scale(dino_p, (60,60))
spike_p = pygame.transform.scale(spike_p, (40,60))
class Dino:

    def __init__(self):
        self.x = 50
        self.y = 300
        self.width = 60
        self.height = 60
        self.is_jumping = False
        self.jump_count = 10
        self.gravity = 3
        self.image = dino_p
        self.jump_score = jump_score

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def jump(self):
        if self.is_jumping:
            if self.jump_count >= -10:
                neg = 1
                if self.jump_count < 0:
                    neg = -1
                self.y -= (self.jump_count ** 2) * 0.5 * neg
                self.jump_count -= 1
            else:
                self.is_jumping = False
                self.jump_count = 10

class Obstacle:

    def __init__(self,x,y,width,height,speed):
        self.passed = False
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.image = pygame.transform.scale(spike_p, (width,height))

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def reset(self):
        self.x = self.start_x

    def move(self):
        self.x -= self.speed

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def display_score(score, screen):
        font = pygame.font.Font('PressStart2P-Regular.ttf', 36)
        score_text = font.render(f"Score: {score}", True, black)
        screen.blit(score_text, (10, 10))


dino = Dino()

obstacles = [
    Obstacle(800, 300, 40, 60, 8),
    Obstacle(1200, 300, 40, 60, 8),
    Obstacle(1600, 300, 40, 60, 8)
]
score = 0

running = True

def reset_game():
    global score, game_over

    score = 0
    game_over = False

    dino.y = 300
    dino.is_jumping = False
    dino.jump_count = 10

    obstacles[0].x = 800
    obstacles[1].x = 1200
    obstacles[2].x = 1600

while running:
    if score > 10:
        screen.fill(green)
    else:
        screen.fill(white)
    screen.blit(ground_p, (0, 350))
    dino.draw(screen)
    for obstacle in obstacles:
        obstacle.draw(screen)

        if not game_over:
            obstacle.move()
    for obstacle in obstacles:
        for other in obstacles:
            if obstacle != other:
                if obstacle.get_rect().colliderect(other.get_rect()):
                    obstacle.x = other.x + random.randint(250, 450)

    for obstacle in obstacles:
        obstacle.speed = min(8 + score // 10, 15)

        if dino.get_rect().colliderect(obstacle.get_rect()):
            game_over = True

    for event in pygame.event.get():

        if event.type == pygame.KEYDOWN:
            if game_over and event.key == pygame.K_r:
                reset_game()

        if event.type == pygame.QUIT:

            running = False

    keys = pygame.key.get_pressed()

    if not game_over:
        if not dino.is_jumping:
            if keys[pygame.K_SPACE]:
                dino.is_jumping = True
                dino.jump_score += 1
                print(f"Всего прыжков : {dino.jump_score}")
    dino.jump()

    for obstacle in obstacles:

        if not obstacle.passed and obstacle.x + obstacle.width < dino.x:
            score += 1
            obstacle.passed = True

        if obstacle.x < -obstacle.width:
            obstacle.x = max(o.x for o in obstacles) + random.randint(250, 450)
            obstacle.passed = False

    Obstacle.display_score(score, screen)
    if game_over:
        dino.jump_score = 0
        font = pygame.font.Font(None, 50)
        text = font.render("GAME OVER (R - restart)", True, black)
        screen.blit(text, (180, 150))
    pygame.display.update()
    clock.tick(fps)

pygame.quit()
print(f"Игра окончена! Вы прыгнули за игру {dino.jump_score} раз(-а)")