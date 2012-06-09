from random import randrange
from game.server.bowman import NetBowman

class Ranger(NetBowman):
    health = 1150

    max_steps = 6
    max_diagonal_steps = 3

    axe_distance_mod = 0
    bow_distance_mod = 1
    spear_distance_mod = 1

    axe_defense = 16
    bow_defense = 4
    spear_defense = 7

    @property
    def bow_damage_mod(self):
        return randrange(16, 28)

    @property
    def spear_damage_mod(self):
        return randrange(72, 84)

    @property
    def axe_damage_mod(self):
        return randrange(95, 115)

class Damager(NetBowman):
    health = 800

    max_steps = 8
    max_diagonal_steps = 4

    axe_distance_mod = 0
    bow_distance_mod = 2
    spear_distance_mod = 0

    axe_defense = 3
    bow_defense = 13
    spear_defense = 9

    @property
    def bow_damage_mod(self):
        return randrange(57, 105)

    @property
    def spear_damage_mod(self):
        return randrange(49, 72)

    @property
    def axe_damage_mod(self):
        return randrange(99, 100)

class Tank(NetBowman):
    health = 2400

    max_steps = 6
    max_diagonal_steps = 3

    axe_distance_mod = 1
    bow_distance_mod = 0
    spear_distance_mod = 0

    axe_defense = 17
    bow_defense = 11
    spear_defense = 14

    @property
    def bow_damage_mod(self):
        return randrange(6, 27)

    @property
    def spear_damage_mod(self):
        return randrange(22, 43)

    @property
    def axe_damage_mod(self):
        return randrange(118, 165)

class Mage(NetBowman):
    health = 1060

    max_steps = 6
    max_diagonal_steps = 3

    axe_distance_mod = 0
    bow_distance_mod = 100
    spear_distance_mod = 0

    axe_defense = 3
    bow_defense = 5
    spear_defense = 4

    @property
    def bow_damage_mod(self):
        return randrange(-5, 10)

    @property
    def spear_damage_mod(self):
        return randrange(-10, 50)

    @property
    def axe_damage_mod(self):
        return randrange(0, 151, 150)
