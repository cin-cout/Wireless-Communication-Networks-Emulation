#p = 0.08 /sec
import pygame
import random
import math

alg = 0
switch = 0
BLACK = (0,0,0)
WHITE = (255,250,250)
RED = (255,0,0)
BLUE = (0,0,255)
ORANGE = (255,160,0)
running = True
FPS = 60

font_name = pygame.font.match_font('arial')
def draw_text(surf,text,size,x,y):
    font = pygame.font.Font(font_name,size)
    text_surface = font.render(text,True,BLACK)
    text_rect = text_surface.get_rect()
    text_rect.center = (x,y)
    surf.blit(text_surface,text_rect)

def _draw_gridlines(screen):
    # 畫網格線 豎線
    for x in range(50,301,25):
        pygame.draw.line(screen, BLACK, (x , 50), (x, 300), 1)
    # 畫網格線 橫線
    for y in range(50,301,25):
        pygame.draw.line(screen, BLACK, (50, y), (300, y), 1)


def alg1(x,y,id):
    global switch
    max = -1
    tempid = -1
    for station in station_sprites.sprites():
        pr = station.get_pr(x,y)
        
        if station.id == id:
            if pr >= 15:
                return id

        if pr>max:
            max = pr
            tempid = station.id
    
    if tempid != id:
        if id != -1:
            switch += 1
    return tempid

def alg2(x,y,id):
    global switch
    max = -1
    tempid = -1
    for station in station_sprites.sprites():
        pr = station.get_pr(x,y)
        if pr>max:
            max = pr
            tempid = station.id
    if tempid != id:
        if id != -1:
            switch += 1
    return tempid

def alg3(x,y,id):
    global switch
    max = -1
    tempid = -1
    for station in station_sprites.sprites():
        pr = station.get_pr(x,y)
        
        if station.id == id:
            prnow = pr
                
        if pr>max:
            max = pr
            tempid = station.id
    
    if id == -1:
        return tempid
    elif max - prnow > 10:
        switch += 1
        return tempid
    else:
        return id

def alg4(x,y,id):
    global switch
    max = -1
    tempid = -1
    for station in station_sprites.sprites():
        dis = station.get_dis(x,y)
        if dis>max:
            max = dis
            tempid = station.id
    if tempid != id:
        if id != -1:
            switch += 1
    return tempid

