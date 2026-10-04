from pygame import *
import os
import sys




def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath('.'), relative_path)

init()
missed1 = 0
missed2 = 0

screen = display.set_mode((700, 500))
display.set_caption("PingPong")
clock = time.Clock()

game_font = font.SysFont("arial", 30)

background = transform.scale(image.load(resource_path("background.png")), (700, 500))



class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, size_x=20, size_y=50):
        self.image = transform.scale(image.load(resource_path(player_image)), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        
    def reset(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))




class Player(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed, size_x=25, size_y=120, up_key=K_w, down_key=K_s):
        super().__init__(player_image, player_x, player_y, player_speed, size_x, size_y)
        self.up_key = up_key
        self.down_key = down_key

    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[self.up_key] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys_pressed[self.down_key] and self.rect.y < 375: 
            self.rect.y += self.speed



class Ball(GameSprite):
    def __init__(self, player_image, player_x, player_y, speed_x, speed_y, size_x=100, size_y=50):
        super().__init__(player_image, player_x, player_y, 0, size_x, size_y)
        self.speed_x = speed_x
        self.speed_y = speed_y

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.y <= 0 or self.rect.y >= 460: 
            self.speed_y *= -1 



racket1 = Player("racket.png", 30, 200, 10, 25, 120, up_key=K_w, down_key=K_s)
racket2 = Player("racket.png", 645, 200, 10, 25, 120, up_key=K_UP, down_key=K_DOWN)
ball = Ball("tenis_ball.png", 330, 230, 4, 4, 40, 40)





game = True
finish = False
rel_time = False


while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    if not finish:
        screen.blit(background, (0, 0))
        if sprite.collide_rect(racket1, ball) or sprite.collide_rect(racket2, ball):
            ball.speed_x *= -1 
        racket1.update()
        racket2.update()
        ball.update()    
        racket1.reset()
        ball.reset()
        racket2.reset()
        if ball.rect.x < 0:
            missed1 += 1
            ball.rect.x = 330
            ball.rect.y = 230
            ball.speed_x = 4  
            ball.speed_y = 4  

        if ball.rect.x > 700:
            missed2 += 1
            ball.rect.x = 330
            ball.rect.y = 230
            ball.speed_x = -4  
            ball.speed_y = -4  
            
        display.update()

        if missed1 >= 1: 
            game_font = font.SysFont("arial", 40)
            text_lose = game_font.render("Победа правого игрока!", True, (3, 252, 15))
            screen.blit(text_lose, (150, 200))
            finish = True

        if missed2 >= 1: 
            game_font = font.SysFont("arial", 40)
            text_lose = game_font.render("Победа левого игрока!", True, (3, 252, 15))
            screen.blit(text_lose, (150, 200))
            finish = True


    display.update()
    clock.tick(60)

