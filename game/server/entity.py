from random import randrange

class Entity():
    collidable = False
    name = "entity"
    symbol = ""

    def __str__(self):
        return self.symbol

    def damage(self, player):
        return 0

    def register(self, d):
        d[self.symbol] = self

class Grass(Entity):
    name = "grass"
    symbol = "."

class Wall(Entity):
    collidable = True
    name = "wall"
    symbol = "*"

class Spikes(Entity):
    name = "spikes"
    symbol = "#"

    def damage(self, player):
        return randrange(20, 100)
