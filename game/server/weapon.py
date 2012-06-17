from random import randrange, randint
from game.server.const import BASE_BOW_DISTANCE, BASE_SPEAR_DISTANCE, BASE_AXE_DISTANCE

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
            damage = randrange(20, 30) + self.damage_mod
            return False, damage

    def count_defense(self, player, opponent, distance):
        a = randrange(6, 20)
        a /= 10
        return round(opponent.bow_defense * a)

class Axe(Weapon):
    name = "axe"

    def count_damage(self, player, opponent, distance):
        if distance - self.distance_mod > BASE_AXE_DISTANCE:
            return True, 0
        else:
            damage = randrange(40, 60) + self.damage_mod
            return False, damage

    def count_defense(self, player, opponent, distance):
        a = randrange(9, 25)
        a /= 10
        return round(opponent.axe_defense * a)

class Spear(Weapon):
    name = "spear"

    def count_damage(self, player, opponent, distance):
        if distance - self.distance_mod > BASE_SPEAR_DISTANCE:
            return True, 0
        else:
            damage = randrange(30, 40) + self.damage_mod
            return False, damage

    def count_defense(self, player, opponent, distance):
        a = randrange(9, 22)
        a /= 10
        return round(opponent.spear_defense * a)
