import pygame
import random
from Spider import Shiraori
from Enemy import UndergroundFrog
from EnemySpawner import Spawner
from Underground import Cave
from GlobalVar import GlobalVariables
from Interface import Interface
from pygame.locals import *

pygame.init()

clock = pygame.time.Clock()
cave = Cave()
gVar = GlobalVariables()
gVar.font = pygame.font.Font('Font\oneFont.ttf', 7)
win = pygame.display.set_mode([cave.width * gVar.scale, cave.height * gVar.scale],
                                     pygame.DOUBLEBUF | pygame.FULLSCREEN)
background_image = pygame.image.load('Images\BackGr.jpg')
HelpG = pygame.image.load('Images\help.jpg')

class button():
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, win, outline=None):
        # Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 2)

        if self.text != '':
            font = pygame.font.Font('Font\oneFont.ttf', 55) # Размер шрифта
            text = font.render(self.text, 1, (255, 255, 255)) # Цвет букв в главном меню
            win.blit(text, (self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False


def redrawMenuWindow():
    #win.fill((0, 180, 210)) - одноцветный фон
    win.blit(background_image,(5, 5))
    greenButton.draw(win, (0, 0, 0))
    redButton.draw(win, (0, 0, 0))
    listButton.draw(win, (0, 0, 0))
    helpButton.draw(win, (0, 0, 0))

#ИГРА НАЧИНАЕТСЯ ТУТ

def main():
    pygame.init()
    screen = pygame.display.set_mode([41 * 31, 23 * 31], 
                                            pygame.DOUBLEBUF | pygame.FULLSCREEN | pygame.HWSURFACE)
    pygame.display.set_caption("Spider-Verse")

    gVar = GlobalVariables()
    gVar.font = pygame.font.Font('Font\PixelFont.ttf', 7)
    clock = pygame.time.Clock()
    cave = Cave()
    spider = Shiraori(cave.width // 2, cave.height // 2)
    interface = Interface(gVar.font)

    spawned_enemys = 0
    enemy_limit = 4
    spawners = [
        Spawner(1, cave.height // 2),
        Spawner(cave.width // 2, cave.height - 2),
        Spawner(cave.width - 2, cave.height // 2),
        Spawner(cave.width // 2, 1)
    ]

    youDied = pygame.font.Font('Font\PixelFont.ttf', 50)
    dieText = youDied.render(("YOU DIED"), True, (255, 0, 0))

    game_state = "game"

    cave.create_world(gVar)

    while game_state == "game":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
               game_state = "menu"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_state = "menu"
                    gVar.DestroyEverything(interface)
                    cave = None
                    spider = None
                    spawners.clear()
                    gVar = None
                    interface = None
                    screen.fill((0, 0, 0))
                    screen = None
                    pygame.display.flip()
                    pygame.display.update()
                if event.key == pygame.K_c:
                    spider.createWeb(gVar)
                
        if game_state == "game":

            '''Обработка зажатий клавиш'''
            key = pygame.key.get_pressed()
            if gVar.spider_alive and gVar.turn % 25 == 0:
                if key[pygame.K_UP]:
                    spider.move(gVar, "Top")
                if key[pygame.K_DOWN]:
                    spider.move(gVar, "Bottom")
                if key[pygame.K_LEFT]:
                    spider.move(gVar, "Left")
                if key[pygame.K_RIGHT]:
                    spider.move(gVar, "Right")
                if key[pygame.K_z]:
                    spider.attack(gVar.turn)
                if key[pygame.K_x]:
                    spider.spitVenom()

            '''Движения существ'''
            if gVar.spider_alive and gVar.turn % 8 == 0 and len(spider.range_attacks) != 0:
                for i in range(len(spider.range_attacks)):
                    spider.range_attacks[i].move()
            if gVar.spider_alive and gVar.turn % 50 == 0:
                for i in range(len(gVar.enemys)):
                    gVar.enemys[i].attack(spider, gVar)
                    gVar.enemys[i].move(spider, gVar)
            if gVar.turn % 480 == 0 and gVar.spider_alive and spawned_enemys != enemy_limit:
                spawners[random.randint(0, 3)].spawn_enemy(gVar)
                spawned_enemys += 1
                gVar.turn = 0
            if spawned_enemys == enemy_limit and len(gVar.enemys) == 0:
                spawned_enemys = 0
                if enemy_limit != 50: enemy_limit += 1
                interface.change_day(1)
                if interface.day%5 == 0: gVar.enemy_dmg += 1
                gVar.enemy_hp += 1
            if gVar.spider_alive: spider.action = None

            '''Очистка экрана'''
            screen.fill((0, 0, 0))

            '''Отрисовка карты'''
            cave.draw_world(gVar, screen)
            cave.draw_webs(gVar, screen)

            '''Отрисовка существ'''
            for i in range(len(gVar.enemys)):
                gVar.enemys[i].draw(gVar, screen)
            if gVar.spider_alive: spider.draw(gVar, screen)

            '''Отрисовка атак'''
            if gVar.spider_alive: cave.draw_attacks(spider, screen)
            cave.draw_enemy_attacks(gVar, screen)
            for x in range(len(gVar.walls[0])):
                if gVar.spider_alive: 
                    gVar.walls[0][x].collide_bullet(spider)
            if gVar.spider_alive:
                spider.collide_attack(gVar.enemy_attacks)
                for i in range(len(gVar.enemys)):
                    gVar.enemys[i].collide_attacks(spider)

            '''События'''
            if gVar.spider_alive and spider.xp_limit <= interface.experience:
                spider.level_up()
                interface.change_level(1)
                interface.experience = 0

            '''СМЕРТИ!!!'''
            cave.kill_at_0hp(gVar, interface)
            if gVar.spider_alive and gVar.turn %2 == 0: cave.del_attacks(spider.attacks, gVar.enemy_attacks, spider.range_attacks, gVar.turn)
            if spider != None and spider.health <= 0:
                spider.die(gVar)
                spider = None

            interface.draw_exp(screen)
            interface.draw_level(screen)
            interface.draw_day(screen)
            if gVar.spider_alive == False:
                screen.blit(dieText, ((cave.width / 3) * gVar.scale, (cave.height / 4) * gVar.scale))

            gVar.turn += 1
            pygame.display.flip()
            pygame.display.update()
            print(clock.get_fps())
            clock.tick(gVar.FPS)

    menu()

### ИГРА ЗАКАНЧИВАЕТСЯ ТУТ


greenButton = button((0, 255, 0), cave.width * gVar.scale//3,cave.height * gVar.scale//3, 400, 100, "Начать игру")
redButton = button((255, 0, 0), cave.width * gVar.scale//3,cave.height * gVar.scale//1.2, 400, 100, "Выйти")
listButton = button((255, 0, 0), cave.width * gVar.scale//3,cave.height * gVar.scale//1.5, 400, 100, "Читы")
helpButton = button((0, 0, 0), cave.width * gVar.scale//3,cave.height * gVar.scale//2, 400, 100, "Инструкция и управление")

def menu():
    game_state = "menu"
    run = True
    while run:
        if game_state == "menu":
            redrawMenuWindow()
        elif game_state == "game":
            main()
        pygame.display.update()

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

            if game_state == "menu":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if greenButton.isOver(pos):
                        print("clicked the button")
                        game_state = "game"
                    if redButton.isOver(pos):
                        print("clicked the 2button")
                        run = False
                        pygame.quit()
                        quit()
                    if listButton.isOver(pos):
                        print("clicked the 3button")
                        while game_state == 'menu':
                            win.blit(pygame.image.load('Images\Ham.jpg').convert(), (cave.width * gVar.scale//4,cave.height * gVar.scale//50))
                            pygame.display.flip()
                            for event in pygame.event.get():
                                if event.type == pygame.KEYDOWN:
                                    if event.key == pygame.K_ESCAPE:
                                        pygame.quit()
                                        quit()
                    if helpButton.isOver(pos):
                        print("clicked the 4button")
                        game_state = 'help'
                        while game_state == 'help':
                            win.blit(HelpG,(5, 5))
                            pygame.display.update()
                            for event in pygame.event.get():
                                if event.type == pygame.KEYDOWN:
                                    if event.key == pygame.K_ESCAPE:
                                        game_state = 'menu'
                                        pygame.display.update()

                if event.type == pygame.MOUSEMOTION:
                    if greenButton.isOver(pos):
                        greenButton.color = (0, 0, 0)
                    else:
                        greenButton.color = (255, 255, 255)
                    if redButton.isOver(pos):
                        redButton.color = (0, 0, 0)
                    else:
                        redButton.color = (255, 255, 255)
                    if listButton.isOver(pos):
                        listButton.color = (0, 0, 0)
                    else:
                        listButton.color = (255, 255, 255)
                    if helpButton.isOver(pos):
                        helpButton.color = (0, 0, 0)
                    else:
                        helpButton.color = (255, 255, 255)

menu()