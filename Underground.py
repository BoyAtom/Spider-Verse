import pygame
import random
from Enemy import UndergroundFrog as UF
from GlobalVar import GlobalVariables as GV

class Cave:

    height = 23
    width = 41

    def create_world(self, gvar):
        for x in range(self.width):
            for y in range(self.height):
                if x == 0 or y == 0 or x == self.width-1 or y == self.height-1:
                    gvar.walls.append(Wall(x, y, "Tiles\Wall.png"))
                elif x == 1 or y == 1 or x == self.width-2 or y == self.height-2:
                    gvar.floor.append(Floor(x, y, "Tiles\Ground.png"))
                elif random.randint(0, 10) <= 2:
                    gvar.walls.append(Wall(x, y, "Tiles\Wall.png"))
                else:
                    gvar.floor.append(Floor(x, y, "Tiles\Ground.png"))

    def draw_world(self, gvar, screen):
        for i in range(len(gvar.walls)):
            gvar.walls[i].draw(screen)

        for i in range(len(gvar.floor)):
            gvar.floor[i].draw(screen)

    def draw_webs(self, gvar, screen):
        for i in range(len(gvar.webs)):
            gvar.webs[i].draw(screen)

    def draw_attacks(self, spider, screen):
        for i in range(len(spider.attacks)):
            spider.attacks[i].draw(screen)

    def draw_enemy_attacks(self, gVar, screen):
        for i in range(len(gVar.enemy_attacks)):
            gVar.enemy_attacks[i].draw(screen)

    def kill_at_0hp(self, gvar, iface):
        for j in range (len(gvar.enemys)):
            for i in range (len(gvar.enemys)):
                if gvar.enemys[i].health <= 0:
                    iface.change_exp(gvar.enemys[i].xp_treasure)
                    gvar.enemys.pop(i)
                    gvar.enemys.append(UF(1, 1))
                    break
    
    def del_attacks(self, attacks, enemy_attacks, cur_turn):
        for j in range(len(attacks)):
            for i in range(len(attacks)):
                if attacks[i].del_turn == cur_turn:
                    attacks.pop(i)
                    break
        for j in range(len(enemy_attacks)):
            for i in range(len(enemy_attacks)):
                if enemy_attacks[i].del_turn == cur_turn:
                    enemy_attacks.pop(i)
                    break


class Wall:
    def __init__(self, x, y, image):
        '''Значение scale должно быть кратно 8!'''
        self.img = pygame.image.load(image)
        self.img = pygame.transform.scale(self.img, (GV.scale, GV.scale))
        self.objrect = self.img.get_rect()
        self.objrect.x = x * GV.scale
        self.objrect.y = y * GV.scale

    def collision(self, object):
        return self.objrect.colliderect(object.objrect)

    def draw(self, screen):
        screen.blit(self.img, self.objrect)

class Floor:
    def __init__(self, x, y, image):
        '''Значение scale должно быть кратно 8!'''
        self.img = pygame.image.load(image)
        self.img = pygame.transform.scale(self.img, (GV.scale, GV.scale))
        self.objrect = self.img.get_rect()
        self.objrect.x = x * GV.scale
        self.objrect.y = y * GV.scale

    def draw(self, screen):
        screen.blit(self.img, self.objrect)