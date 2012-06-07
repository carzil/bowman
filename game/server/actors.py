from random import randrange
from game.server.bowman import NetBowman

class Ranger(NetBowman):
    health = 700
    max_steps = 7

    @property
    def bow_damage_mod(self):
        return randrange(70, 115, 5)

    @property
    def spear_damage_mod(self):
        return randrange(125, 150, 5)

    @property
    def axe_damage_mod(self):
        return randrange(150, 180, 5)

class Damager(NetBowman):
    health = 500
    max_steps = 8

    @property
    def bow_damage_mod(self):
        return randrange(100, 135, 5)

    @property
    def spear_damage_mod(self):
        return randrange(140, 165, 5)

    @property
    def axe_damage_mod(self):
        return randrange(180, 230, 5)

class Tank(NetBowman):
    health = 1200
    max_steps = 6

    @property
    def bow_damage_mod(self):
        return randrange(50, 80, 5)

    @property
    def spear_damage_mod(self):
        return randrange(80, 115, 5)

    @property
    def axe_damage_mod(self):
        return randrange(200, 250, 5)
