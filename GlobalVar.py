import pygame


class GlobalVariables:
    scale = 31
    day = 0
    turn = 0
    walls = []
    wall_tiles = [
        "Tiles\Wall.png",
    ]
    ground_tiles = [
        "Tiles\Ground.png",
        "Tiles\Ground.png",
        "Tiles\Ground.png",
        "Tiles\Ground1.png"
    ]
    floor = []
    webs = []
    enemys = []
    enemy_attacks = []
    spider_alive = True
    font = None
    FPS = 60