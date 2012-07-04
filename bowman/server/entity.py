# Copyright 2012 Andreev Alexander <carzil@yandex.ru>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.

from random import randrange
from .log import game_log

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
        return randrange(120, 130)

class HealthPack(Entity):
    lives = 200
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

class SpawnPoint(Entity):
    symbol = "&"
    name = "spawn point"


