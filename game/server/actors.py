from math import sqrt
from random import randrange
from game.server.bowman import NetBowman
from game.server.exceptions import Restart
from game.server.log import game_log
from game.server.regen import ManaRegen

class Ranger(NetBowman):
    health = 3150

    max_steps = 5
    max_diagonal_steps = 3

    axe_distance_mod = 0
    bow_distance_mod = 0
    spear_distance_mod = 1

    axe_defense = 4
    bow_defense = 3
    spear_defense = 4

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

    max_steps = 6
    max_diagonal_steps = 3

    axe_distance_mod = 0
    bow_distance_mod = 2
    spear_distance_mod = 0

    axe_defense = 3
    bow_defense = 7
    spear_defense = 4

    @property
    def bow_damage_mod(self):
        return randrange(102, 133)

    @property
    def spear_damage_mod(self):
        return randrange(119, 156)

    @property
    def axe_damage_mod(self):
        return randrange(193, 203)

class Tank(NetBowman):
    health = 5870

    max_steps = 5
    max_diagonal_steps = 3

    axe_distance_mod = 1
    bow_distance_mod = 0
    spear_distance_mod = 0

    axe_defense = 4
    bow_defense = 7
    spear_defense = 6

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
    health = 2810
    mana = 200

    max_steps = 5
    max_diagonal_steps = 3

    axe_distance_mod = 0
    bow_distance_mod = 3
    spear_distance_mod = 0

    axe_defense = 13
    bow_defense = 17
    spear_defense = 15

    def __init__(self, *args, **kwargs):
        super(Mage, self).__init__(*args, **kwargs)
        self.mana_regen = ManaRegen()

    @property
    def bow_damage_mod(self):
        return randrange(0, 100)

    @property
    def spear_damage_mod(self):
        return randrange(0, 140]

    @property
    def axe_damage_mod(self):
        return randrange(0, 320)

    def spell(self, opponent, spell):
        game_log.info("bowman %d make a spell", self.n)
        r = round(sqrt((opponent.x - self.x) ** 2 + (opponent.y - self.y) ** 2))
        game_log.info("distance from bowman %d to bowman %d is %d", self.n, opponent.n, r)
        is_miss, damage = spell.count_damage(self, opponent, r)
        self.mana -= spell.mana
        if is_miss:
            game_log.info("bowman %d missed", self.n)
        else:
            res = opponent.damage(damage)
            game_log.info("bowman")
            game_log.info("bowman %d caused damage (%d) to bowman %d", self.n, damage, opponent.n)
            if not res:
                game_log.info("bowman %d killed bowman %d", self.n, opponent.n)
                self.win()
                opponent.lose()
                raise Restart

    def regenerate_mana(self):
        r = self.mana_regen.count_regen()
        if self.mana + r <= self.__class__.mana:
            self.mana += r
            game_log.info("bowman %d regenerated %d mana", self.n, r)

    def get_info(self):
        out = "You have %d lives and %d mana, your marker is '%d'\n" % (self.health, self.mana, self.n)
        for i in self.world.get_players():
            if i is not self:
                out += "Bowman %d have %d lives\n" % (i.n, i.health)
        out += "\n"
        out += self.world.render_matrix()
        return out

