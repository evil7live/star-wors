from random import randint
from tkinter import font
from time import time as timer 

#Создай собственный Шутер!

from pygame import *
import pygame
lost  = 0
clock = time.Clock()
FPS = 30
wn = pygame.display.set_mode((700,500))
background = transform.scale(image.load("galaxy.jpg"),(700,500))
display.set_caption("ШУТЕР")
speed = 10
mixer.init()
mixer.music.load("ni_por_favor.mp3")
mixer.music.play()
class GameSprite(sprite.Sprite):
    def __init__(self,player_image,player_x,player_y,size_x,size_y,player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(size_x,size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        wn.blit(self.image, (self.rect.x,self.rect.y))

class Enemy(GameSprite):
    def update(self):
        global lost
        if self.rect.y > 450:
            self.rect.x = randint(80,620)  
            self.rect.y = 0
            lost += 1
        self.rect.y += 1
bullets = sprite.Group()

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

class Aster(GameSprite):
    def update(self):
        if self.rect.y > 450:
            self.rect.x = randint(80,620)
            self.rect.y = 0
        self.rect.y += 1

font.init()
font1 = font.SysFont("Arial", 36)
text_lose = font1.render("Пропущено:" + str(lost),1, (10,240,30))
text_score = font1.render("СЧЕТ:" + str(lost),1, (30,240,30))
score = 0
enemies = sprite.Group()
for i in range(5):
    m = Enemy("ufo.png",randint(80,620),-40,80,50,randint(1,7))
    enemies.add(m)
asteroids = sprite.Group()
for i in range(3):
    asteroid = Aster("asteroid.png",randint(80,620),-80,80,50,randint(1,5))
    asteroids.add(asteroid)



class Player(GameSprite):
    def update(self):
        keys= key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 700 - 80:
            self.rect.x += self.speed  
            # 
        # if keys[K_SPACE]:
        #     self.fire()
    def fire(self):
        bullet = Bullet('bullet.png',self.rect.centerx,self.rect.top,15,20,-15)
        bullets.add(bullet)

player = Player("rocket.png",350,400,80,100,10)
life = 3 
life_text = font.SysFont("lumineri",70).render(str(life),True,(255,255,131))
finish = False
game  = True

num_fire = 0
rel_time = False 

while game:
    wn.blit(background,(0,0))
    for e in event.get():
        if e.type == QUIT:
            game = False
            # 
        if e.type == KEYDOWN and e.key == K_SPACE:
            if num_fire <5 and rel_time == False:
                num_fire += 1
                player.fire()
            if num_fire >= 5 and rel_time == False:
                last_time = timer()
                rel_time = True 
    if  not finish:
        if rel_time == True:
            now_time = timer()
            if now_time - last_time < 1:
                reload = font.SysFont("snellroundhand",40).render("Wait! reloading...",True,(255,255,255))
                wn.blit(reload,(260,420))
            else:
                num_fire = 0
                rel_time = False  
    sprites_list = sprite.groupcollide(enemies,bullets,True,True)
    player_list = sprite.spritecollide(player,enemies,True)
    for i in player_list:  
        life -= 1
        life_text = font.SysFont("lumineri",70).render(str(life),True,(255,255,131))
        m = Enemy("ufo.png",randint(80,620),-80,80,50,randint(4,5))
        enemies.add(m)
    aster_list = sprite.spritecollide(player,asteroids,True)
    for i in aster_list:
        life -= 1
        life_text = font.SysFont("lumineri",70).render(str(life),True,(255,255,131))
        asteroid =  Aster("asteroid.png",randint(80,620),-80,80,50,randint(4,5))
        asteroids.add(m)
    if life < 1 :
        game = False
    for i in sprites_list:
        m = Enemy("ufo.png",randint(80,620),-80,80,50,randint(1,5))
        enemies.add(m)
        score += 1
    score_text = font1.render("СЧЕТ:" + str(score),True, (10,240,150))
    player.reset()
    player.update()
    text_lose = font1.render("Пропущено:" + str(lost),1, (10,240,30))
    text_score = font1.render("СЧЕТ:" + str(score),1, (10,240,150))
    if score > 19:
        game = False
    if lost > 5:
        game = False

    asteroids.draw(wn)
    asteroids.update()
    enemies.draw(wn)
    bullets.draw(wn)
    bullets.update()
    enemies.update()
    wn.blit(life_text,(600,0))
    
    wn.blit(text_lose,(0,0))
    wn.blit(score_text,(0,30))
    clock.tick(FPS)
    display.update()
display.update()