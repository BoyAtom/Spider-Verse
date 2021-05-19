import pygame
from GlobalVar import GlobalVariables as GV


class Interface:

    day = None
    experience = None
    level = None
    font = None

    def __init__(self, font, day = 0, expirience = 0, level = 0):
        self.day = day
        self.experience = expirience
        self.level = level
        self.font = font
    
    def change_exp(self, amount):
        self.experience += amount

    def draw_exp(self, screen):
        screen.blit(self.font.render(("Опыт " + str(self.experience)), True, (255, 255, 255)), (0, 0))

    def change_level(self, amount):
        self.level += amount

    def draw_level(self, screen):
        screen.blit(self.font.render(("Уровень " + str(self.level)), True, (255, 255, 255)), (0, GV.scale / 2))