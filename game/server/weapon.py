from random import randrange, randint

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
        if distance - self.distance_mod > 16:
            return True, 0
        else:
            damage = randrange(10, 20) + self.damage_mod
            return False, damage

    def count_defense(self, player, opponent, distance):
        a = randrange(7, 21)
        a /= 10
        return opponent.bow_defense * a

class Axe(Weapon):
    name = "axe"

    def count_damage(self, player, opponent, distance):
        if distance - self.distance_mod > 2:
            return True, 0
        else:
            damage = randrange(20, 60) + self.damage_mod
            return False, damage

    def count_defense(self, player, opponent, distance):
        a = randrange(15, 28)
        a /= 10
        return opponent.axe_defense * a

class Spear(Weapon):
    name = "spear"

    def count_damage(self, player, opponent, distance):
        if distance - self.distance_mod > 8:
            return True, 0
        else:
            damage = randrange(25, 35) + self.damage_mod
            return False, damage

    def count_defense(self, player, opponent, distance):
        a = randrange(9, 24)
        a /= 10
        return opponent.spear_defense * a
