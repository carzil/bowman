from math import sqrt
from pickle import dumps
import socket
from game.server.log import game_log, net_log
from game.server.exceptions import Restart, Exit
from game.server.weapon import Spear, Axe, Bow

class Bowman():
    health = 250
    axe_damage_mod = 0
    bow_damage_mod = 0
    spear_damage_mod = 0
    axe_distance_mod = 0
    bow_distance_mod = 0
    spear_distance_mod = 0
    max_steps = 5

    def __init__(self, x, y, n, world):
        self.x = x
        self.y = y
        self.n = n
        self.world = world
        self.miss_chance = [True]
        self.set_position(self.x, self.y)
        self.bow = Bow(self.bow_damage_mod)
        self.axe = Axe(self.axe_damage_mod)
        self.spear = Spear(self.spear_damage_mod)

    def _set(self):
        return self.world.set_player(self.x, self.y, self)

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
        if is_miss:
            self.miss()
            game_log.info("bowman %d missed", self.n)
        else:
            res = opponent.damage(damage)
            if not res:
                game_log.info("bowman %d killed bowman %d", self.n, opponent.n)
                self.win()
                opponent.lose()
                raise Restart
            else:
                game_log.info("bowman %d caused damage (%d) to bowman %d", self.n, damage, opponent.n)

    def _update(self, string):
        first_letter = string[0]
        if first_letter == "f":
            for i in self.world.get_players():
                splited_string = string.split(" ")
                try:
                    weapon_type = splited_string[1]
                except IndexError:
                    weapon_type = "b"
                if weapon_type == "a":
                    weapon = self.axe
                elif weapon_type == "s":
                    weapon = self.spear
                else:
                    weapon = self.bow
                if i is not self:
                    self.fire(i, weapon)
                    break
        else:
            splited_string = string.split(" ")
            first_letter = string[0]
            self.handle_move(first_letter, splited_string)

    def update(self):
        string = input()
        return self._update(string)

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
            self.move_up(meters)
            self.move_left(meters)

        elif first_letter == "e":
            self.move_up(meters)
            self.move_right(meters)

        elif first_letter == "z":
            self.move_down(meters)
            self.move_left(meters)

        elif first_letter == "c":
            self.move_down(meters)
            self.move_right(meters)

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

    def get_info(self):
        out = "You have %d lives, your marker is '%d'\n" % (self.health, self.n)
        for i in self.world.get_players():
            if i is not self:
                out += "Bowman %d have %d lives\n" % (i.n, i.health)
        out += "\n"
        out += self.world.render_matrix()
        return out

    def __str__(self):
        return str(self.n)

class NetBowman(Bowman):
    def __init__(self, maxx, maxy, n, world, socket, ci):
        super(NetBowman, self).__init__(maxx, maxy, n, world)
        self.socket = socket
        self.client_info = ci

    def update(self):
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
        res = self._update(string)
        return res

    def send_info(self):
        self.socket.send(b"mx")
        self.socket.send(dumps(self.get_info()))
        self.socket.send(b"\xff")

    def lose(self):
        self.socket.send(b"lo")
        self.end_game()

    def win(self):
        self.socket.send(b"wi")
        self.end_game()

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
