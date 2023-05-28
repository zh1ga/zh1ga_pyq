#Создай собственный Шутер!

from pygame import *
from random import randint, random

init()

WIN_SIZE = [700, 500] # размер окна
window = display.set_mode(WIN_SIZE) # создание окна с размерами win_size
display.set_caption("Maze") # установить подпись окна
background = transform.scale(image.load("kocmos.png"), (WIN_SIZE)) # сделать размер картинки под размер окна

game = True 
finish = False

FPS = 60
clock = time.Clock()

mixer.init() # подключение использования миксира
mixer.music.load("space.ogg") # загрузить звуковой файл для ФОНОВОГО воспроизведение
mixer.music.set_volume(0.1)
mixer.music.play() # начать проигрывание ФОНОВОЙ музыки
fire_sound = mixer.Sound("fire.ogg")
fire_sound.set_volume(0.1)

class GameSprite(sprite.Sprite):
    def __init__(self, playerimage, speed, x, y, size_x, size_y):
        super().__init__()
        self.image = transform.scale(image.load(playerimage), (size_x, size_y)) 
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x < 635:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet("bullet.png", 5, self.rect.centerx - 7, self.rect.top - 5, 15, 20)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > WIN_SIZE[1]:
            self.rect.x = randint(20, WIN_SIZE[0] - 80)
            self.rect.y = 0
            self.speed = randint(1, 2)
            global lost
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()
        

score = 0
lost = 0
f1 = font.Font(None, 36)

bullets = sprite.Group()
monsters = sprite.Group()

player = Player("rocket.png", 10, 250, 435, 65, 65)

for i in range(1, 10):
    monster = Enemy("ufo.png", randint(1, 2), randint(20, WIN_SIZE[0] - 80), -40, 80, 50,)
    monsters.add(monster)

while game:
    if not finish:
        window.blit(background, (0, 0))
        player.reset()
        player.update()

        monsters.update()
        monsters.draw(window)
    
        bullets.update()
        bullets.draw(window)

        score2 = f1.render("Пропущено:" + str(lost), False, [255, 255, 255])
        window.blit(score2, (10, 25))
        score1 = f1.render("Счёт:" + str(score), True, [255, 255, 255])
        window.blit(score1, (10, 50))

    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                player.fire()
                fire_sound.play()

    sprite_list = sprite.groupcollide(monsters, bullets, True, True)
    for i in sprite_list:
        score += 1
        monster = Enemy("ufo.png", randint(1, 2), randint(20, WIN_SIZE[0] - 80), -40, 80, 50,)
        monsters.add(monster)



        
    display.update()
    clock.tick(FPS)

