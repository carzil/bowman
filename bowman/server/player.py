# Copyright 2012 Andreev Alexander <carzil@yandex.ru>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.

from math import sqrt
import socket
from functools import wraps
from .log import game_log, net_log
from .exceptions import Retry, Kill
from .spells import Spell, FireBall, get_spells_help
from .weapon import Spear, Axe, Bow
from .regen import Regen
from ..utils import Connection

def command(*letters):
    def decorating_function(func):
        for letter in letters: commands_dict[letter] = func
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    return decorating_function

commands_dict = {}

class Player():
    health = 250

    regen_mod = 1

    axe_damage_mod = 0
    bow_damage_mod = 0
    spear_damage_mod = 0

    axe_distance_mod = 0
    bow_distance_mod = 0
    spear_distance_mod = 0

    axe_defense = 0
    bow_defense = 0
    spear_defense = 0

    max_steps = 5
    max_diagonal_steps = 5

    mana = 0

    klass = "s" # for WorldInfo

    def __init__(self, n, world, team=None):
        self.n = n
        self.world = world

        self.bow = Bow(self.bow_damage_mod, self.bow_distance_mod)
        self.axe = Axe(self.axe_damage_mod, self.axe_distance_mod)
        self.spear = Spear(self.spear_damage_mod, self.spear_distance_mod)

        self.regen = Regen(self.regen_mod)

        self.killed = False

        self.team = team
        self.team_nums = ""

        self.applied_spells = []

        self.spells_dict = {}
        for i in Spell.__subclasses__():
            for symbol in i.symbols:
                self.spells_dict[symbol] = i

    def _set(self, x, y):
        return self.world.set_player(x, y, self)

    def check_heal(self):
        self.world.check_heal(self)

    def clean_position(self, x, y):
        self.world.clean_position(x, y)

    def set_position(self, x, y):
        self.clean_position(self.x, self.y)
        self.x = x
        self.y = y
        self._set(x, y)

    def move_down(self, m):
        """
        Moves the player down on `m` cells and returns True if move preforms successful.
         . P .        . P .        . . .
         . . .   ->   . P .   ->   . P .
         . . .        . . .        . . .
        (before)     (check)      (clean)
        """
        for i in range(m):
            ox, oy = self.x, self.y
            x, y = self.x + 1, self.y
            if not self._set(x, y):
                x -= 1
                self.x = x
                self.y = y
                break
            self.clean_position(ox, oy)
            self.x = x
            self.y = y
        game_log.info("player %d moved down on %d m", self.n, m)
        return True

    def move_up(self, m):
        """
        Moves the player up on `m` cells and returns True if move preforms successful.
        """
        for i in range(m):
            ox, oy = self.x, self.y
            x, y = self.x - 1, self.y
            if not self._set(x, y):
                x += 1
                self.x = x
                self.y = y
                break
            self.clean_position(ox, oy)
            self.x = x
            self.y = y
        game_log.info("player %d moved up on %d m", self.n, m)
        return True

    def move_left(self, m):
        """
        Moves the player left on `m` cells and returns True if move preforms successful.
        """
        for i in range(m):
            ox, oy = self.x, self.y
            x, y = self.x, self.y - 1
            if not self._set(x, y):
                y += 1
                self.x = x
                self.y = y
                break
            self.clean_position(ox, oy)
            self.x = x
            self.y = y
        game_log.info("player %d moved left on %d m", self.n, m)
        return True

    def move_right(self, m):
        """
        Moves the player right on `m` cells and returns True if move preforms successful.
        """
        for i in range(m):
            ox, oy = self.x, self.y
            x, y = self.x, self.y + 1
            if not self._set(x, y):
                y -= 1
                self.x = x
                self.y = y
                break
            self.clean_position(ox, oy)
            self.x = x
            self.y = y
        game_log.info("player %d moved right on %d m", self.n, m)
        return True

    def move_up_left(self, m):
        """
        Moves the player up and left on `m` cells direction and returns True if move preforms successful.
        """
        for i in range(m):
            ox, oy = self.x, self.y
            x, y = self.x - 1, self.y - 1
            if not self._set(x, y):
                y += 1
                x += 1
                self.x = x
                self.y = y
                break
            self.clean_position(ox, oy)
            self.x = x
            self.y = y
        game_log.info("player %d moved by diagonal up left on %d m", self.n, m)
        return True

    def move_up_right(self, m):
        """
        Moves the player up and right on `m` cells direction and returns True if move preforms successful.
        """
        for i in range(m):
            ox, oy = self.x, self.y
            x, y = self.x - 1, self.y + 1
            if not self._set(x, y):
                y -= 1
                x += 1
                self.x = x
                self.y = y
                break
            self.clean_position(ox, oy)
            self.x = x
            self.y = y
        game_log.info("player %d moved by diagonal up right on %d m", self.n, m)
        return True

    def move_down_left(self, m):
        """
        Moves the player down and left on `m` cells direction and returns True if move preforms successful.
        """
        for i in range(m):
            ox, oy = self.x, self.y
            x, y = self.x + 1, self.y - 1
            if not self._set(x, y):
                y += 1
                x -= 1
                self.x = x
                self.y = y
                break
            self.clean_position(ox, oy)
            self.x = x
            self.y = y
        game_log.info("player %d moved by diagonal down left on %d m", self.n, m)
        return True

    def move_down_right(self, m):
        """
        Moves the player down and right on `m` cells direction and returns True if move preforms successful.
        """
        for i in range(m):
            ox, oy = self.x, self.y
            x, y = self.x + 1, self.y + 1
            if not self._set(x, y):
                y -= 1
                x -= 1
                self.x = x
                self.y = y
                break
            self.clean_position(ox, oy)
            self.x = x
            self.y = y
        game_log.info("player %d moved by diagonal down right on %d m", self.n, m)
        return True

    def regenerate(self):
        r = self.regen.count_regen()
        if self.health + r <= self.__class__.health:
            self.health += r
            game_log.info("player %d regenerated %d lives", self.n, r)

    def damage(self, damage):
        self.health -= damage
        if self.health < 0:
            return False
        if self.health > self.__class__.health:
            # it looks strange, but sometimes damage may be negative (for example, Damager's life steal)
            self.health = self.__class__.health
        return True

    def spell(self, opponent, spell):
        raise Retry

    def regenerate_mana(self):
        pass

    def prompt(self):
        return input(">> ")

    def get_spell(self, splited_string, i):
        """
        Return selected spell or fireball.
        """
        try:
            symbol = splited_string[i]
        except IndexError:
            symbol = "f"
        return self.spells_dict.get(symbol, FireBall)()

    def get_closest_player(self, splited_string, i):
        """
        Return selected player or the closest player.
        """
        try:
            player = self.world.get_player(int(splited_string[i]))
        except IndexError:
            player = self.world.get_closest_player(self)
        if not player:
            player = self.world.get_closest_player(self)
        return player

    def get_weapon(self, splited_string, i, player):
        """
        Return selected weapon or suitable weapon.
        """
        try:
            weapon_type = splited_string[i]
        except (IndexError, ValueError):
            weapon_type = ""
        if weapon_type == "a":
            weapon = self.axe
        elif weapon_type == "s":
            weapon = self.spear
        elif weapon_type == "b":
            weapon = self.bow
        else:
            r = round(sqrt((player.x - self.x) ** 2 + (player.y - self.y) ** 2))
            if r - self.axe_distance_mod < 2:
                weapon = self.axe
            elif r - self.spear_distance_mod < 8:
                weapon = self.spear
            else:
                weapon = self.bow
        return weapon

    def _update(self):
        string = self.prompt()
        first_letter = string[0]
        splited_string = string.split(" ")
        cmd = commands_dict.get(first_letter)
        if not cmd:
            raise Retry

        return cmd(self, first_letter, splited_string)

    def update(self):
        while True:
            try:
                self._update()
            except Retry:
                pass
            else:
                break

    def update_regen(self):
        self.regenerate()
        self.regenerate_mana()
        self.apply_spells()

    def apply_spells(self):
        to_remove = []
        for spell in self.applied_spells:
            spell.apply(self)
            if spell.finished:
                to_remove.append(spell)

        for i in to_remove:
            self.applied_spells.remove(i)

    def add_spell(self, spell):
        self.applied_spells.append(spell)

    def fire(self, opponent, weapon):
        # Distance from point A to point B in 2d euclid space is:
        #      _______________________________
        # R = \|(A.x - B.x) ** 2 + (A.y - B.y)
        r = round(sqrt((opponent.x - self.x) ** 2 + (opponent.y - self.y) ** 2))
        game_log.info("player %d fire player %d with %s", self.n, opponent.n, weapon.name)
        game_log.info("distance from player %d to player %d is %d", self.n, opponent.n, r)
        is_miss, damage = weapon.count_damage(self, opponent, r)
        defense = weapon.count_defense(self, opponent, r)
        if is_miss:
            self.miss()
            game_log.info("player %d missed", self.n)
        else:
            # if defense > damage, damage shouldn't be negative
            if defense > damage:
                damage = 0
            else:
                damage -= defense
            res = opponent.damage(damage)
            game_log.info("player %d %s defense is %d", opponent.n, weapon.name, defense)
            if damage > 0:
                game_log.info("player %d caused damage (%d) to player %d", self.n, damage, opponent.n)
            else:
                game_log.info("player %d heal player %d by %d lives", self.n, opponent.n, -damage)
            if not res:
                game_log.info("player %d killed player %d", self.n, opponent.n)
                opponent.lose()
                raise Kill(opponent)
        return damage

    @command("a", "s", "d", "w", "q", "e", "z", "c")
    def handle_move(self, first_letter, splited_string):
        try:
            meters = int(splited_string[1])
        except IndexError:
            raise Retry

        if meters > self.max_steps:
            meters = self.max_steps
        if first_letter == "s":
            self.move_down(meters)

        elif first_letter == "w":
            self.move_up(meters)

        elif first_letter == "a":
            self.move_left(meters)

        elif first_letter == "d":
            self.move_right(meters)

        elif first_letter == "q":
            if meters > self.max_diagonal_steps:
                meters = self.max_diagonal_steps
            self.move_up_left(meters)

        elif first_letter == "e":
            if meters > self.max_diagonal_steps:
                meters = self.max_diagonal_steps
            self.move_up_right(meters)

        elif first_letter == "z":
            if meters > self.max_diagonal_steps:
                meters = self.max_diagonal_steps
            self.move_down_left(meters)

        elif first_letter == "c":
            if meters > self.max_diagonal_steps:
                meters = self.max_diagonal_steps
            self.move_down_right(meters)
    
    @command("f")
    def handle_fire(self, first_letter, splited_string):
        player = self.get_closest_player(splited_string, 1)
        if self.team and player in self.team:
            self.ally_fire()
            raise Retry
        weapon = self.get_weapon(splited_string, 2, player)
        self.fire(player, weapon)
        player.check_heal()

    @command("m")
    def handle_spell(self, first_letter, splited_string):
        player = self.get_closest_player(splited_string, 2)
        spell = self.get_spell(splited_string, 1)
        if self.team and not spell.allow_ally_fire and player in self.team:
            self.ally_fire()
            raise Retry
        self.spell(player, spell)
        player.check_heal()

    @command("h", "help", "?")
    def handle_help(self, first_letter, splited_string):
        self.print(get_spells_help())
        raise Retry

    @command("p")
    def handle_pass(self, first_letter, splited_string):
        pass

    def lose(self):
        pass

    def win(self):
        pass

    def near_border(self):
        pass

    def miss(self):
        pass

    def end_game(self):
        pass

    def send_info(self, info):
        pass

    def print(self, string):
        pass

    def kill(self):
        self.killed = True

    def ally_fire(self):
        pass

    def team_win(self):
        pass

    def team_lose(self):
        pass

    def get_info(self):
        if not self.killed:
            out = "You have %d lives, your marker is '%d'\n" % (self.health, self.n)
        else:
            out = "You have killed\n"
        if self.team:
            if self.team_nums:
                out += "Your team is %s" % (self.team_nums,)
            else:
                out += "Your team is %s" % (", ".join([str(i.n) for i in self.team.get_players()]),)
            out += "\n"
        for i in self.world.get_players():
            if i is not self:
                out += "Player %d have %d lives\n" % (i.n, i.health)
        out += "\n"
        out += self.world.render_matrix()
        return out

    def __str__(self):
        return str(self.n)

