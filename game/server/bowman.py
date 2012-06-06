from math import sqrt
from pickle import dumps
from random import choice
from game.server.log import game_log
from game.server.const import maxx, maxy
from game.server.exceptions import Restart

class Bowman():
    health = 250

    def __init__(self, x, y, n, world):
        self.x = x
        self.y = y
        self.n = n
        self.world = world
        self.miss_chance = [True, False, False, False, False]
        self.set_position(self.x, self.y)

    def _set(self):
        self.world.set_cell(self.x, self.y, self)
        game_log.debug("bowman %d is in cell (%d, %d)", self.n, self.y, self.x)

    def clean_position(self, x, y):
        self.world.set_cell(x, y, None)

    def check_position(self):
        if self.x < 0 or self.x > (maxx - 1):
            return False
        elif self.y < 0 or self.y > (maxy - 1):
            return False
        xy = self.world.get_cell(self.x, self.y)
        if xy and not xy is self:
            self.lose()
            raise Restart
        return True

    def set_position(self, x, y):
        self.clean_position(self.x, self.y)
        self.x = x
        self.y = y
        self._set()

    def move_down(self, m):
        ox, oy = self.x, self.y
        self.x += m
        if not self.check_position():
            self.near_border()
            self.x -= m
            return False
        self.clean_position(ox, oy)
        self._set()
        game_log.info("bowman %d moved down", self.n)
        return True

    def move_up(self, m):
        ox, oy = self.x, self.y
        self.x -= m
        if not self.check_position():
            self.near_border()
            self.x += m
            return False
        self.clean_position(ox, oy)
        self._set()
        game_log.info("bowman %d moved up", self.n)
        return True

    def move_left(self, m):
        ox, oy = self.x, self.y
        self.y -= m
        if not self.check_position():
            self.near_border()
            self.y += m
            return False
        self.clean_position(ox, oy)
        self._set()
        game_log.info("bowman %d moved left", self.n)
        return True

    def move_right(self, m):
        ox, oy = self.x, self.y
        self.y += m
        if not self.check_position():
            self.near_border()
            self.y -= m
            return False
        self.clean_position(ox, oy)
        self._set()
        game_log.info("bowman %d moved right", self.n)
        return True

    def damage(self, damage):
        self.health -= damage
        if self.health < 0:
            return False
        return True

    def fire(self, opponent):
        game_log.debug("bowman %d is firing, miss_chance is %s", self.n, str(100 / len(self.miss_chance)))
        r = sqrt((opponent.x - self.x) ** 2 + (opponent.y - self.y) ** 2)
        miss = choice(self.miss_chance)
        if miss:
            self.miss()
            self.miss_chance.append(False)
            game_log.info("bowman %d missed", self.n)
        else:
            if len(self.miss_chance) > 1:
                self.miss_chance.pop()
            if r < 2:
                damage = Bowman.health
            elif 2 < r < 10:
                damage = round((1 / r) * 100)
            else:
                damage = round((1 / r) * 50)
            res = opponent.damage(damage)
            if not res:
                game_log.info("bowman %d killed bowman %d!", self.n, opponent.n)
                self.win()
                raise Restart
            else:
                game_log.info("bowman %d caused damage (%d) to bowman %d", self.n, damage, opponent.n)
        game_log.info("miss_chance for bowman %d is %s", self.n, str(100 / len(self.miss_chance)))

    def _update(self, string):
        first_letter = string[0]
        if first_letter == "f":
            for i in self.world.get_players():
                if i is not self:
                    self.fire(i)
        else:
            splited_string = string.split(" ")
            first_letter = string[0]
            self.handle_move(first_letter, splited_string)

    def update(self):
        string = input()
        return self._update(string)

    def handle_move(self, first_letter, splited_string):
        meters = int(splited_string[1])
        if first_letter == "s":
            return self.move_down(meters)
        elif first_letter == "w":
            return self.move_up(meters)
        elif first_letter == "a":
            return self.move_left(meters)
        elif first_letter == "d":
            return self.move_right(meters)

    def lose(self):
        pass

    def win(self):
        pass

    def near_border(self):
        pass

    def miss(self):
        pass

class NetBowman(Bowman):
    def __init__(self, maxx, maxy, n, world, socket):
        super(NetBowman, self).__init__(maxx, maxy, n, world)
        self.socket = socket

    def update(self):
        self.socket.send(b"go")
        string = self.socket.recv(5)
        string = str(string, "utf-8")
        res = self._update(string)
        self.send_matrix()
        return res

    def send_matrix(self):
        self.socket.send(b"mx")
        self.socket.send(dumps(self.world.render_to_string()))
        self.socket.send(b"\xff")

    def lose(self):
        self.socket.send(b"lo")

    def win(self):
        self.socket.send(b"wi")

    def near_border(self):
        self.socket.send(b"nb")

    def miss(self):
        self.socket.send(b"mi")