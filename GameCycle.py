import pygame
from Spider import Shiraori
from Enemy import UndergroundFrog
from Underground import Cave
from GlobalVar import GlobalVariables


def main():
    pygame.init()

    cave = Cave()
    spider = Shiraori(10, 10)
    gVar = GlobalVariables()
    gVar.font = pygame.font.Font('Font\PixelFont.ttf', 6)
    for i in range(1):
        gVar.enemys.append(UndergroundFrog(1, 1))

    run = True
    screen = pygame.display.set_mode((cave.width * gVar.scale, cave.height * gVar.scale))

    cave.create_world(gVar)

    while run:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    spider.dir = "Top"
                if event.key == pygame.K_s:
                    spider.dir = "Bottom"
                if event.key == pygame.K_a:
                    spider.dir = "Left"
                if event.key == pygame.K_d:
                    spider.dir = "Right"
                if event.key == pygame.K_q:
                    spider.createWeb(gVar)
                if event.key == pygame.K_e:
                    spider.attack(gVar.turn)

        '''Движения существ'''
        if gVar.turn % 30 == 0:
            spider.move(gVar.walls)
        if gVar.turn % 60 == 0:
            for i in range (len(gVar.enemys)):
                gVar.enemys[i].attack(spider, gVar)
                gVar.enemys[i].move(spider, gVar.walls)
            gVar.turn = 0

        '''Очистка экрана'''
        screen.fill((0, 0, 0))

        '''Отрисовка карты'''
        cave.draw_world(gVar, screen)
        cave.draw_webs(gVar, screen)

        '''Отрисовка существ'''
        for i in range(len(gVar.enemys)):
            gVar.enemys[i].draw(gVar, screen)
        if gVar.spider_alive != False: spider.draw(gVar, screen)

        '''Отрисовка атак'''
        cave.draw_attacks(spider, screen)
        cave.draw_enemy_attacks(gVar, screen)

        if gVar.spider_alive != False: spider.collide_attack(gVar.enemy_attacks)
        for i in range(len(gVar.enemys)):
            gVar.enemys[i].collide_attacks(spider)

        cave.del_attacks(spider.attacks, gVar.enemy_attacks, gVar.turn)
        cave.kill_at_0hp(gVar)
        if spider.health <= 0:
            spider.die(gVar)

        gVar.turn += 1
        pygame.display.flip()
        pygame.display.update()

    pygame.quit()


main()
