from random import randrange

class Regen():
    def __init__(self, regen=12):
        self.regen = regen

    def count_regen(self):
        a = randrange(8, 27)
        a = a // 10
        return self.regen * a

class ManaRegen():
    def __init__(self, regen=59):
        self.regen = regen

    def count_regen(self):
        a = randrange(6, 21)
        a = a // 10
        return self.regen * a