class Car(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((5,5))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.speed = 1
        self.direct = random.randrange(4)
        self.calltime = random.randrange(1801)
        self.timer = 1
        self.nowstationid = -1

    def update(self):
        if ((self.rect.centerx % 25) == 0) and ((self.rect.centery % 25) ==0):
            i = random.randrange(32)
            if i < 16:
                if self.direct == 0:
                    self.rect.y -= self.speed
                elif self.direct == 1:
                    self.rect.x += self.speed
                elif self.direct == 2:
                    self.rect.y += self.speed
                elif self.direct == 3:
                    self.rect.x -= self.speed
            elif i > 15 and i < 23:
                if self.direct == 0:
                    self.rect.x += self.speed
                    self.direct = 1
                elif self.direct == 1:
                    self.rect.y += self.speed
                    self.direct = 2
                elif self.direct == 2:
                    self.rect.x -= self.speed
                    self.direct = 3
                elif self.direct == 3:
                    self.rect.y -= self.speed
                    self.direct = 0
            elif i > 22 and i < 30:
                if self.direct == 0:
                    self.rect.x -= self.speed
                    self.direct = 3
                elif self.direct == 1:
                    self.rect.y -= self.speed
                    self.direct = 0
                elif self.direct == 2:
                    self.rect.x += self.speed
                    self.direct = 1
                elif self.direct == 3:
                    self.rect.y += self.speed
                    self.direct = 2
            elif i > 29 and i < 32:
                if self.direct == 0:
                    self.rect.y += self.speed
                    self.direct = 2
                elif self.direct == 1:
                    self.rect.x -= self.speed
                    self.direct = 3
                elif self.direct == 2:
                    self.rect.y -= self.speed
                    self.direct = 0
                elif self.direct == 3:
                    self.rect.x += self.speed
                    self.direct = 1
        else:
            if self.direct == 0:
                self.rect.y -= self.speed
            elif self.direct == 1:
                self.rect.x += self.speed
            elif self.direct == 2:
                self.rect.y += self.speed
            elif self.direct == 3:
                self.rect.x -= self.speed 
        if self.rect.centerx < 50 or self.rect.centerx > 300 or self.rect.centery < 50 or self.rect.centery > 300:
            self.kill()
        
        self.timer += 1
        if self.timer >= self.calltime and self.timer <= (self.calltime+180) :
            if int(alg) == 1:
                finalid = alg1(self.rect.centerx,self.rect.centery,self.nowstationid)
            elif int(alg)==2:
                finalid = alg2(self.rect.centerx,self.rect.centery,self.nowstationid)
            elif int(alg)==3:
                finalid = alg3(self.rect.centerx,self.rect.centery,self.nowstationid)
            elif int(alg)==4:
                finalid = alg4(self.rect.centerx,self.rect.centery,self.nowstationid)
            self.nowstationid = finalid
            self.image.fill((255/(self.nowstationid+1),255 - 255/(self.nowstationid+1),0))

        elif self.timer == (self.calltime+181):
            self.image.fill(BLUE)
            self.nowstationid = -1
        elif self.timer > 1800 and self.timer > (self.calltime+181):
            self.timer = 1

class Station(pygame.sprite.Sprite):
    def __init__(self,x,y,f,i):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([5*2,5*2])
        self.image.fill(WHITE) 
        pygame.draw.circle(self.image, ORANGE, (5,5), 5, 0)
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.frequency = f
        self.id = i

    def get_pr(self,cx,cy):
        d = ((self.rect.centerx - cx) ** 2 + (self.rect.centery - cy) ** 2) ** 0.5
        lpf = 32.45 + 20*math.log10(self.frequency)+20*math.log10(d/10)
        pr = 120 - lpf 
        return pr

    def get_dis(self,cx,cy):
        d = ((self.rect.centerx - cx) ** 2 + (self.rect.centery - cy) ** 2) ** 0.5
        return d

print("-----------------------------------------")
print("Please choose one algorithm below:")
print("(1) Minium(Threshold)")
print("(2) Best_effort")
print("(3) Entropy")
print("(4) Myself")
alg = input("Input (1~4): ")

#初始化
pygame.init()
screen = pygame.display.set_mode((350,350))
clock = pygame.time.Clock()
pygame.display.set_caption("WMC Modle")

car_sprites = pygame.sprite.Group()
station_sprites = pygame.sprite.Group()
#car = Car(150,150)
#car_sprites.add(car)

id = 0
for i in range(63,289,25):
    for j in range(63,289,25):
        r = random.randrange(11)
        if r == 0 :
            f = random.randrange(1,11)
            s = random.randrange(4)
            if s ==0:
                station = Station(i+1,j,f*100,id)
            elif s ==1:
                station = Station(i-1,j,f*100,id)
            elif s ==2:
                station = Station(i,j+1,f*100,id)
            elif s ==3:
                station = Station(i,j-1,f*100,id)
            id += 1
            station_sprites.add(station)

#模擬迴圈
while running:
    clock.tick(FPS)
    #結束
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #放車車
    
    for x in range(75,276,25):
        i = random.randrange(101)
        if i < 7 :
            car = Car(x,50)
            car_sprites.add(car)
    for x in range(75,276,25):
        i = random.randrange(101)
        if i < 7 :
            car = Car(x,300)
            car_sprites.add(car)
    for y in range(75,276,25):
        i = random.randrange(101)
        if i < 7 :
            car = Car(50,y)
            car_sprites.add(car)
    for y in range(75,276,25):
        i = random.randrange(101)
        if i < 7 :
            car = Car(300,y)
            car_sprites.add(car)
    
    #更新
    screen.fill(WHITE)
    _draw_gridlines(screen)
    car_sprites.draw(screen)
    station_sprites.draw(screen)
    car_sprites.update()
    draw_text(screen,"Switch time: "+str(switch),18,55,25)
    pygame.display.update()
            
pygame.quit()