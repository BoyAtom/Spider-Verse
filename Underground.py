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
                    if (x == 20) or (y == 11):
                        gvar.floor.append(Floor(x, y, GV.ground_tiles[random.randint(0, len(GV.ground_tiles) - 1)]))
                    else: 
                        gvar.walls.append(Wall(x, y, GV.wall_tiles[random.randint(0, len(GV.wall_tiles) - 1)]))
                elif x == 1 or y == 1 or x == self.width-2 or y == self.height-2:
                    gvar.floor.append(Floor(x, y, GV.ground_tiles[random.randint(0, len(GV.ground_tiles) - 1)]))
                elif random.randint(0, 10) <= 1:
                    gvar.walls.append(Wall(x, y, GV.wall_tiles[random.randint(0, len(GV.wall_tiles) - 1)]))
                else:
                    gvar.floor.append(Floor(x, y, GV.ground_tiles[random.randint(0, len(GV.ground_tiles) - 1)]))

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
        for i in range(len(spider.range_attacks)):
            spider.range_attacks[i].draw(screen)

    def draw_enemy_attacks(self, gVar, screen):
        for i in range(len(gVar.enemy_attacks)):
            gVar.enemy_attacks[i].draw(screen)

    def kill_at_0hp(self, gvar, iface):
        for j in range (len(gvar.enemys)):
            for i in range (len(gvar.enemys)):
                if gvar.enemys[i].health <= 0:
                    iface.change_exp(gvar.enemys[i].xp_treasure)
                    gvar.enemys.pop(i)
                    break
    
    def del_attacks(self, attacks, enemy_attacks, range_attacks, cur_turn):
        for j in range(len(attacks)):
            for i in range(len(attacks)):
                if attacks[i].del_turn == cur_turn or len(attacks) >= 1:
                    attacks.pop(i)
                    break
        for j in range(len(enemy_attacks)):
            for i in range(len(enemy_attacks)):
                if enemy_attacks[i].del_turn == cur_turn:
                    enemy_attacks.pop(i)
                    break
        for j in range(len(range_attacks)):
            for i in range(len(range_attacks)):
                if range_attacks[i].dist == 4:
                    range_attacks.pop(i)
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

    def collide_bullet(self, spider):
        for j in range(len(spider.range_attacks)):
            for i in range(len(spider.range_attacks)):
                if spider.range_attacks[i].collision(self):
                    spider.range_attacks.pop(i)
                    break

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