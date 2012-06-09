from random import randrange
from game.server.bowman import NetBowman

class Ranger(NetBowman):
    health = 3800

    max_steps = 5
    max_diagonal_steps = 3

    axe_distance_mod = 0
    bow_distance_mod = 0
    spear_distance_mod = 1

    axe_defense = 7
    bow_defense = 5
    spear_defense = 8

    @property
    def bow_damage_mod(self):
        return randrange(69, 73)

    @property
    def spear_damage_mod(self):
        return randrange(149, 201)

    @property
    def axe_damage_mod(self):
        return randrange(218, 243)

class Damager(NetBowman):
    health = 2500

    max_steps = 6
    max_diagonal_steps = 3

    axe_distance_mod = 0
    bow_distance_mod = 2
    spear_distance_mod = 0

    axe_defense = 4
    bow_defense = 9
    spear_defense = 5

    @property
    def bow_damage_mod(self):
        return randrange(79, 132)

    @property
    def spear_damage_mod(self):
        return randrange(133, 134)

    @property
    def axe_damage_mod(self):
        return randrange(183, 197)

class Tank(NetBowman):
    health = 8000

    max_steps = 5
    max_diagonal_steps = 3

    axe_distance_mod = 1
    bow_distance_mod = 0
    spear_distance_mod = 0

    axe_defense = 14
    bow_defense = 8
    spear_defense = 7

    @property
    def bow_damage_mod(self):
        return randrange(34, 49)

    @property
    def spear_damage_mod(self):
        return randrange(50, 32)

    @property
    def axe_damage_mod(self):
        return randrange(276, 402)

class Mage(NetBowman):
    health = 3167

    max_steps = 5
    max_diagonal_steps = 3

    axe_distance_mod = 0
    bow_distance_mod = 3
    spear_distance_mod = 0

    axe_defense = 2
    bow_defense = 3
    spear_defense = 3

    @property
    def bow_damage_mod(self):
        return randrange(-50, 150)

    @property
    def spear_damage_mod(self):
        return randrange(-80, 200)

    @property
    def axe_damage_mod(self):
        return randrange(-120, 300)
