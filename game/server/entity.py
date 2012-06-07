from random import randrange
from game.server.log import game_log

class Entity():
    collidable = False
    name = "entity"
    symbol = ""
    pickable = False

    def __str__(self):
        return self.symbol

    def damage(self, player):
        return 0

    def register(self, d):
        d[self.symbol] = self

    def apply(self, player):
        pass

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

class HealthPack(Entity):
    lives = 100
    symbol = "+"
    name = "heal"
    pickable = True

    def apply(self, player):
        delta = player.__class__.health - player.health
        game_log.info("delta is %d", delta)
        if delta >= self.lives:
            player.damage(-self.lives)
            game_log.info("health pack picked up")
            return True
        else:
            player.damage(-delta)
            self.lives -= delta
            game_log.info("health pack rest is %d", self.lives)
            return False


