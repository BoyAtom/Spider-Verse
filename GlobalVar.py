import pygame
import numpy


class GlobalVariables:
    scale = 31
    day = 0
    turn = 0
    walls = []
    floor = []
    wall_tiles = [
        "Tiles\Wall.png",
    ]
    ground_tiles = [
        "Tiles\Ground.png",
        "Tiles\Ground.png",
        "Tiles\Ground.png",
        "Tiles\Ground1.png"
    ]
    entrance_tiles = [
        "Tiles\Entrance.png"
    ]
    webs = []
    enemys = []
    enemy_attacks = []
    enemy_dmg = 1
    enemy_hp = 5
    spider_alive = True
    font = None
    FPS = 120

    def DestroyEverything(self, interface):
        self.day = 0
        self.turn = 0
        self.walls.clear()
        self.floor.clear()
        self.webs.clear()
        self.enemys.clear()
        self.enemy_attacks.clear()
        self.enemy_hp = 5
        self.enemy_dmg = 1
        self.spider_alive = True
        interface.day = None
        interface.experience = None
        interface.level = None