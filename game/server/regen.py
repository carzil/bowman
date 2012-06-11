from random import randrange

class Regen():
    def __init__(self, regen=12):
        self.regen = regen

    def count_regen(self):
        a = randrange(8, 27)
        a /= 10
        return self.regen * a

class ManaRegen():
    def __init__(self, regen=43):
        self.regen = regen

    def count_regen(self):
        a = randrange(5, 19)
        a /= 10
        return self.regen * a
