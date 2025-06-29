from pygame import *
import pygame,sys
from random import randint

pygame.init()
musica=pygame.mixer.music.load("nose.wav")
pygame.mixer.music.play(1000)

font.init()
font=font.Font(None,64)

class GameSprite(sprite.Sprite):

    def __init__(self, player_image, player_x, player_y,size_x,size_y, player_speed):

        sprite.Sprite.__init__(self)

        self.image = transform.scale(image.load(player_image), (size_x,size_y))
        self.speed = player_speed

        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):

    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < SCREEN_WIDTH -80:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top,20,40, 10)
        bullets.add(bullet)

        
class Enemy(GameSprite):
    side = "left"
    #movimiento del enemigo
    def update(self):
        if self.rect.x <= 30:
            self.side = "right"
        if self.rect.x >= SCREEN_WIDTH - 85:
            self.side = "left"
        if self.side == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

class Minion(GameSprite):
    #movimiento del enemigo
    def update(self):
        self.rect.y += self.speed
        global lost

        if self.rect.y > SCREEN_HEIGHT:
            self.rect.x = randint(80, SCREEN_WIDTH - 80)
            self.rect.y = 0
            lost += 1


class Bullet(GameSprite):
    def update(self):

        self.rect.y -= self.speed

        if self.rect.y <= 0:
            self.kill()


SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
RED=(255,0,0)

score=0
boss_score = 20 
lost= 0
max_lost= 10000
goal = 21

display.set_caption("Half life")
window = display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


player = Player('hero.png', 5, SCREEN_HEIGHT - 80,80,80, 8)
jose = Enemy('boss.png', SCREEN_WIDTH - 80, 200,80,80, 5)
Powerups = GameSprite('pac.png', SCREEN_WIDTH - 85, SCREEN_HEIGHT - 100,80,80, 0)
img_bullet = "bullet.png"


background = image.load('space.jpeg')
transform.scale(background, (1000, 800))

monsters = sprite.Group()
for i in range(1, 6):
    monster = Minion('enemy.png', randint(50,SCREEN_WIDTH-50), randint(10,80),randint(50,100),randint(50,100),randint(1,5))
    monsters.add(monster)


bullets = sprite.Group()

clock = time.Clock()

finish = False

run = True
while run:

    time.delay(10)

    clock.tick(144)

    for e in event.get():

        if e.type == QUIT:
            run = False

        elif  e.type == KEYDOWN:
            if e.key == K_SPACE:
                player.fire() 


    if not finish:
        window.fill((0, 0, 0))

        window.blit(background, (0, 0))

        score_text=font.render(f"Hola: {score}" , 0 , RED) 
        window.blit(score_text, (10, 20)) 

        text_lose =font.render(f'Adios:{lost}', 0, (RED))
        window.blit(text_lose, (10, 50))

        player.update()
        monsters.update()

        player.reset()
        

        monsters.draw(window)
        bullets.draw(window)

        bullets.update()

        collides = sprite.groupcollide(monsters,bullets,True,True)

        if score  >= boss_score:
            jose.update()
            jose.reset()
             

        for c in collides:
            score += 1
            monster = Minion('enemy.png', randint(50,SCREEN_WIDTH-50), randint(10,80),randint(50,100),randint(50,100),randint(1,5))
            monsters.add(monster)


        if sprite.spritecollide(player, monsters, False) or lost >= max_lost:
            finish = True

            window.fill((0, 6, 13))
            img = image.load('game-over_1.jpg')
            d = img.get_width() // img.get_height()
            window.blit(transform.scale(img, (SCREEN_HEIGHT * d, SCREEN_HEIGHT)), (90, 0))

        if score >= goal:
            finish = True
            img = image.load('thumb.jpg')
            window.fill((255, 255, 255))
            window.blit(transform.scale(img, (SCREEN_WIDTH, SCREEN_HEIGHT)), (0, 0))

    display.update()