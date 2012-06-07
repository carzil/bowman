from random import randrange
from game.server.bowman import NetBowman

class Ranger(NetBowman):
    health = 750

    max_steps = 7
    max_diagonal_steps = 3

    axe_distance_mod = 0
    bow_distance_mod = 0
    spear_distance_mod = 0

    axe_defense = 5
    bow_defense = 5
    spear_defense = 5

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
    max_diagonal_steps = 4

    axe_distance_mod = 0
    bow_distance_mod = 0
    spear_distance_mod = 0

    axe_defense = 10
    bow_defense = 2
    spear_defense = 5

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
    max_diagonal_steps = 3

    axe_distance_mod = 0
    bow_distance_mod = 0
    spear_distance_mod = 0

    axe_defense = 5
    bow_defense = 10
    spear_defense = 2

    @property
    def bow_damage_mod(self):
        return randrange(30, 54)

    @property
    def spear_damage_mod(self):
        return randrange(71, 86)

    @property
    def axe_damage_mod(self):
        return randrange(199, 234)
