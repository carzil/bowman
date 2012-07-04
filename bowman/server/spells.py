# Copyright 2012 Andreev Alexander <carzil@yandex.ru>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.

from .log import game_log

class Spell():
    mana = 0
    allow_ally_fire = False

    continues = False
    finished = False

    symbols = []

    def count_damage(self, player, opponent, r):
        pass

    def apply(self, player):
        pass

class FireBall(Spell):
    mana = 300

    symbols = ["f", "fb"]
    
    def count_damage(self, player, opponent, r):
        return False, 230

class HealthBreak(Spell):
    mana = 800

    symbols = ["hb"]

    def count_damage(self, player, opponent, r):
        return False, opponent.health // 4

class Heal(Spell):
    mana = 550
    allow_ally_fire = True

    symbols = ["h"]

    def count_damage(self, player, opponent, r):
        return False, -320

class Razor(Spell):
    mana = 950
    allow_ally_fire = False

    symbols = ["r", "rz"]

    def count_damage(self, player, opponent, r):
        if r > 14:
            return True, 0
        else:
            return False, 850

class Poison(Spell):
    continues = True
    mana = 50
    times = 3

    symbols = ["p"]

    def apply(self, player):
        if self.times <= 0:
            game_log.info("poison on player %d", player.n)
            self.finished = True
        else:
            player.damage(20)
            game_log.info("player %d poisoned by 20", player.n)
            self.times -= 1

class AllyPoison(Spell):
    mana = 100
    allow_ally_fire = True
    continues = True
    times = 5

    symbols = ["ap"]

    def apply(self, player):
        if self.times <= 0:
            game_log.info("player %d continues heal ended", player.n)
            self.finished = True
        else:
            player.damage(-50)
            game_log.info("player %d healed by 50", player.n)
            self.times -= 1



