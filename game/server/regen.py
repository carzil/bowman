from random import randint

class Regen():
    def __init__(self, regen=12):
        self.regen = regen

    def count_regen(self):
        return self.regen * randint(0, 5)

class ManaRegen():
    def __init__(self, regen=43):
        self.regen = regen

    def count_regen(self):
        return self.regen * randint(0, 5)
