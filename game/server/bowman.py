from math import sqrt
from pickle import dumps
import socket
from game.server.log import game_log, net_log
from game.server.exceptions import Retry, Kill
from game.server.spells import FireBall, HealthBreak, Heal
from game.server.weapon import Spear, Axe, Bow
from game.server.regen import Regen

class Bowman():
    health = 250

    regen_mod = 0

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

    klass = "s"

    def __init__(self, n, world, team=None):
        self.n = n
        self.world = world

        self.bow = Bow(self.bow_damage_mod, self.bow_distance_mod)
        self.axe = Axe(self.axe_damage_mod, self.axe_distance_mod)
        self.spear = Spear(self.spear_damage_mod, self.spear_distance_mod)

        self.fireball = FireBall()
        self.health_break = HealthBreak()
        self.heal = Heal()

        self.regen = Regen(self.regen_mod)

        self.killed = False

        self.team = team
        self.team_nums = ""

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
        This function move the player down on m cells
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

    def fire(self, opponent, weapon):
        # Distance from point A to point B in 2d euclid space is:
        #   _______________________________
        # \|(A.x - B.x) ** 2 + (A.y - B.y)
        r = round(sqrt((opponent.x - self.x) ** 2 + (opponent.y - self.y) ** 2))
        game_log.info("player %d fire player %d with %s", self.n, opponent.n, weapon.name)
        game_log.info("distance from player %d to player %d is %d", self.n, opponent.n, r)
        is_miss, damage = weapon.count_damage(self, opponent, r)
        defense = weapon.count_defense(self, opponent, r)
        if is_miss:
            self.miss()
            game_log.info("player %d missed", self.n)
        else:
            # if defense > damage, damage shouldn't be negative (heal),
            # but heal is valid negative damage
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

    def spell(self, opponent, spell):
        raise Retry

    def regenerate_mana(self):
        pass

    def prompt(self):
        return input(">> ")

    def get_spell(self, symbol):
        """
        Return selected spell or fireball
        """
        if symbol == "hb":
            return self.health_break
        elif symbol == "h":
            return self.heal
        else:
            return self.fireball

    def get_closest_player(self, splited_string, i):
        """
        Return selected player or the closest player
        """
        try:
            player = self.world.get_player(int(splited_string[i]))
        except IndexError:
            player = self.world.get_closest_player(self)
        if not player or player.n == self.n:
            player = self.world.get_closest_player(self)
        return player

    def get_weapon(self, splited_string, i):
        """
        Return selected weapon or suitable weapon
        """
        try:
            weapon_type = splited_string[i]
        except IndexError:
            weapon_type = ""
        if weapon_type == "a":
            weapon = self.axe
        elif weapon_type == "s":
            weapon = self.spear
        elif weapon_type == "b":
            weapon = self.bow
        else:
            weapon = None
        return weapon

    def _update(self):
        #XXX: we have to rewrite this function
        string = self.prompt()
        first_letter = string[0]
        splited_string = string.split(" ")
        if first_letter == "f":
            player = self.get_closest_player(splited_string, 1)
            if self.team and player in self.team:
                self.ally_fire()
                raise Retry
            weapon = self.get_weapon(splited_string, 2)
            if not weapon:
                r = round(sqrt((player.x - self.x) ** 2 + (player.y - self.y) ** 2))
                if r - self.axe_distance_mod < 2:
                    weapon = self.axe
                elif r - self.spear_distance_mod < 8:
                    weapon = self.spear
                else:
                    weapon = self.bow
            self.fire(player, weapon)
            player.check_heal()
        elif first_letter in ["a", "s", "d", "w", "q", "e", "z", "c"]:
            splited_string = string.split(" ")
            first_letter = string[0]
            self.handle_move(first_letter, splited_string)
        elif first_letter == "p":
            pass
        elif first_letter == "m":
            player = self.get_closest_player(splited_string, 2)
            try:
                spell = self.get_spell(splited_string[1])
            except IndexError:
                spell = self.fireball
            if self.team and not spell.allow_ally_fire and player in self.team:
                self.ally_fire()
                raise Retry
            self.spell(player, spell)
            player.check_heal()
        else:
            raise Retry

    def update(self):
        while True:
            try:
                self._update()
            except (IndexError, ValueError, Retry):
                pass
            else:
                break

    def update_regen(self):
        self.regenerate()
        self.regenerate_mana()

    def handle_move(self, first_letter, splited_string):
        meters = int(splited_string[1])

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

class NetBowman(Bowman):
    def __init__(self, socket, ci, *args, **kwargs):
        super(NetBowman, self).__init__(*args, **kwargs)
        self.socket = socket
        self.client_info = ci

    def prompt(self):
        self.socket.send(b"go")
        try:
            string = self.socket.recv(10)
            string = str(string, "utf-8")
            if string:
                net_log.debug("client '%s:%s' sent '%s'", self.client_info[0], self.client_info[1], string)
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
            super(NetBowman, self).update()
        except socket.error:
            net_log.warning("client '%s:%d' disconnected", self.client_info[0], self.client_info[1])
            raise Kill(self)

    def send_info(self, info):
        try:
            i = dumps(info)
            self.socket.send(b"mx")
            self.socket.send(i)
            self.socket.send(b"\xff" * 20)
        except socket.error:
            pass

    def lose(self):
        try:
            self.socket.send(b"lo")
        except socket.error:
            pass

    def win(self):
        try:
            self.socket.send(b"wi")
        except socket.error:
            pass

    def near_border(self):
        try:
            self.socket.send(b"nb")
        except socket.error:
            pass

    def miss(self):
        try:
            self.socket.send(b"mi")
        except socket.error:
            pass

    def end_game(self):
        try:
            self.socket.send(b"eg")
        except socket.error:
            pass

    def abort_game(self):
        try:
            self.socket.send(b"ag")
        except socket.error:
            pass

    def ally_fire(self):
        try:
            self.socket.send(b"af")
        except socket.error:
            pass

    def team_win(self):
        try:
            self.socket.send(b"tw")
        except socket.error:
            pass

    def team_lose(self):
        try:
            self.socket.send(b"tl")
        except socket.error:
            pass

    def __str__(self):
        return str(self.n)
