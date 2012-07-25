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
    mana = 150

    symbols = ["f", "fb"]

    description = "150 mp, 250 dmg"
    
    def count_damage(self, player, opponent, r):
        return False, 250

class HealthBreak(Spell):
    mana = 600

    symbols = ["hb"]

    description = "600 mp, dmg 25%"

    def count_damage(self, player, opponent, r):
        return False, opponent.health // 4

class Heal(Spell):
    mana = 300
    allow_ally_fire = True

    symbols = ["h"]

    description = "300 mp, heal 400 hp"

    def count_damage(self, player, opponent, r):
        return False, -400

class Razor(Spell):
    mana = 650
    allow_ally_fire = False

    symbols = ["r", "rz"]

    description = "650 mp, 800 dmg"

    def count_damage(self, player, opponent, r):
        if r > 9:
            return True, 0
        else:
            return False, 800

class Poison(Spell):
    continuous = True
    mana = 200
    times = 10
    damage = 80
    symbols = ["p"]

    description = "200 mp, 10 times 80 dmg per move"

    def apply(self, player):
        if self.times <= 0:
            game_log.info("player %d poisoning ended", player.n)
            self.finished = True
        else:
            player.damage(self.damage)
            game_log.info("player %d poisoned by %d", player.n, self.damage)
            self.times -= 1

class AllyPoison(Poison):
    mana = 220
    allow_ally_fire = True
    continuous = True
    times = 10
    damage = -60

    symbols = ["ap"]

    description = "220 mp, 10 times heal 60 xp per move"

class Shield(Spell):
    mana = 200

    bow_defense = 5
    axe_defense = 5
    spear_defense = 5

    times = 10

    finished = False

    symbol = "s"

    def apply(self, player):
        if self.times == self.__class__.times:
            player.bow_defense += self.bow_defense
            player.axe_defense += self.axe_defense
            player.spear_defense += self.spear_defense
        if self.times <= 0:
            self.finished = True
            player.bow_defense -= self.bow_defense
            player.axe_defense -= self.axe_defense
            player.spear_defense -= self.spear_defense
        else:
            self.time -= 1






def get_spells_help():
    out = ""
    for cls in Spell.__subclasses__():
        out += "%s - %s\n" % (cls.__name__, cls.description)
    return out