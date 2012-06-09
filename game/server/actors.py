from math import sqrt
from random import randrange
from game.server.bowman import NetBowman
from game.server.exceptions import Restart
from game.server.log import game_log
from game.server.regen import ManaRegen

class Ranger(NetBowman):
    health = 3800

    max_steps = 5
    max_diagonal_steps = 3

    axe_distance_mod = 0
    bow_distance_mod = 0
    spear_distance_mod = 1

    axe_defense = 7
    bow_defense = 5
    spear_defense = 8

    @property
    def bow_damage_mod(self):

        return randrange(69, 73)

    @property
    def spear_damage_mod(self):
        return randrange(149, 201)

    @property
    def axe_damage_mod(self):
        return randrange(218, 243)

class Damager(NetBowman):
    health = 2500

    max_steps = 6
    max_diagonal_steps = 3

    axe_distance_mod = 0
    bow_distance_mod = 2
    spear_distance_mod = 0

    axe_defense = 4
    bow_defense = 9
    spear_defense = 5

    @property
    def bow_damage_mod(self):
        return randrange(79, 132)

    @property
    def spear_damage_mod(self):
        return randrange(133, 134)

    @property
    def axe_damage_mod(self):
        return randrange(183, 197)

class Tank(NetBowman):
    health = 8000

    max_steps = 5
    max_diagonal_steps = 3

    axe_distance_mod = 1
    bow_distance_mod = 0
    spear_distance_mod = 0

    axe_defense = 14
    bow_defense = 8
    spear_defense = 7

    @property
    def bow_damage_mod(self):
        return randrange(34, 49)

    @property
    def spear_damage_mod(self):
        return randrange(50, 57)

    @property
    def axe_damage_mod(self):
        return randrange(276, 402)

class Mage(NetBowman):
    health = 3167

    max_steps = 5
    max_diagonal_steps = 3

    axe_distance_mod = 0
    bow_distance_mod = 3
    spear_distance_mod = 0

    axe_defense = 2
    bow_defense = 3
    spear_defense = 3

    mana = 200

    def __init__(self, *args, **kwargs):
        super(Mage, self).__init__(*args, **kwargs)
        self.mana_regen = ManaRegen()

    @property
    def bow_damage_mod(self):
        return randrange(-50, 150)

    @property
    def spear_damage_mod(self):
        return randrange(-80, 200)

    @property
    def axe_damage_mod(self):
        return randrange(-120, 300)

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

