from random import randrange
from game.server.bowman import NetBowman

class Ranger(NetBowman):
    health = 1150

    max_steps = 5
    max_diagonal_steps = 3

    axe_distance_mod = 0
    bow_distance_mod = 0
    spear_distance_mod = 1

    axe_defense = 16
    bow_defense = 4
    spear_defense = 7

    @property
    def bow_damage_mod(self):
<<<<<<< Updated upstream
        return randrange(32, 56)

    @property
    def spear_damage_mod(self):
        return randrange(145, 169)

    @property
    def axe_damage_mod(self):
        return randrange(190, 230)
=======
        return randrange(25, 39)

    @property
    def spear_damage_mod(self):
        return randrange(79, 113)

    @property
    def axe_damage_mod(self):
        return randrange(101, 143)
>>>>>>> Stashed changes

class Damager(NetBowman):
    health = 800

    max_steps = 6
    max_diagonal_steps = 3

    axe_distance_mod = 0
    bow_distance_mod = 2
    spear_distance_mod = 0

    axe_defense = 3
    bow_defense = 13
    spear_defense = 9

    @property
    def bow_damage_mod(self):
<<<<<<< Updated upstream
        return randrange(114, 211)

    @property
    def spear_damage_mod(self):
        return randrange(99, 145)

    @property
    def axe_damage_mod(self):
        return randrange(198, 199)
=======
        return randrange(65, 103)

    @property
    def spear_damage_mod(self):
        return randrange(69, 111)

    @property
    def axe_damage_mod(self):
        return randrange(120, 130)
>>>>>>> Stashed changes

class Tank(NetBowman):
    health = 2400

    max_steps = 5
    max_diagonal_steps = 3

    axe_distance_mod = 1
    bow_distance_mod = 0
    spear_distance_mod = 0

    axe_defense = 17
    bow_defense = 11
    spear_defense = 14

    @property
    def bow_damage_mod(self):
<<<<<<< Updated upstream
        return randrange(13, 54)

    @property
    def spear_damage_mod(self):
        return randrange(45, 87)

    @property
    def axe_damage_mod(self):
        return randrange(237, 331)
=======
        return randrange(14, 41)

    @property
    def spear_damage_mod(self):
        return randrange(22, 56)

    @property
    def axe_damage_mod(self):
        return randrange(156, 189)
>>>>>>> Stashed changes

class Mage(NetBowman):
    health = 1060

    max_steps = 5
    max_diagonal_steps = 3

    axe_distance_mod = 0
    bow_distance_mod = 100
    spear_distance_mod = 0

    axe_defense = 3
    bow_defense = 5
    spear_defense = 4

    @property
    def bow_damage_mod(self):
<<<<<<< Updated upstream
        return randrange(-10, 20)

    @property
    def spear_damage_mod(self):
        return randrange(-20, 100)

    @property
    def axe_damage_mod(self):
        return randrange(0, 301, 300)
=======
        return randrange(-20, 80, 99)

    @property
    def spear_damage_mod(self):
        return randrange(-40, 160, 199)

    @property
    def axe_damage_mod(self):
        return randrange(-50, 210, 259)
>>>>>>> Stashed changes
