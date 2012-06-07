from random import randrange
from game.server.bowman import NetBowman

class Ranger(NetBowman):
    health = 900

    max_steps = 6
    max_diagonal_steps = 3

    axe_distance_mod = 0
    bow_distance_mod = 1
    spear_distance_mod = 1

    axe_defense = 10
    bow_defense = 10
    spear_defense = 15

    @property
    def bow_damage_mod(self):
        return randrange(55, 87)

    @property
    def spear_damage_mod(self):
        return randrange(113, 143)

    @property
    def axe_damage_mod(self):
        return randrange(170, 200)

class Damager(NetBowman):
    health = 700

    max_steps = 8
    max_diagonal_steps = 4

    axe_distance_mod = 0
    bow_distance_mod = 2
    spear_distance_mod = 0

    axe_defense = 0
    bow_defense = 10
    spear_defense = 8

    @property
    def bow_damage_mod(self):
        return randrange(134, 156)

    @property
    def spear_damage_mod(self):
        return randrange(145, 165)

    @property
    def axe_damage_mod(self):
        return randrange(160, 190)

class Tank(NetBowman):
    health = 2400

    max_steps = 6
    max_diagonal_steps = 3

    axe_distance_mod = 1
    bow_distance_mod = 0
    spear_distance_mod = 0

    axe_defense = 15
    bow_defense = 10
    spear_defense = 12

    @property
    def bow_damage_mod(self):
        return randrange(13, 54)

    @property
    def spear_damage_mod(self):
        return randrange(45, 97)

    @property
    def axe_damage_mod(self):
        return randrange(213, 299)
