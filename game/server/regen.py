from random import randrange

class Regen():
    def __init__(self, regen=4):
        self.regen = regen

    def count_regen(self):
        a = randrange(8, 24)
        a /= 10
        return round(self.regen * a)

class ManaRegen():
    def __init__(self, regen=13):
        self.regen = regen

    def count_regen(self):
        a = randrange(6, 18)
        a /= 10
        return round(self.regen * a)
