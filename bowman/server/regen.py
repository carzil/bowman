# Copyright 2012 Boris Tuzhilin
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.

from random import randrange

class Regen():
    def __init__(self, regen=4):
        self.regen = regen

    def count_regen(self):
        a = randrange(5, 26)
        a /= 10
        return round(self.regen * a)

class ManaRegen():
    def __init__(self, regen=12):
        self.regen = regen

    def count_regen(self):
        a = randrange(9, 21)
        a /= 10
        return round(self.regen * a)
