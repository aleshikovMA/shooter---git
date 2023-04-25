from os import*
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from random import *
from pygame import *
import time as timer
total = 0
b = True
a = True
global skeeped
skeeped = 0
gametime = "0"
start = timer.time()
clock = time.Clock()
window = display.set_mode((700,500))
class spriten(sprite.Sprite):
    def __init__ (self, img, sx, sy, px, py, pspx, pspy):
        super().__init__()
        self.sizex = sx
        self.sizey = sy
        self.image = transform.scale(image.load(img),(self.sizex,self.sizey))
        self.last_time = timer.time()
        self.rect = self.image.get_rect()
        self.rect.x = px
        self.rect.y = py
        self.start_x = px
        self.start_y = py
        self.speedx2 = pspx
        self.speedy2 = pspy
        self.speedx = pspx
        self.speedy = pspy
        self.rects = [self.rect.x,self.rect.y]
    def reset(self):
        window.blit(self.image,(self.rect.x, self.rect.y))
    def update2(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and hero.rect.x >5:
                hero.rect.x -= 3
        if keys[K_RIGHT] and hero.rect.x < 635:
                hero.rect.x += 3
        if keys[K_UP] and hero.rect.y > 250:
                hero.rect.y -= 3
        if keys[K_DOWN] and hero.rect.y < 450:
                hero.rect.y += 3
    def updater(self):
        global skeeped
        cur_time = timer.time()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.y >= 450:
            self.rect.y = 20
            skeeped += 1

        if self.rect.x + self.sizex >= 700:
            if self.start_x <= 200:
                self.rect.x = self.start_x
                self.rect.y = self.start_y
            else:
                self.rect.x = 5
        if self.rect.x <= 0:
            self.rect.x = 620
        if self.rect.y <= 0:
            self.rect.y = 420

        if cur_time - self.last_time >= 0.3:
            self.last_time = cur_time
            x = randint(-1,5)
            y = randint(1,5)
            self.speedx = randint(-3,3)
            self.speedy = randint(0,3)
    def updat(self):
        self.rect.x += self.speedx2
        self.rect.y += self.speedy2
        if self.rect.y >= 450:
            self.rect.y = 20

        if self.rect.x + 65 >= 700:
            if self.start_x <= 200:
                self.rect.x = self.start_x
                self.rect.y = self.start_y
            else:
                self.rect.x = 5
        if self.rect.x <= 0:
            self.rect.x = 620
        if self.rect.y <= 0:
            self.rect.y = 420
    def update(self):
        self.rect.y -= self.speedy
    def fire(self):
        bullet = spriten("bullet.png",20,30,hero.rect.x + 20,hero.rect.y +2,0,4)
        bulets.add(bullet)
    def start(self):
        self.rect.x = self.start_x
        self.rect.y = self.start_y

font.init()
font = font.SysFont("Roman",40)          
bg = transform.scale(image.load("galaxy.jpg"),(700,500))
hero = spriten("rocket.png",60,60,295,400,6,4)
enemy = spriten("ufo.png",40,40,10,5,4,0)
enemy2 = spriten("ufo.png",40,40,140,5,4,0)
enemy3 = spriten("ufo.png",40,40,270,5,4,0)
enemy4 = spriten("ufo.png",40,40,400,5,4,0)
meteor1 = spriten("asteroid.png",70,70,10,10,5,4)
meteor2 = spriten("asteroid.png",70,70,620,10,-5,4)
spr = [hero, enemy,enemy2, enemy3,enemy4,meteor1, meteor2]
bulets = sprite.Group()
while b:
    keys = key.get_pressed()
    window.blit(bg,(0,0))
    enemy.reset()
    enemy2.reset()
    enemy3.reset()
    enemy4.reset()
    hero.reset()
    meteor2.reset()
    meteor1.reset()
    bulets.draw(window)
    if a == True:
        enemy.updater()
        enemy2.updater()
        enemy3.updater()
        enemy4.updater()
        meteor1.updat()
        meteor2.updat()
        hero.update2()
        bulets.update()
        if sprite.collide_rect(hero,enemy):
            a = False
        if sprite.collide_rect(hero,enemy2):
            a = False
        if sprite.collide_rect(hero,enemy3):
            a = False
        if sprite.collide_rect(hero,enemy4):
            a = False
        if sprite.collide_rect(hero,meteor1):
            a = False
        if sprite.collide_rect(hero,meteor2):
            a = False
        if sprite.spritecollide(enemy,bulets,True):
            enemy.start()
            total += 1
        if sprite.spritecollide(enemy2,bulets,True):
            enemy2.start()
        if sprite.spritecollide(enemy3,bulets,True):
            enemy3.start()
            total+=1
        if sprite.spritecollide(enemy4,bulets,True):
            enemy4.start()
            total+=1
        if sprite.spritecollide(meteor1,bulets,True):
            meteor1.start()
            total+=1
        if sprite.spritecollide(meteor2,bulets,True):
            meteor2.start() 
            total+=1 
        finish = timer.time()
        gametime = finish - start
    else:            
        gametime = int(gametime)
        gametime = str(gametime)
        end = font.render(" вы продержались:"+gametime,True,(250,0,0))
        tot = font.render(" счет:"+str(total),True,(250,250,0))
        skpd = font.render("пропущено:" +str(skeeped),True,(250,75,0))
        window.blit(end,(0,100))
        window.blit(skpd,(275,200))
        window.blit(tot,(500,100))
        if keys[K_LALT] and keys[K_LCTRL]:
            total = 0
            gametime = 0
            skeeped = 0
            a = True 
            start = timer.time()
            for sprit in spr:
                sprit.start()
            for bul in bulets:
                bul.kill()
    for e in event.get():
        if e.type == QUIT:
            b = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                hero.fire()

    clock.tick(60)
    display.update()