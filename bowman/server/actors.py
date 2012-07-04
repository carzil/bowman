# Copyright 2012 Andreev Alexander <carzil@yandex.ru>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.

from math import sqrt
from random import randrange
from .player import Player, NetPlayer
from .exceptions import Retry, Kill
from .log import game_log
from .regen import ManaRegen

class Ranger(NetPlayer):
    health = 4000

    regen_mod = 8

    max_steps = 5
    max_diagonal_steps = 3

    axe_distance_mod = 0
    bow_distance_mod = 0
    spear_distance_mod = 1

    axe_defense = 6
    bow_defense = 4
    spear_defense = 5

    klass = "r"

    @property
    def bow_damage_mod(self):
        return randrange(87, 125)

    @property
    def spear_damage_mod(self):
        return randrange(183, 205)

    @property
    def axe_damage_mod(self):
        return randrange(254, 259)

    def fire(self, opponent, weapon):
        damage = super(Ranger, self).fire(opponent, weapon)
        splash_damage = damage // 7
        if splash_damage:
            q = self.world.get_cell(opponent.x - 1, opponent.y - 1)
            w = self.world.get_cell(opponent.x - 1, opponent.y)
            s = self.world.get_cell(opponent.x + 1, opponent.y)
            a = self.world.get_cell(opponent.x, opponent.y - 1)
            d = self.world.get_cell(opponent.x, opponent.y + 1)
            e = self.world.get_cell(opponent.x - 1, opponent.y + 1)
            z = self.world.get_cell(opponent.x + 1, opponent.y - 1)
            c = self.world.get_cell(opponent.x + 1, opponent.y + 1)
            cells = list(filter(lambda x: isinstance(x, Player), [q, w, s, a, d, e, z, c]))
            if cells:
                for i in cells:
                    i.damage(splash_damage)
                if len(cells) > 1:
                    game_log.info("player %d caused splash damage %d to players %s",
                                  self.n, splash_damage, ", ".join([str(i.n) for i in cells]))
                else:
                    game_log.info("player %d caused splash damage %d to player %d", self.n, splash_damage, cells[0].n)
        return damage

class Damager(NetPlayer):
    health = 3100

    regen_mod = 6

    max_steps = 6
    max_diagonal_steps = 3

    axe_distance_mod = 0
    bow_distance_mod = 1
    spear_distance_mod = 0

    axe_defense = 4
    bow_defense = 5
    spear_defense = 4

    klass = "d"

    @property
    def bow_damage_mod(self):
        return randrange(123, 151)

    @property
    def spear_damage_mod(self):
        return randrange(146, 173)

    @property
    def axe_damage_mod(self):
        return randrange(257, 287)

    def fire(self, opponent, weapon):
        damage = super(Damager, self).fire(opponent, weapon)
        life_steal = -(damage // 2)
        game_log.info("life steal for player %d is %d", self.n, abs(life_steal))
        self.damage(life_steal)
        return damage

class Tank(NetPlayer):
    health = 6200

    regen_mod = 12

    max_steps = 5
    max_diagonal_steps = 3

    axe_distance_mod = 1
    bow_distance_mod = 0
    spear_distance_mod = 0

    axe_defense = 4
    bow_defense = 6
    spear_defense = 5

    klass = "t"

    @property
    def bow_damage_mod(self):
        return randrange(51, 63)

    @property
    def spear_damage_mod(self):
        return randrange(64, 74)

    @property
    def axe_damage_mod(self):
        return randrange(298, 511)

class Mage(NetPlayer):

    health = 2900
    mana = 500

    regen_mod = 10

    max_steps = 5
    max_diagonal_steps = 3

    axe_distance_mod = 0
    bow_distance_mod = 0
    spear_distance_mod = 0

    axe_defense = 6
    bow_defense = 6
    spear_defense = 6

    klass = "m"

    def __init__(self, *args, **kwargs):
        super(Mage, self).__init__(*args, **kwargs)
        self.mana_regen = ManaRegen()

    @property
    def bow_damage_mod(self):
        return randrange(50, 120)

    @property
    def spear_damage_mod(self):
        return randrange(70, 150)

    @property
    def axe_damage_mod(self):
        return randrange(100, 320)

    def spell(self, opponent, spell):
        game_log.info("player %d make a spell", self.n)
        r = round(sqrt((opponent.x - self.x) ** 2 + (opponent.y - self.y) ** 2))
        game_log.info("distance from player %d to player %d is %d", self.n, opponent.n, r)
        if spell.mana > self.mana:
            game_log.info("player %d have not enough mana (need %d, found %d)", self.n, spell.mana, self.mana)
            raise Retry
        self.mana -= spell.mana
        if not spell.continuous:
            is_miss, damage = spell.count_damage(self, opponent, r)
            if is_miss:
                game_log.info("player %d missed", self.n)
            else:
                res = opponent.damage(damage)
                if damage > 0:
                    game_log.info("player %d caused damage (%d) to player %d", self.n, damage, opponent.n)
                else:
                    game_log.info("player %d heal player %d by %d lives", self.n, opponent.n, -damage)
                if not res:
                    game_log.info("player %d killed player %d", self.n, opponent.n)
                    opponent.lose()
                    raise Kill(opponent)
        else:
            opponent.add_spell(spell)

    def regenerate_mana(self):
        r = self.mana_regen.count_regen()
        if self.mana + r <= self.__class__.mana:
            self.mana += r
            game_log.info("player %d regenerated %d mana", self.n, r)

    def get_own_info(self):
        if not self.killed:
            out = "You have %d lives and %d mana, your marker is '%d'" % (self.health, self.mana, self.n)
        else:
            out = "You have killed"
        return out

    def get_info(self):
        out = "Player %d has %d lives and %d mana" % (self.n, self.mana, self.health)
        return out

