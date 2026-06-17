import pygame
pygame.init()

height=900
wight=600
screen=pygame.display.set_mode((height,wight))

white=(255,255,255)
black=(0,0,0)
green=(0,255,0)
blue=(0,0,100)
score = 0
score2 = 0
clock=pygame.time.Clock()
fps=120

class Player:
    def __init__(self,x,y,wight,height,color):
        self.x=x
        self.y=y
        self.wight=wight
        self.height=height
        self.color=color
        self.speed=4

    def draw(self,screen):
        pygame.draw.rect(screen,self.color,(self.x,self.y,self.wight,self.height))

    def collision(self,y):
        if self.y<=0:
            self.y=0
        elif self.y>= wight - self.height:
            self.y= wight - self.height

    def move(self,keys):
        if keys[pygame.K_s]:
            self.y=self.y+self.speed
        elif keys[pygame.K_w]:
            self.y=self.y-self.speed

    def rect(self):
        return pygame.Rect(self.x,self.y,self.wight,self.height)


class Player2:
    def __init__(self,x2,y2,wight,height,color):
        self.x=x2
        self.y=y2
        self.wight = wight
        self.height = height
        self.color=color
        self.speed=4

    def collision(self,y):
        if self.y<=0:
            self.y=0
        elif self.y>= wight - self.height:
            self.y= wight - self.height

    def draw(self,screen):
        pygame.draw.rect(screen,self.color,(self.x,self.y,self.wight,self.height))

    def move(self,keys):
        if keys[pygame.K_DOWN]:
            self.y=self.y+self.speed
        elif keys[pygame.K_UP]:
            self.y=self.y-self.speed

    def rect(self):
        return pygame.Rect(self.x,self.y,self.wight,self.height)

class Ball:
    def __init__(self,x,y,radius,color):
        self.x=x
        self.y=y
        self.radius=radius
        self.color=color
        self.speed_x=2
        self.speed_y=2

    def draw(self,screen):
        pygame.draw.circle(screen,self.color,(self.x,self.y),self.radius)

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y

    def reset(self):
        self.x = 450
        self.y = 300
        self.speed_x *= -1

running=True

player1=Player(50,50,30,100,white)
ball = Ball(450,300,15,green)
player2=Player2(850,50,30,100,white)

while running:
    screen.fill(blue)
    player1.draw(screen)
    player2.draw(screen)
    ball.draw(screen)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False
            print(f"У Игрока 1 {score} очков\nУ Игрока 2 {score2} очков")

    ball.move()
    if ball.y - ball.radius <= 0:
        ball.speed_y *= -1

    if ball.y + ball.radius > 600:
        ball.speed_y *= -1

    ball_rect = pygame.Rect(
        ball.x - ball.radius,
        ball.y - ball.radius,
        ball.radius * 2,
        ball.radius * 2
    )
    if ball.x < 0 :
        ball.reset()
        score2 += 1
        ball.speed_x = 2
    elif ball.x > 900:
        ball.reset()
        score += 1
        ball.speed_x = 2
    if ball_rect.colliderect(player1.rect()):
        ball.speed_x *= -1.05

    if ball_rect.colliderect(player2.rect()):
        ball.speed_x *= -1.05

    player1.collision(player1.y)
    player2.collision(player2.y)
    keys=pygame.key.get_pressed()
    player1.move(keys)
    player2.move(keys)
    pygame.display.update()
    clock.tick(fps)
pygame.quit()
