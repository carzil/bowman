# Copyright 2012 Andreev Alexander <carzil@yandex.ru>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.

class Spell():
    mana = 0
    allow_ally_fire = False

    def count_damage(self, player, opponent, r):
        pass

class FireBall(Spell):
    mana = 300
    
    def count_damage(self, player, opponent, r):
        return False, 230

class HealthBreak(Spell):
    mana = 800

    def count_damage(self, player, opponent, r):
        return False, opponent.health // 4

class Heal(Spell):
    mana = 550
    allow_ally_fire = True

    def count_damage(self, player, opponent, r):
        return False, -320

class Razor(Spell):
    mana = 950
    allow_ally_fire = False

    def count_damage(self, player, opponent, r):
        if r > 14:
            return True, 0
        else:
            return False, 850
