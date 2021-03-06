import pygame
import random
import math
from Spider import MeleeAttack
from GlobalVar import GlobalVariables as GV

class UndergroundFrog:
    
    health = 5
    max_health = 5
    damage = 3
    xp_treasure = 5
    in_web = None
    orgn_image = None
    image = None
    way = []
    dir = "Top"
    prevX = None
    prevY = None

    def __init__(self, x, y, dmg, hp):
        self.orgn_image = pygame.image.load(r"Tiles\UndergroundFrog.png")
        self.orgn_image = pygame.transform.scale(self.orgn_image, (GV.scale, GV.scale))
        self.image = self.orgn_image
        self.objrect = self.image.get_rect()
        self.objrect.x = x * GV.scale
        self.objrect.y = y * GV.scale
        self.max_health = hp
        self.health = self.max_health
        self.damage = dmg
        self.in_web = False

    def move(self, spider, gVar):
        '''Движение тратит 2 хода'''
        self.collide_web(spider.webs)
        self.collide_attacks(spider)
        self.prevX = self.objrect.x
        self.prevY = self.objrect.y

        pif = math.sqrt((spider.objrect.x/GV.scale - self.objrect.x/GV.scale)**2 + (spider.objrect.y/GV.scale - self.objrect.y/GV.scale)**2)
        if pif > 1.5 and self.in_web == False:
            if spider.objrect.x >= self.objrect.x and random.randint(0, 10) > 7:
                self.turn_to_spider("Right")
                self.objrect.x += GV.scale
            if spider.objrect.y > self.objrect.y and random.randint(0, 10) > 7:
                self.turn_to_spider("Bottom")
                self.objrect.y += GV.scale
            if spider.objrect.x <= self.objrect.x and random.randint(0, 10) > 7:
                self.turn_to_spider("Left")
                self.objrect.x -= GV.scale
            if spider.objrect.y < self.objrect.y and random.randint(0, 10) > 7:
                self.turn_to_spider("Top")
                self.objrect.y -= GV.scale
        elif pif <= 1.5 and self.in_web == False:
            if spider.objrect.x > self.objrect.x and spider.objrect.y == self.objrect.y:
                self.turn_to_spider("Right")
            if spider.objrect.y > self.objrect.y and spider.objrect.x == self.objrect.x:
                self.turn_to_spider("Bottom")
            if spider.objrect.x < self.objrect.x and spider.objrect.y == self.objrect.y:
                self.turn_to_spider("Left")
            if spider.objrect.y < self.objrect.y and spider.objrect.x == self.objrect.x:
                self.turn_to_spider("Top")

        self.collide_wall(spider, gVar.walls)

    def collide_web(self, Webs):
        for i in range(len(Webs)):
            if Webs[i].collision(self):
                self.in_web = True

    def collide_attacks(self, spider):
        for j in range(len(spider.attacks)):
            for i in range(len(spider.attacks)):
                if spider.attacks[i].collision(self):
                    self.health -= spider.attacks[i].damage
                    spider.attacks.pop(i)
                    spider.add_health(1)
                    break
        for j in range(len(spider.range_attacks)):
            for i in range(len(spider.range_attacks)):
                if spider.range_attacks[i].collision(self):
                    self.health -= spider.range_attacks[i].damage
                    spider.range_attacks.pop(i)
                    break

    def collide_wall(self, spider, walls):
        for x in range (len(walls[0])):
            if walls[0][x].collision(self):
                self.objrect.x = self.prevX
                self.objrect.y = self.prevY
            
    def turn_to_spider(self, dir):
        if dir == "Top":
            self.image = pygame.transform.rotate(self.orgn_image, 0)
        elif dir == "Left":
            self.image = pygame.transform.rotate(self.orgn_image, 90)
        elif dir == "Bottom":
            self.image = pygame.transform.rotate(self.orgn_image, 180)
        elif dir == "Right":
            self.image = pygame.transform.rotate(self.orgn_image, 270)
        self.dir = dir

    def attack(self, spider, gVar):
        '''Атака тратит 1 ход'''
        if self.dir == "Top":
            if self.objrect.y - GV.scale == spider.objrect.y and self.objrect.x == spider.objrect.x:
                attack = MeleeAttack(self.objrect.x, self.objrect.y - GV.scale, self.damage, "Tiles\AttackFrog.png", gVar.turn, "Top")
                gVar.enemy_attacks.append(attack)
        elif self.dir == "Left":
            if self.objrect.y == spider.objrect.y and self.objrect.x - GV.scale == spider.objrect.x:
                attack = MeleeAttack(self.objrect.x - GV.scale, self.objrect.y, self.damage, "Tiles\AttackFrog.png", gVar.turn, "Left")
                gVar.enemy_attacks.append(attack)
        elif self.dir == "Bottom":
            if self.objrect.y + GV.scale == spider.objrect.y and self.objrect.x == spider.objrect.x:
                attack = MeleeAttack(self.objrect.x, self.objrect.y + GV.scale, self.damage, "Tiles\AttackFrog.png", gVar.turn, "Bottom")
                gVar.enemy_attacks.append(attack)
        elif self.dir == "Right":
            if self.objrect.y == spider.objrect.y and self.objrect.x + GV.scale == spider.objrect.x:
                attack = MeleeAttack(self.objrect.x + GV.scale, self.objrect.y, self.damage, "Tiles\AttackFrog.png", gVar.turn, "Right")
                gVar.enemy_attacks.append(attack)

    def draw_current_hp(self, gVar):
        '''Отрисовка текущего и максимального здоровья над персонажем'''
        hp = str(self.health) +"/"+ str(self.max_health)
        return gVar.font.render(hp, True, (255, 255, 255))

    def draw(self, gVar, screen):
        screen.blit(self.image, self.objrect)
        screen.blit(self.draw_current_hp(gVar), (self.objrect.x, self.objrect.y - gVar.scale/2))