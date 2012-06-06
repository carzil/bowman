from random import randrange

class Weapon():
    name = "weapon"

    def __init__(self, damage_mod=0):
        self.damage_mod = damage_mod

    def count_damage(self, player, opponent, distance):
        pass

class Bow(Weapon):
    name = "bow"

    def count_damage(self, player, opponent, distance):
        if distance > 20:
            return True, 0
        else:
            damage = randrange(40, 60) + self.damage_mod
            return False, damage

class Axe(Weapon):
    name = "axe"

    def count_damage(self, player, opponent, distance):
        if distance > 2:
            return True, 0
        else:
            damage = randrange(150, 200) + self.damage_mod
            return False, damage

class Spear(Weapon):
    name = "spear"

    def count_damage(self, player, opponent, distance):
        if distance > 9:
            return True, 0
        else:
            damage = randrange(80, 120) + self.damage_mod
            return False, damage
