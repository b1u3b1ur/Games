from pygame import *


class GameSprite(sprite.Sprite):

    def __init__(self, player_image, player_x, player_y, player_speed):

        sprite.Sprite.__init__(self)

        self.image = transform.scale(image.load(player_image), (80, 80))
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
        if keys[K_RIGHT] and self.rect.x < SCREEN_WIDTH - 80:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < SCREEN_HEIGHT - 80:
            self.rect.y += self.speed

  
class Enemy(GameSprite):
    side = "left"
    #movimiento del enemigo
    def update(self):
        if self.rect.x <= 410:
            self.side = "right"
        if self.rect.x >= SCREEN_WIDTH - 85:
            self.side = "left"
        if self.side == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed


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


SCREEN_WIDTH = 700
SCREEN_HEIGHT = 500
display.set_caption("Labyrinth")
window = display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

wall1 = Wall(0, 0, 0, SCREEN_WIDTH / 2 - SCREEN_WIDTH / 3, SCREEN_HEIGHT / 2, 300, 10)
wall2 = Wall(0, 0, 0, 410, SCREEN_HEIGHT / 2 - SCREEN_HEIGHT / 4, 10, 350)

pacman = Player('hero.png', 5, SCREEN_HEIGHT - 80, 5)
monster = Enemy('cyborg.png', SCREEN_WIDTH - 80, 200, 5)
final_sprite = GameSprite('pac.png', SCREEN_WIDTH - 85, SCREEN_HEIGHT - 100, 0)

background = image.load('jungle.jpg')
transform.scale(background, (700, 500))

clock = time.Clock()

finish = False

run = True
while run:

    time.delay(10)

    clock.tick(144)

    for e in event.get():

        if e.type == QUIT:
            run = False

    if not finish:

        window.fill((255, 255, 255))

        window.blit(background, (0, 0))

        wall1.draw_wall()
        wall2.draw_wall()

        pacman.update()
        monster.update()

        pacman.reset()
        monster.reset()
        final_sprite.reset()

        if sprite.collide_rect(pacman, monster) or sprite.collide_rect(pacman, wall1) or sprite.collide_rect(pacman, wall2):
            finish = True

            img = image.load('game-over_1.png')
            d = img.get_width() // img.get_height()
            window.fill((255, 255, 255))
            window.blit(transform.scale(img, (SCREEN_HEIGHT * d, SCREEN_HEIGHT)), (90, 0))

        if sprite.collide_rect(pacman, final_sprite):
            finish = True
            img = image.load('thumb.jpg')
            window.fill((255, 255, 255))
            window.blit(transform.scale(img, (SCREEN_WIDTH, SCREEN_HEIGHT)), (0, 0))

    display.update()