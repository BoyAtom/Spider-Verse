import pygame
from GlobalVar import GlobalVariables as GV

class Shiraori:

    health = 10
    max_health = 10
    action = None
    damage = 1
    dir = "Top"
    attack_dir = "Top"
    max_web = 2
    xp_limit = 10
    webs = []
    attacks = []
    range_attacks = []
    orgn_image = None
    image = None
    objrect = None
    prevX = None
    prevY = None

    def __init__(self, x, y):
        self.orgn_image = pygame.image.load("Tiles\Spider.png")
        self.orgn_image = pygame.transform.scale(self.orgn_image, (GV.scale, GV.scale))
        self.image = self.orgn_image
        self.objrect = self.image.get_rect()
        self.objrect.x = x * GV.scale
        self.objrect.y = y * GV.scale

    def move(self, walls):
        '''Движение тратит ход'''
        self.attack_dir = self.dir
        self.prevX = self.objrect.x
        self.prevY = self.objrect.y
        if self.dir == "Top":
            self.image = pygame.transform.rotate(self.orgn_image, 0)
            self.objrect.y -= GV.scale
            self.dir = None
        elif self.dir == "Left":
            self.image = pygame.transform.rotate(self.orgn_image, 90)
            self.objrect.x -= GV.scale
            self.dir = None
        elif self.dir == "Bottom":
            self.image = pygame.transform.rotate(self.orgn_image, 180)
            self.objrect.y += GV.scale
            self.dir = None
        elif self.dir == "Right":
            self.image = pygame.transform.rotate(self.orgn_image, 270)
            self.objrect.x += GV.scale
            self.dir = None
        self.collide_wall(walls)

    def createWeb(self, gVar):
        '''Создание паутины тратит 2 хода'''
        if self.max_web != len(self.webs):
            self.webs.append(Web(self.objrect.x / gVar.scale, self.objrect.y / gVar.scale))
            gVar.webs = self.webs

    def attack(self, cur_turn):
        '''Атака тратит ход'''
        if self.attack_dir == "Top":
            self.attacks.append(MeleeAttack(self.objrect.x, self.objrect.y - GV.scale, self.damage, "Tiles\AttackSpider.png", cur_turn, "Top"))
        elif self.attack_dir == "Left":
            self.attacks.append(MeleeAttack(self.objrect.x - GV.scale, self.objrect.y, self.damage, "Tiles\AttackSpider.png", cur_turn, "Left"))
        elif self.attack_dir == "Bottom":
            self.attacks.append(MeleeAttack(self.objrect.x, self.objrect.y + GV.scale, self.damage, "Tiles\AttackSpider.png", cur_turn, "Bottom"))
        elif self.attack_dir == "Right":
            self.attacks.append(MeleeAttack(self.objrect.x + GV.scale, self.objrect.y, self.damage, "Tiles\AttackSpider.png", cur_turn, "Right"))
        self.action = None

    def spitVenom(self):
        '''Плевок тратит ход'''
        if self.attack_dir == "Top":
            self.range_attacks.append(RangeAttack(self.objrect.x, self.objrect.y - GV.scale, self.damage, "Top"))
        elif self.attack_dir == "Left":
            self.range_attacks.append(RangeAttack(self.objrect.x - GV.scale, self.objrect.y, self.damage, "Left"))
        elif self.attack_dir == "Bottom":
            self.range_attacks.append(RangeAttack(self.objrect.x, self.objrect.y + GV.scale, self.damage, "Bottom"))
        elif self.attack_dir == "Right":
            self.range_attacks.append(RangeAttack(self.objrect.x + GV.scale, self.objrect.y, self.damage, "Right"))
        self.action = None
        pass

    def collide_wall(self, walls):
        for i in range (len(walls)):
            if walls[i].collision(self):
                self.objrect.x = self.prevX
                self.objrect.y = self.prevY

    def collide_attack(self, enemy_attacks):
        for j in range (len(enemy_attacks)):
            for i in range (len(enemy_attacks)):
                if enemy_attacks[i].collision(self):
                    self.health -= enemy_attacks[i].damage
                    enemy_attacks.pop(i)
                    break

    def add_health(self, amount):
        if self.health + amount <= self.max_health:
            self.health += amount

    def draw_current_hp(self, gVar):
        hp = str(self.health) +"/"+ str(self.max_health)
        return gVar.font.render(hp, True, (255, 255, 255))

    def level_up(self):
        self.max_health += 2
        self.max_web += 2
        if self.xp_limit % 30 == 0:
            self.damage += 1
        self.xp_limit += 5

    def die(self, gVar):
        self.orgn_image = None
        self.image = None
        gVar.spider_alive = False
        pass

    def draw(self, gVar, screen):
        screen.blit(self.image, self.objrect)
        screen.blit(self.draw_current_hp(gVar), (self.objrect.x, self.objrect.y - gVar.scale/2))


class Web:

    img = None

    def __init__(self, x, y):
        '''Значение scale должно быть кратно 8!'''
        self.img = pygame.image.load("Tiles\Web.png")
        self.img = pygame.transform.scale(self.img, (GV.scale, GV.scale))
        self.objrect = self.img.get_rect()
        self.objrect.x = x * GV.scale
        self.objrect.y = y * GV.scale

    def collision(self, object):
        return self.objrect.colliderect(object.objrect)

    def draw(self, screen):
        screen.blit(self.img, self.objrect)


class MeleeAttack:

    img = None
    damage = None
    del_turn = None

    def __init__(self, x, y, damage, image, cur_time, dir):
        '''Значение scale должно быть кратно 8!'''
        self.img = pygame.image.load(image)
        self.img = pygame.transform.scale(self.img, (GV.scale, GV.scale))
        if dir == "Left":
            self.img = pygame.transform.rotate(self.img, 90)
        elif dir == "Bottom":
            self.img = pygame.transform.rotate(self.img, 180)
        elif dir == "Right":
            self.img = pygame.transform.rotate(self.img, 270)
        self.objrect = self.img.get_rect()
        self.objrect.x = x
        self.objrect.y = y
        self.damage = damage
        if cur_time + 5 > 150:
            self.del_turn = cur_time - 145
        else: 
            self.del_turn = cur_time + 5

    def collision(self, object):
        return self.objrect.colliderect(object.objrect)

    def draw(self, screen):
        screen.blit(self.img, self.objrect)

class RangeAttack:
    
    img = None
    damage = None
    dist = 0
    dir = None

    def __init__(self, x, y, damage, dir):
        self.img = pygame.image.load("Tiles\RangeAttackSpider.png")
        self.img = pygame.transform.scale(self.img, (GV.scale, GV.scale))
        if dir == "Left":
            self.img = pygame.transform.rotate(self.img, 90)
        elif dir == "Bottom":
            self.img = pygame.transform.rotate(self.img, 180)
        elif dir == "Right":
            self.img = pygame.transform.rotate(self.img, 270)
        self.objrect = self.img.get_rect()
        self.objrect.x = x
        self.objrect.y = y
        self.dir = dir
        self.damage = damage

    def move(self):
        self.dist += 1
        if self.dir == "Top":
            self.objrect.y -= GV.scale
        elif self.dir == "Left":
            self.objrect.x -= GV.scale
        elif self.dir == "Bottom":
            self.objrect.y += GV.scale
        elif self.dir == "Right":
            self.objrect.x += GV.scale

    def collision(self, object):
        return self.objrect.colliderect(object.objrect)

    def draw(self, screen):
        screen.blit(self.img, self.objrect)