class NetPlayer(Player):
    def __init__(self, socket, ci, *args, **kwargs):
        super(NetPlayer, self).__init__(*args, **kwargs)
        self.connection = Connection(socket)
        self.client_info = ci

    def prompt(self):
        self.connection.send_pack("go")
        try:
            string = self.connection.get_pack()
            if string:
                net_log.debug("client '%s:%s' (player %d) sent '%s'", self.client_info[0], self.client_info[1], self.n, string)
            else:
                net_log.warning("client '%s:%d' disconnected (player %d)",
                    self.client_info[0], self.client_info[1], self.n)
                raise Kill(self)
            return string
        except socket.error:
            net_log.warning("client '%s:%d' disconnected (player %d)",
                self.client_info[0], self.client_info[1], self.n)
            raise Kill(self)

    def update(self):
        try:
            super(NetPlayer, self).update()
        except socket.error:
            net_log.warning("client '%s:%d' disconnected", self.client_info[0], self.client_info[1])
            raise Kill(self)

    def send_info(self, info):
        try:
            self.connection.send_pack("mx")
            self.connection.send_pack(info)
        except socket.error:
            pass

    def print(self, string):
        try:
            self.connection.send_pack("pr")
            self.connection.send_pack(string)
        except socket.error:
            pass

    def lose(self):
        try:
            self.connection.send_pack("lo")
        except socket.error:
            pass

    def win(self):
        try:
            self.connection.send_pack("wi")
        except socket.error:
            pass

    def near_border(self):
        try:
            self.connection.send_pack("nb")
        except socket.error:
            pass

    def miss(self):
        try:
            self.connection.send_pack("mi")
        except socket.error:
            pass

    def end_game(self):
        try:
            self.connection.send_pack("eg")
        except socket.error:
            pass

    def abort_game(self):
        try:
            self.connection.send_pack("ag")
        except socket.error:
            pass

    def ally_fire(self):
        try:
            self.connection.send_pack("af")
        except socket.error:
            pass

    def team_win(self):
        try:
            self.connection.send_pack("tw")
        except socket.error:
            pass

    def team_lose(self):
        try:
            self.connection.send_pack("tl")
        except socket.error:
            pass

    def __str__(self):
        return str(self.n)
