from random import randint

class Regen():
    def __init__(self, regen=0):
        self.regen = regen

    def count_regen(self):
        return randint(0, 15) + self.regen
