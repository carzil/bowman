# Copyright 2012 Andreev Alexander <carzil@yandex.ru>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.

from random import randrange, randint
from .const import BASE_BOW_DISTANCE, BASE_SPEAR_DISTANCE, BASE_AXE_DISTANCE
from .log import game_log

class Weapon():
    name = "weapon"

    def __init__(self, damage_mod=0, distance_mod=0):
        self.damage_mod = damage_mod
        self.distance_mod = distance_mod

    def count_damage(self, player, opponent, distance):
        pass

    def count_defense(self, player, opponent, distance):
        pass


class Bow(Weapon):
    name = "bow"

    def count_damage(self, player, opponent, distance):
        if distance - self.distance_mod > BASE_BOW_DISTANCE:
            return True, 0
        else:
            damage = randint(1, 10) + self.damage_mod
            game_log.info("damage mod: %d, damage: %d", self.damage_mod, damage)
            return False, damage

    def count_defense(self, player, opponent, distance):
        a = randrange(11, 20)
        a /= 10
        return round(opponent.bow_defense * a)

class Axe(Weapon):
    name = "axe"

    def count_damage(self, player, opponent, distance):
        if distance - self.distance_mod > BASE_AXE_DISTANCE:
            return True, 0
        else:
            damage = randrange(1, 40) + self.damage_mod
            return False, damage

    def count_defense(self, player, opponent, distance):
        a = randrange(9, 23)
        a /= 10
        return round(opponent.axe_defense * a)

class Spear(Weapon):
    name = "spear"

    def count_damage(self, player, opponent, distance):
        if distance - self.distance_mod > BASE_SPEAR_DISTANCE:
            return True, 0
        else:
            damage = randrange(1, 30) + self.damage_mod
            return False, damage

    def count_defense(self, player, opponent, distance):
        a = randrange(10, 19)
        a /= 10
        return round(opponent.spear_defense * a)
