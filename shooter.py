from os import*
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from random import *
from pygame import *
import time as timer
global skeeped
global finish
global speedtime
global total 
total = 0
speedtime = timer.time()
finish = timer.time()
b = True
a = True
skeeped = 0
gametime = "0"
start = timer.time()
clock = time.Clock()
window = display.set_mode((700,500))
class spriten(sprite.Sprite):
    def __init__ (self, img, sx, sy, px, py, pspx, pspy, hp, damage):
        super().__init__()
        self.hp = hp
        self.damage = damage 
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
        self.startsx = pspx
        self.startsy = pspy
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
        global speedtime
        global finish
        self.rect.x += self.speedx
        self.rect.y += self.speedy
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
        bullet = spriten("bullet.png",20,30,hero.rect.x + 20,hero.rect.y +2,0,4,1,100)
        bulets.add(bullet)
    def nl(self):
        self.speedx += 10
        self.speedy += 10
    def start(self):
        self.rect.x = self.start_x
        self.rect.y = self.start_y
        self.speedx = self.startsx
        self.speedy = self.startsy
    def dmg(self):
        global total
        self.hp -= hero.damage
        if self.hp <= 0:
            self.start()
            total +=1 

font.init()
font = font.SysFont("Roman",40)          
bg = transform.scale(image.load("galaxy.jpg"),(700,500))
hero = spriten("rocket.png",60,60,295,400,6,4,1,100)
enemy = spriten("ufo.png",40,40,10,5,4,0,100,100)
enemy2 = spriten("ufo.png",40,40,140,5,4,0,100,100)
enemy3 = spriten("ufo.png",40,40,270,5,4,0,100,100)
enemy4 = spriten("ufo.png",40,40,400,5,4,0,100,100)
meteor1 = spriten("asteroid.png",70,70,10,10,5,4,200,100)
meteor2 = spriten("asteroid.png",70,70,620,10,-5,4,200,100)
bulets = sprite.Group()
spr = [hero, enemy,enemy2, enemy3,enemy4,meteor1, meteor2]
spr1 = [enemy,enemy2, enemy3,enemy4,meteor1, meteor2]
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
        if finish -speedtime >= 1:
            meteor1.speedx += 1.3
            meteor1.speedy += 1.3
            meteor2.speedy += 1.3
            meteor2.speedx += 1.3
            speedtime = timer.time()
        for s in spr1:
            if sprite.collide_rect(hero,s):
                a = False
        for s in spr1:
            
            if sprite.spritecollide(s,bulets,True):
                s.dmg()
                for bul in bulets:
                    bul.kill()
                

                
        finish = timer.time()
        gametime = finish - start
    else:            
        gametime = int(gametime)
        gametime = str(gametime) 
        end = font.render(" Вы продержались:"+gametime,True,(250,0,0))
        tot = font.render(" Счет:"+str(total),True,(250,250,0))
        skpd = font.render("Пропущено:" +str(skeeped),True,(250,75,0))
        lvl = font.render("Уровень:" +str(int(gametime)//5 +1),True,(150,0,150))
        window.blit(end,(0,100))
        window.blit(skpd,(10,200))
        window.blit(tot,(500,100))
        window.blit(lvl,(475,200))
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