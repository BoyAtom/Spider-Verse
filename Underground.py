import pygame
import random
import numpy as np
from Enemy import UndergroundFrog as UF
from GlobalVar import GlobalVariables as GV

class Cave:

    height = 23 #23
    width = 41 #41

    def create_world(self, gvar):
        wls = []
        flr = []
        for x in range(self.height):
            for y in range(self.width):
                if x == 0 or y == 0 or y == self.width-1 or x == self.height-1:
                    if (x == self.height // 2) or (y == self.width // 2):
                        wls.append(Wall(y, x, GV.entrance_tiles[random.randint(0, len(GV.entrance_tiles) - 1)]))
                        print("f", end=' ')
                    else:
                        wls.append(Wall(y, x, GV.wall_tiles[random.randint(0, len(GV.wall_tiles) - 1)]))
                        print("w", end=' ')
                elif x == 1 or y == 1 or y == self.width-2 or x == self.height-2:
                    if (x == self.height // 2) or (y == self.width // 2):
                        flr.append(Floor(y, x, GV.ground_tiles[random.randint(0, len(GV.ground_tiles) - 1)]))
                        print("f", end=' ')
                    else:
                        wls.append(Wall(y, x, GV.wall_tiles[random.randint(0, len(GV.wall_tiles) - 1)]))
                        print("w", end=' ')
                elif x == 2 or y == 2 or y == self.width-3 or x == self.height-3:
                    flr.append(Floor(y, x, GV.ground_tiles[random.randint(0, len(GV.ground_tiles) - 1)]))
                    print("f", end=' ')
                elif random.randint(0, 10) <= 1:
                    wls.append(Wall(y, x, GV.wall_tiles[random.randint(0, len(GV.wall_tiles) - 1)]))
                    print("w", end=' ')
                else:
                    flr.append(Floor(y, x, GV.ground_tiles[random.randint(0, len(GV.ground_tiles) - 1)]))
                    print("f", end=' ')
            print()
        gvar.walls.append(np.array(wls))
        gvar.floor.append(np.array(flr))

    def draw_world(self, gvar, screen):
        for x in range(len(gvar.walls[0])):
            gvar.walls[0][x].draw(screen)
        for x in range(len(gvar.floor[0])):
            gvar.floor[0][x].draw(screen)

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

    tag = "Wall"

    def __init__(self, x, y, image):
        self.img = pygame.image.load(image).convert()
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

    tag = "Floor"

    def __init__(self, x, y, image):
        self.img = pygame.image.load(image).convert()
        self.img = pygame.transform.scale(self.img, (GV.scale, GV.scale))
        self.objrect = self.img.get_rect()
        self.objrect.x = x * GV.scale
        self.objrect.y = y * GV.scale

    def draw(self, screen):
        screen.blit(self.img, self.objrect)