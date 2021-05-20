import pygame
import random
from Spider import Shiraori
from Enemy import UndergroundFrog
from EnemySpawner import Spawner
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
    gVar.font = pygame.font.Font('Font\PixelFont.ttf', 7)
    interface = Interface(gVar.font)

    spawned_enemys = 0
    enemy_limit = 4
    spawners = [
        Spawner(20, 0),
        Spawner(0, 11),
        Spawner(41, 11),
        Spawner(20, 22)
    ]
    
    youDied = pygame.font.Font('Font\PixelFont.ttf', 50)
    dieText = youDied.render(("YOU DIED"), True, (255, 255, 255))

    run = True
    screen = pygame.display.set_mode((cave.width * gVar.scale, cave.height * gVar.scale), pygame.FULLSCREEN)

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
        if spider.action == "Attack" and gVar.turn % 2 == 0 and gVar.spider_alive:
            spider.attack(gVar.turn)
        if gVar.turn % 30 == 0 and gVar.spider_alive:
            for i in range (len(gVar.enemys)):
                gVar.enemys[i].attack(spider, gVar)
                gVar.enemys[i].move(spider, gVar.walls)
        if gVar.turn % 150 == 0 and gVar.spider_alive and spawned_enemys != enemy_limit:
            spawners[random.randint(0, 3)].spawn_enemy(gVar)
            spawned_enemys += 1
            gVar.turn = 0
        if spawned_enemys == enemy_limit and len(gVar.enemys) == 0:
            spawned_enemys = 0
            if enemy_limit != 15: enemy_limit += 1
            interface.change_day(1)
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
        interface.draw_day(screen)
        if gVar.spider_alive == False:
            screen.blit(dieText, ((cave.width / 3) * gVar.scale, (cave.height / 4) * gVar.scale))

        gVar.turn += 1
        pygame.display.flip()
        pygame.display.update()
        clock.tick(gVar.FPS)

    pygame.quit()


main()
