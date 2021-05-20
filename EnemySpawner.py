from Enemy import UndergroundFrog as UF


class Spawner:

    posX = None
    posY = None

    def __init__(self, x, y):
        self.posX = x
        self.posY = y

    def spawn_enemy(self, gVar):
        gVar.enemys.append(UF(self.posX, self.posY))