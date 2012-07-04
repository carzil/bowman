# Copyright 2012 Andreev Alexander <carzil@yandex.ru>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.

from .log import game_log

class Spell():
    mana = 0
    allow_ally_fire = False

    continuous = False
    finished = False

    symbols = []

    description = ""

    def count_damage(self, player, opponent, r):
        pass

    def apply(self, player):
        pass

class FireBall(Spell):
    mana = 140

    symbols = ["f", "fb"]

    description = "simple spell, little damage"
    
    def count_damage(self, player, opponent, r):
        return False, 215

class HealthBreak(Spell):
    mana = 450

    symbols = ["hb"]

    description = "decrease enemy's lives on 25%"

    def count_damage(self, player, opponent, r):
        return False, opponent.health // 4

class Heal(Spell):
    mana = 340
    allow_ally_fire = True

    symbols = ["h"]

    description = "heal any player"

    def count_damage(self, player, opponent, r):
        return False, -400

class Razor(Spell):
    mana = 480
    allow_ally_fire = False

    symbols = ["r", "rz"]

    description = "ultra-spell, big damage"

    def count_damage(self, player, opponent, r):
        if r > 14:
            return True, 0
        else:
            return False, 690

class Poison(Spell):
    continuous = True
    mana = 200
    times = 5
    damage = 65
    symbols = ["p"]

    description = "simple continuous spell"

    def apply(self, player):
        if self.times <= 0:
            game_log.info("poison on player %d", player.n)
            self.finished = True
        else:
            player.damage(self.damage)
            game_log.info("player %d poisoned by %d", player.n, self.damage)
            self.times -= 1

class AllyPoison(Poison):
    mana = 280
    allow_ally_fire = True
    continuous = True
    times = 5
    damage = -50

    symbols = ["ap"]

    description = "continuous heal"

def get_spells_help():
    out = ""
    for cls in Spell.__subclasses__():
        out += "%s - %s\n" % (cls.__name__, cls.description)
    return out
