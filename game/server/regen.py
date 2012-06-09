from random import randint

class Regen():
    def __init__(self, regen=14):
        self.regen = regen

    def count_regen(self):
        return self.regen

class ManaRegen():
    def __init__(self, regen=25):
        self.regen = regen

    def count_regen(self):
        return self.regen
