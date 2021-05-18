import pygame
import random
import math
from GlobalVar import GlobalVariables as GV

class UndergroundFrog:
    
    health = 5
    max_health = 5
    damage = 1
    in_web = None
    orgn_image = None
    image = None
    prevX = None
    prevY = None

    def __init__(self, x, y):
        self.orgn_image = pygame.image.load(r"Tiles\UndergroundFrog.png")
        self.orgn_image = pygame.transform.scale(self.orgn_image, (GV.scale, GV.scale))
        self.image = self.orgn_image
        self.objrect = self.image.get_rect()
        self.objrect.x = x * GV.scale
        self.objrect.y = y * GV.scale
        self.in_web = False

    def move(self, spider, walls):
        '''Движение тратит 2 хода'''
        self.collide_web(spider.webs)
        self.collide_attacks(spider)
        self.prevX = self.objrect.x
        self.prevY = self.objrect.y

        pif = math.sqrt((spider.objrect.x/GV.scale - self.objrect.x/GV.scale)**2 + (spider.objrect.y/GV.scale - self.objrect.y/GV.scale)**2)
        if pif > 1.5 and self.in_web == False:
            if spider.objrect.x >= self.objrect.x and random.randint(0, 10) > 6:
                self.image = pygame.transform.rotate(self.orgn_image, 270)
                self.objrect.x += GV.scale
            elif spider.objrect.y > self.objrect.y:
                self.image = pygame.transform.rotate(self.orgn_image, 180)
                self.objrect.y += GV.scale
            if spider.objrect.x <= self.objrect.x and random.randint(0, 10) > 4:
                self.image = pygame.transform.rotate(self.orgn_image, 90)
                self.objrect.x -= GV.scale
            elif spider.objrect.y < self.objrect.y:
                self.image = pygame.transform.rotate(self.orgn_image, 0)
                self.objrect.y -= GV.scale

        self.collide_wall(walls)

    def collide_web(self, Webs):
        for i in range(len(Webs)):
            if Webs[i].collision(self):
                self.in_web = True

    def collide_attacks(self, spider):
        for i in range(len(spider.attacks)):
            if spider.attacks[i].collision(self):
                self.health -= spider.attacks[i].damage
                spider.attacks.pop(i)
                spider.add_health(1)

    def collide_wall(self, walls):
        for i in range (len(walls)):
            if walls[i].collision(self):
                self.objrect.x = self.prevX
                self.objrect.y = self.prevY

    def attack():
        '''Атака тратит 1 ход'''
        pass

    def draw_current_hp(self, gVar):
        '''Отрисовка текущего и максимального здоровья над персонажем'''
        hp = str(self.health) +"/"+ str(self.max_health)
        return gVar.font.render(hp, True, (255, 255, 255))

    def draw(self, gVar, screen):
        screen.blit(self.image, self.objrect)
        screen.blit(self.draw_current_hp(gVar), (self.objrect.x, self.objrect.y - gVar.scale/2))