from random import randrange
from game.server.bowman import NetBowman

class Ranger(NetBowman):
    health = 750
    max_steps = 7

    @property
    def bow_damage_mod(self):
        return 60

    @property
    def spear_damage_mod(self):
        return 100

    @property
    def axe_damage_mod(self):
        return 120

class Damager(NetBowman):
    health = 550
    max_steps = 8

    @property
    def bow_damage_mod(self):
        return 110

    @property
    def spear_damage_mod(self):
        return 120

    @property
    def axe_damage_mod(self):
        return 140

class Tank(NetBowman):
    health = 1200
    max_steps = 6

    @property
    def bow_damage_mod(self):
        return 40

    @property
    def spear_damage_mod(self):
        return 70

    @property
    def axe_damage_mod(self):
        return 180
