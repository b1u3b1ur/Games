from pygame import *
import pygame,sys
from random import randint

pygame.init()
musica=pygame.mixer.music.load("hola.wav")
pygame.mixer.music.play(1000)

font.init()
font=font.Font(None,64)

hero_sprite = ('azul.png')

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
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < SCREEN_WIDTH -80:
            self.rect.x += self.speed
        if keys[K_SPACE]:
            self.rect.y -= self.speed*2
        if self.rect.y < SCREEN_HEIGHT - 80:
            self.rect.y += self.speed 
        if keys[K_s]:
            player.rect.y += 8
            


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



class Safe(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost

        if self.rect.y > SCREEN_HEIGHT:
            self.rect.x = randint(80, SCREEN_WIDTH - 80)
            self.rect.y = 0
            #este no es el codigo solo es algo que estoy probando
        
    

class Wall(sprite.Sprite):
  def __init__(self, color_1, color_2, color_3, wall_x, wall_y, wall_width, wall_height):
      sprite.Sprite.__init__(self)
      self.color_1 = color_1
      self.color_2 = color_2
      self.color_3 = color_3
      self.width = wall_width
      self.height = wall_height

      self.image = Surface([self.width, self.height])
      self.image.fill((color_1, color_2, color_3))

      self.rect = self.image.get_rect()
      self.rect.x = wall_x
      self.rect.y = wall_y

  def draw_wall(self):
      draw.rect(window, (self.color_1, self.color_2, self.color_3), (self.rect.x, self.rect.y, self.width, self.height))


SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
RED=(255,0,0)

Lifes = 3
boss_score = 20 
goal = 21
Jump= False
jump_heigth= 20 
jump_vel= jump_heigth
gravity= 5

display.set_caption("Half life")
window = display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))



player = Player(hero_sprite, 5, SCREEN_HEIGHT - 80,80,80, 8)
jose = Enemy('rojo.png', SCREEN_WIDTH - 80, SCREEN_HEIGHT - 80,80,80, 0)
Powerups = GameSprite('blanco.jpg', SCREEN_WIDTH - 85, SCREEN_HEIGHT - 100,80,80, 0)



background = image.load('negro.png')
transform.scale(background, (1000, 800))

monsters = sprite.Group()
for i in range(1, 6):
    monster = Minion('rojo.png', randint(50,SCREEN_WIDTH-50), randint(10,80),randint(50,100),randint(50,100),randint(1,5))
    monsters.add(monster)

isJump = False

jumpCount = 10

bullets = sprite.Group()

walsup = sprite.Group()
wals = sprite.Group()
for i in range(1, 6):
    wal =  Wall(255, 255, 255, 410, SCREEN_WIDTH / 2 - SCREEN_WIDTH / 4, 350, 10)
    walsup.add(wal)

for i in range(1, 6):
    wale =  Wall(200, 255, 255, 210, SCREEN_WIDTH / 2 , 350, 10)
    wals.add(wale)
    
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
                isJump = True 


    if not finish:
        WHITE = (255, 255, 255)
        OTHERCOLOR = (0, 0, 255)
        
        window.fill((135, 206, 235))

        window.blit(background, (0,220))

        Lifes_text=font.render(f"Vidas: {Lifes}" , 0 , RED) 
        window.blit(Lifes_text, (10, 20)) 

        wals.draw(window)
        walsup.draw(window)
        
        player.update()
        player.reset()

        jose.update()
        jose.reset()


        if sprite.collide_rect(player, jose):
            Lifes -= 1

        if sprite.collide_rect(player, wal):
            player.rect.y -= 8

        if sprite.collide_rect(player, wale):
            player.rect.y += 8
            
        if Lifes == 0:
            run= False



    display.update()