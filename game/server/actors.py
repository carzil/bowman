from random import randrange
from game.server.bowman import NetBowman

class Ranger(NetBowman):
    health = 750
    max_steps = 7

    @property
    def bow_damage_mod(self):
        return randrange(60, 83)

    @property
    def spear_damage_mod(self):
        return randrange(91, 112)

    @property
    def axe_damage_mod(self):
        return randrange(134, 167)

class Damager(NetBowman):
    health = 550
    max_steps = 8

    @property
    def bow_damage_mod(self):
        return randrange(103, 142)

    @property
    def spear_damage_mod(self):
        return randrange(143, 151)

    @property
    def axe_damage_mod(self):
        return randrange(181, 210)

class Tank(NetBowman):
    health = 1200
    max_steps = 6

    @property
    def bow_damage_mod(self):
        return randrange(30, 54)

    @property
    def spear_damage_mod(self):
        return randrange(71, 86)

    @property
    def axe_damage_mod(self):
        return randrange(199, 234)
