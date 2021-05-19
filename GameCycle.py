import pygame
from pygame.version import PygameVersion
from Spider import Shiraori
from Enemy import UndergroundFrog
from Underground import Cave
from GlobalVar import GlobalVariables
from Interface import Interface


def main():
    pygame.init()
    pygame.display.set_caption("Spider-Verse")

    clock = pygame.time.Clock()
    cave = Cave()
    spider = Shiraori(21, 12)
    gVar = GlobalVariables()
    gVar.font = pygame.font.Font('Font\PixelFont.ttf', 6)
    interface = Interface(gVar.font)

    for i in range(1):
        gVar.enemys.append(UndergroundFrog(1, 1))
    
    youDied = pygame.font.Font('Font\PixelFont.ttf', 50)
    dieText = youDied.render(("YOU DIED"), True, (255, 255, 255))

    run = True
    screen = pygame.display.set_mode((cave.width * gVar.scale, cave.height * gVar.scale),
                                        pygame.DOUBLEBUF | pygame.FULLSCREEN)

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
                    spider.action = "Attack"
                if event.key == pygame.K_ESCAPE:
                    run = False

        '''Движения существ'''
        if gVar.turn % 15 == 0 and gVar.spider_alive:
            spider.move(gVar.walls)
        if spider.action == "Attack" and gVar.turn % 2 == 0:
            spider.attack(gVar.turn)
        if gVar.turn % 30 == 0 and gVar.spider_alive:
            for i in range (len(gVar.enemys)):
                gVar.enemys[i].attack(spider, gVar)
                gVar.enemys[i].move(spider, gVar.walls)
            gVar.turn = 0
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
        if gVar.spider_alive: 
            spider.collide_attack(gVar.enemy_attacks)
            for i in range(len(gVar.enemys)):
                gVar.enemys[i].collide_attacks(spider)

        '''События'''
        if spider.xp_limit <= interface.experience:
            spider.level_up()
            interface.change_level(1)
            interface.experience = 0

        '''СМЕРТИ!!!'''
        cave.kill_at_0hp(gVar, interface)
        if gVar.spider_alive: cave.del_attacks(spider.attacks, gVar.enemy_attacks, gVar.turn)
        if spider != None and spider.health <= 0:
            spider.die(gVar)
            spider = None

        interface.draw_exp(screen)
        interface.draw_level(screen)
        if gVar.spider_alive == False:
            screen.blit(dieText, ((cave.width / 3) * gVar.scale, (cave.height / 4) * gVar.scale))

        gVar.turn += 1
        pygame.display.flip()
        pygame.display.update()
        clock.tick(gVar.FPS)

    pygame.quit()


main()
