from math import sqrt
from random import randrange
from game.server.bowman import NetBowman
from game.server.exceptions import Retry, Kill
from game.server.log import game_log
from game.server.regen import ManaRegen

class Ranger(NetBowman):
    health = 3150

    regen_mod = 13

    max_steps = 5
    max_diagonal_steps = 3

    axe_distance_mod = 0
    bow_distance_mod = 0
    spear_distance_mod = 1

    axe_defense = 4
    bow_defense = 3
    spear_defense = 4

    klass = "r"

    @property
    def bow_damage_mod(self):

        return randrange(89, 98)

    @property
    def spear_damage_mod(self):
        return randrange(143, 187)

    @property
    def axe_damage_mod(self):
        return randrange(206, 247)

class Damager(NetBowman):
    health = 2340

    regen_mod = 9

    max_steps = 6
    max_diagonal_steps = 3

    axe_distance_mod = 0
    bow_distance_mod = 2
    spear_distance_mod = 0

    axe_defense = 3
    bow_defense = 7
    spear_defense = 4

    klass = "d"

    @property
    def bow_damage_mod(self):
        return randrange(102, 133)

    @property
    def spear_damage_mod(self):
        return randrange(119, 156)

    @property
    def axe_damage_mod(self):
        return randrange(193, 203)

    def fire(self, opponent, weapon):
        damage = super(Damager, self).fire(opponent, weapon)
        life_steal = -(damage // 10) # 10%
        game_log.info("life steal for player %d is %d", self.n, abs(life_steal))
        self.damage(life_steal)
        return damage

class Tank(NetBowman):
    health = 5870

    regen_mod = 19

    max_steps = 5
    max_diagonal_steps = 3

    axe_distance_mod = 1
    bow_distance_mod = 0
    spear_distance_mod = 0

    axe_defense = 4
    bow_defense = 7
    spear_defense = 6

    klass = "t"

    @property
    def bow_damage_mod(self):
        return randrange(45, 63)

    @property
    def spear_damage_mod(self):
        return randrange(61, 63)

    @property
    def axe_damage_mod(self):
        return randrange(213, 402)

class Mage(NetBowman):

    health = 2050
    mana = 600

    regen_mod = 27

    max_steps = 5
    max_diagonal_steps = 3

    axe_distance_mod = 0
    bow_distance_mod = 3
    spear_distance_mod = 0

    axe_defense = 13
    bow_defense = 17
    spear_defense = 15

    klass = "m"

    def __init__(self, *args, **kwargs):
        super(Mage, self).__init__(*args, **kwargs)
        self.mana_regen = ManaRegen()

    @property
    def bow_damage_mod(self):
        return randrange(0, 100)

    @property
    def spear_damage_mod(self):
        return randrange(0, 140)

    @property
    def axe_damage_mod(self):
        return randrange(0, 320)

    def spell(self, opponent, spell):
        game_log.info("player %d make a spell", self.n)
        r = round(sqrt((opponent.x - self.x) ** 2 + (opponent.y - self.y) ** 2))
        game_log.info("distance from player %d to player %d is %d", self.n, opponent.n, r)
        if spell.mana > self.mana:
            game_log.info("player %d have not enough mana", self.n)
            raise Retry
        is_miss, damage = spell.count_damage(self, opponent, r)
        if is_miss:
            game_log.info("player %d missed", self.n)
        else:
            res = opponent.damage(damage)
            game_log.info("player %d caused damage (%d) to player %d", self.n, damage, opponent.n)
            if not res:
                game_log.info("player %d killed player %d", self.n, opponent.n)
                opponent.lose()
                raise Kill(opponent)
        self.mana -= spell.mana

    def regenerate_mana(self):
        r = self.mana_regen.count_regen()
        if self.mana + r <= self.__class__.mana:
            self.mana += r
            game_log.info("player %d regenerated %d mana", self.n, r)

    def get_info(self):
        if not self.killed:
            out = "You have %d lives and %d mana, your marker is '%d'\n" % (self.health, self.mana, self.n)
        else:
            out = "You have killed\n"
        if self.team:
            if self.team_nums:
                out += "Your team is %s" % (self.team_nums,)
            else:
                out += "Your team is %s" % (", ".join([str(i.n) for i in self.team.get_players()]),)
            out += "\n"
        out += "\n"
        for i in self.world.get_players():
            if i is not self:
                out += "Player %d have %d lives\n" % (i.n, i.health)
        out += "\n"
        out += self.world.render_matrix()
        return out

