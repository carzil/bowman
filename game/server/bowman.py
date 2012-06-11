from math import sqrt
from pickle import dumps
import socket
from game.server.log import game_log, net_log
from game.server.exceptions import Restart, Exit, Retry, Kill
from game.server.spells import FireBall, HealthBreak
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

    def __init__(self, n, world):
        self.n = n
        self.world = world

        self.bow = Bow(self.bow_damage_mod, self.bow_distance_mod)
        self.axe = Axe(self.axe_damage_mod, self.axe_distance_mod)
        self.spear = Spear(self.spear_damage_mod, self.spear_distance_mod)

        self.fireball = FireBall()
        self.health_break = HealthBreak()

        self.regen = Regen(self.regen_mod)

        self.killed = False

    def _set(self):
        return self.world.set_player(self.x, self.y, self)

    def check_heal(self):
        self.world.check_heal(self)

    def clean_position(self, x, y):
        self.world.clean_position(x, y)

    def set_position(self, x, y):
        self.clean_position(self.x, self.y)
        self.x = x
        self.y = y
        self._set()

    def move_down(self, m):
        for i in range(m):
            ox, oy = self.x, self.y
            self.x += 1
            if not self._set():
                self.x -= 1
                break
            self.clean_position(ox, oy)
        game_log.info("bowman %d moved down on %d m", self.n, m)
        return True

    def move_up(self, m):
        for i in range(m):
            ox, oy = self.x, self.y
            self.x -= 1
            if not self._set():
                self.x += 1
                break
            self.clean_position(ox, oy)
        game_log.info("bowman %d moved up on %d m", self.n, m)
        return True

    def move_left(self, m):
        for i in range(m):
            ox, oy = self.x, self.y
            self.y -= 1
            if not self._set():
                self.y += 1
                break
            self.clean_position(ox, oy)
        game_log.info("bowman %d moved left on %d m", self.n, m)
        return True

    def move_right(self, m):
        for i in range(m):
            ox, oy = self.x, self.y
            self.y += 1
            if not self._set():
                self.y -= 1
                break
            self.clean_position(ox, oy)
        game_log.info("bowman %d moved right on %d m", self.n, m)
        return True

    def move_up_left(self, m):
        for i in range(m):
            ox, oy = self.x, self.y
            self.y -= 1
            self.x -= 1
            if not self._set():
                self.y += 1
                self.x += 1
                break
            self.clean_position(ox, oy)
        game_log.info("bowman %d moved by diagonal up left on %d m", self.n, m)
        return True

    def move_up_right(self, m):
        for i in range(m):
            ox, oy = self.x, self.y
            self.y += 1
            self.x -= 1
            if not self._set():
                self.y -= 1
                self.x += 1
                break
            self.clean_position(ox, oy)
        game_log.info("bowman %d moved by diagonal up right on %d m", self.n, m)
        return True

    def move_down_left(self, m):
        for i in range(m):
            ox, oy = self.x, self.y
            self.y -= 1
            self.x += 1
            if not self._set():
                self.y += 1
                self.x -= 1
                break
            self.clean_position(ox, oy)
        game_log.info("bowman %d moved by diagonal down left on %d m", self.n, m)
        return True

    def move_down_right(self, m):
        for i in range(m):
            ox, oy = self.x, self.y
            self.y += 1
            self.x += 1
            if not self._set():
                self.y -= 1
                self.x -= 1
                break
            self.clean_position(ox, oy)
        game_log.info("bowman %d moved by diagonal down right on %d m", self.n, m)
        return True

    def regenerate(self):
        r = self.regen.count_regen()
        if self.health + r <= self.__class__.health:
            self.health += r
            game_log.info("bowman %d regenerated %d lives", self.n, r)

    def damage(self, damage):
        self.health -= damage
        if self.health < 0:
            return False
        return True

    def fire(self, opponent, weapon):
        r = round(sqrt((opponent.x - self.x) ** 2 + (opponent.y - self.y) ** 2))
        game_log.info("bowman %d fire bowman %d with %s", self.n, opponent.n, weapon.name)
        game_log.info("distance from bowman %d to bowman %d is %d", self.n, opponent.n, r)
        is_miss, damage = weapon.count_damage(self, opponent, r)
        defense = weapon.count_defense(self, opponent, r)
        if is_miss:
            self.miss()
            game_log.info("bowman %d missed", self.n)
        else:
            damage -= defense
            res = opponent.damage(damage)
            game_log.info("bowman %d %s defense is %d", opponent.n, weapon.name, defense)
            game_log.info("bowman %d caused damage (%d) to bowman %d", self.n, damage, opponent.n)
            if not res:
                game_log.info("bowman %d killed bowman %d", self.n, opponent.n)
                opponent.lose()
                raise Kill(opponent)

    def spell(self, opponent, spell):
        raise Retry

    def regenerate_mana(self):
        pass

    def prompt(self):
        return input(">> ")

    def get_spell(self, symbol):
        if symbol == "hb":
            return self.health_break
        else:
            return self.fireball

    def _update(self):
        string = self.prompt()
        first_letter = string[0]
        splited_string = string.split(" ")
        if first_letter == "f":
            try:
                player = self.world.get_player(int(splited_string[1]))
            except IndexError:
                player = self.world.get_closest_player(self)
            if not player or player.n == self.n:
                player = self.world.get_closest_player(self)
            try:
                weapon_type = splited_string[2]
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
            try:
                player = self.world.get_player(int(splited_string[2]))
            except IndexError:
                player = self.world.get_closest_player(self)
            if not player or player.n == self.n:
                player = self.world.get_closest_player(self)
            try:
                spell = self.get_spell(splited_string[1])
            except IndexError:
                spell = self.fireball
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

    def send_info(self):
        pass

    def kill(self):
        self.killed = True

    def get_info(self):
        #XXX: this function have to be moved to class World
        if not self.killed:
            out = "You have %d lives, your marker is '%d'\n" % (self.health, self.n)
        else:
            out = "You have killed"
        for i in self.world.get_players():
            if i is not self:
                out += "Bowman %d have %d lives\n" % (i.n, i.health)
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
            string = self.socket.recv(5)
            string = str(string, "utf-8")
        except socket.error:
            net_log.fatal("client '%s:%d' disconnected", self.client_info[0], self.client_info[1])
            self.world.end_game()
            game_log.fatal("abort")
            raise Exit
        net_log.debug("client '%s:%s' sent '%s'", self.client_info[0], self.client_info[1], string)
        return string

    def send_info(self):
        self.socket.send(b"mx")
        self.socket.send(dumps(self.get_info()))
        self.socket.send(b"\xff")

    def lose(self):
        self.socket.send(b"lo")

    def win(self):
        self.socket.send(b"wi")

    def near_border(self):
        self.socket.send(b"nb")

    def miss(self):
        self.socket.send(b"mi")

    def end_game(self):
        self.socket.send(b"eg")

    def abort_game(self):
        self.socket.send(b"ag")

    def __str__(self):
        return str(self.n)
