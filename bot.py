from socket import *
from pickle import loads
from argparse import ArgumentParser
from math import sqrt
import game.info

def is_matrix(bs):
    try:
        if bs[-20:] == b"\xff" * 20:
            return True
        return False
    except IndexError:
        return False
class Bot():
    def __init__(self, remote_ip, remote_port):
        self.remote_ip = remote_ip
        self.remote_port = remote_port
        self.connect()
        self.unit_type = self.choice_unit_type()
        self.main()
        self.world_info = None
    def connect(self):
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.connect((self.remote_ip, self.remote_port))
        data = self.sock.recv(5)
        if data == b"hello":
            return
        raise Exception("Oops! There is an server error")
    def choice_unit_type(self):
        return b"r"
    def lose(self):
        print("You lose!")
    def win(self):
        print("You win!")
    def miss(self):
        print("You missed!")
    def nb(self):
        print("You have been stopped by wall!")
    def get_info_header(self, info):
        players = info.players
        player = None
        for i in players:
            if i.n == self.n:
                player = i
                break
        if not player:
            out = "You have killed"
        else:
            if player.klass == "m":
                out = "You have %d lives and %d mana" % (player.health, player.mana)
            else:
                out = "You have %d lives" % (player.health,)
        out += "\n"
        for i in players:
            if i.n != self.n:
                if player.klass == "m":
                    out += "Player %d has %d lives and %d mana" % (i.n, i.health, i.mana)
                else:
                    out += "Player %d has %d lives" % (i.n, i.health)
                out += "\n"
        return out
    def receive_matrix(self):
        d = self.sock.recv(1)
        while not is_matrix(d):
            d += self.sock.recv(1)
        matrix = loads(d)
        self.world_info = matrix
        print(self.get_info_header(matrix))
        print(matrix.world_s)
    def end_game(self):
        print("Game finished!")
        self.sock.close()
    def abort_game(self):
        print("Game aborted, because fatal error has been raised on the server!")
        self.sock.close()
    def ally_fire(self):
        print("This player is your ally!")
    def team_lose(self):
        print("Your team lose!")
    def team_win(self):
        print("Your team win!")
    def get_me(self):
        player = None
        for i in self.world_info.players:
            if i.n == self.n:
                player = i
                break
        if not player:
            return None
        else:
            return player
    def sqrt_mi(self, y1, y2, x1, x2):
        if y1 >= y2 and x1 >= x2:
            return round(sqrt((y1 - y2) ** 2 + (x1 - x2) ** 2))
        elif y1 >= y2 and x2 >= x1:
            return round(sqrt((y1 - y2) ** 2 + (x2 - x1) ** 2))
        elif y2 >= y1 and x1 >= x2:
            return round(sqrt((y2 - y1) ** 2 + (x1 - x2) ** 2))
        elif y2 >= y1 and x2 >= x1:
            return round(sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2))
    def search_plus(self):
        res_x, res_y = [], []
        for i in range(len(self.world_info.world)):
            for j in range(len(self.world_info.world[i])):
                if isinstance(self.world_info.world[i][j], game.info.EntityInfo):
                    if self.world_info.world[i][j].symbol == "+":
                        res_y += [i]
                        res_x += [j]
        if res_x != [] and res_y != []:
            return res_y, res_x
        else:
            return None, None
    def search_star(self):
        res_x, res_y = [], []
        for i in range(len(self.world_info.world)):
            for j in range(len(self.world_info.world[i])):
                if isinstance(self.world_info.world[i][j], game.info.EntityInfo):
                    if self.world_info.world[i][j].symbol == "*":
                        res_y += [i]
                        res_x += [j]
        if res_x != [] and res_y != []:
            return res_y, res_x
        else:
            return None, None
    def search_min_plus(self):
        ig_y, ig_x = self.koor(self.n)
        plus_y, plus_x = self.search_plus()
        min_mi = [10000, 0, 0]
        if not plus_y and not plus_x:
            return None, None
        for i in range(0, len(plus_x)):
            y, x = plus_y[i], plus_x[i]
            r = self.sqrt_mi(ig_y, y, ig_x, x)
            if r < min_mi[0]:
                min_mi[0] = r
                min_mi[1] = y
                min_mi[2] = x
        return min_mi[1], min_mi[2]
    def get_plus(self):
        y, x = self.search_min_plus()
        ig_y, ig_x = self.koor(self.n)
        sy, sx = self.search_star()
        my, mx = self.maxxy()
        a = 0
        l = len(sy)
        if not y and not x:
            return None
        else:
            if ig_x > x and ig_y > y:
                print("1")
                a = 0
                if ig_x - x > ig_y - y:
                    res = ig_y - y
                else:
                    res = ig_x - x
                if res > 0:
                    iy, ix = ig_y - 1, ig_x - 1
                    for i in range(0, len(sy)):
                        a += 1
                        if iy == sy[i] and ix == sx[i]:
                            a -= 1
                if a == l:
                    return "q " + str(res)
            if ig_x > x and ig_y < y:
                print("2")
                a = 0
                if ig_x - x > y - ig_y:
                    res = y - ig_y
                else:
                    res = ig_x - x
                if res > 0:
                    iy, ix = ig_y + 1, ig_x - 1
                    for i in range(0, len(sy)):
                        a += 1
                        if iy == sy[i] and ix == sx[i]:
                            a -= 1
                if a == l:
                    return "z " + str(res)
            if ig_x < x and ig_y > y:
                print("3")
                a = 0
                if x - ig_x > ig_y - y:
                    res = ig_y - y
                else:
                    res = x - ig_x
                if res > 0:
                    iy, ix = ig_y - 1, ig_x + 1
                    for i in range(0, len(sy)):
                        a += 1
                        if iy == sy[i] and ix == sx[i]:
                            a -= 1
                if a == l:
                    return "e " + str(res)
            if ig_x < x and ig_y < y:
                print("4")
                a = 0
                if x - ig_x > y - ig_y:
                    res = y - ig_y
                else:
                    res = x - ig_x
                if res > 0:
                    iy, ix = ig_y + 1, ig_x + 1
                    for i in range(0, len(sy)):
                        a += 1
                        if iy == sy[i] and ix == sx[i]:
                            a -= 1
                if a == l:
                    return "c " + str(res)
            if ig_x > x:
                print("5")
                a = 0
                res = ig_x - x
                ix, iy = ig_x - 1, ig_y
                for i in range(0, len(sx)):
                    a += 1
                    if ix == sx[i] and iy == sy[i]:
                        a -= 1
                if a == l:
                    return "a " + str(res)
                else:
                    a = 0
                    if ig_y + 1 != my:
                        for i in range(0, len(sx)):
                            a += 1
                            if ig_x - 1 == sx[i] and ig_y + 1 == sy[i]:
                                a -= 1
                        if a == l:
                            return "z 1"
                    else:
                        for i in range(0, len(sx)):
                            a += 1
                            if ig_x - 1 == sx[i] and ig_y - 1 == sy[i]:
                                a -= 1
                        if a == l:
                            return "q 1"
            if ig_x < x:
                print("6")
                a = 0
                res = x - ig_x
                ix, iy = ig_x + 1, ig_y
                for i in range(0, len(sx)):
                    a += 1
                    if ix == sx[i] and iy == sy[i]:
                        a -= 1
                if a == l:
                    return "d " + str(res)
                else:
                    a = 0
                    if ig_y + 1 != my:
                        for i in range(0, len(sx)):
                            a += 1
                            if ig_x + 1 == sx[i] and ig_y + 1 == sy[i]:
                                a -= 1
                        if a == l:
                            return "c 1"
                    else:
                        for i in range(0, len(sx)):
                            a += 1
                            if ig_x + 1 == sx[i] and ig_y - 1 == sy[i]:
                                a -= 1
                        if a == l:
                            return "e 1"
            if ig_y > y:
                print("7")
                a = 0
                res = ig_y - y
                ix, iy = ig_x, ig_y - 1
                for i in range(0, len(sx)):
                    a += 1
                    if ix == sx[i] and iy == sy[i]:
                        a -= 1
                if a == l:
                    return "w " + str(res)
                else:
                    a = 0
                    if ig_x + 1 != mx:
                        for i in range(0, len(sx)):
                            a += 1
                            if ig_x + 1 == sx[i] and ig_y + 1 == sy[i]:
                                a -= 1
                        if a == l:
                            return "q 1"
                    else:
                        for i in range(0, len(sx)):
                            a += 1
                            if ig_x - 1 == sx[i] and ig_y + 1 == sy[i]:
                                a -= 1
                        if a == l:
                            return "e 1"
            if ig_y < y:
                print("8")
                a = 0
                res = y - ig_y
                ix, iy = ig_x, ig_y + 1
                for i in range(0, len(sx)):
                    a += 1
                    if ix == sx[i] and iy == sy[i]:
                        a -= 1
                if a == l:
                    return "s " + str(res)
                else:
                    a = 0
                    if ig_x + 1 != mx:
                        for i in range(0, len(sx)):
                            a += 1
                            if ig_x + 1 == sx[i] and ig_y - 1 == sy[i]:
                                a -= 1
                        if a == l:
                            return "z 1"
                    else:
                        for i in range(0, len(sx)):
                            a += 1
                            if ig_x - 1 == sx[i] and ig_y - 1 == sy[i]:
                                a -= 1
                        if a == l:
                            return "c 1"
        return None
    def team_enemy(self):
        if not self.world_info.blue_team:
            return "n"
        else:
            for i in self.world_info.blue_team.players:
                if i.n == self.n:
                    return "r"
            for i in self.world_info.red_team.players:
                if i.n == self.n:
                    return "b"
    def maxxy(self):
        i = len(self.world_info.world)
        j = len(self.world_info.world[0])
        return i, j
    def players_xy(self):
        res_y, res_x, res_n = [], [], []
        enemy = self.team_enemy()
        if enemy != "n":
            for i in range(len(self.world_info.world)):
                for j in range(len(self.world_info.world[i])):
                    if isinstance(self.world_info.world[i][j], game.info.PlayerInfo):
                        if enemy == "b":
                            for x in self.world_info.blue_team.players:
                                if self.world_info.world[i][j].n == x.n:
                                    if x.n != self.n:
                                        res_y.append(i)
                                        res_x.append(j)
                                        res_n.append(x.n)
                        elif enemy == "r":
                            for x in self.world_info.red_team.players:
                                if self.world_info.world[i][j].n == x.n:
                                    if x.n != self.n:
                                        res_y.append(i)
                                        res_x.append(j)
                                        res_n.append(x.n)
        else:
            for i in range(len(self.world_info.world)):
                for j in range(len(self.world_info.world[i])):
                    if isinstance(self.world_info.world[i][j], game.info.PlayerInfo):
                        if self.world_info.world[i][j].n != self.n:
                            res_y.append(i)
                            res_x.append(j)
            for x in self.world_info.players:
                if x.n != self.n:
                    res_n.append(x.n)
        return res_y, res_x, res_n
    def koor(self, n_igrok):
        self.n_i = n_igrok
        for i in range(0, len(self.world_info.world)):
            for j in range(len(self.world_info.world[i])):
                if isinstance(self.world_info.world[i][j], game.info.PlayerInfo):
                    if self.world_info.world[i][j].n == self.n_i:
                        return i, j
    def go(self):
        ig_y, ig_x = self.koor(self.n)
        mas_y, mas_x, n = self.players_xy()
        y = mas_y[0]
        x = mas_x[0]
        a = 0
        my, mx = self.maxxy()
        sy, sx = self.search_star()
        l = len(sy)
        print(ig_y, ig_x, "-", y, x)
        if ig_x > x and ig_y > y:
            print("1")
            a = 0
            if ig_x - x > ig_y - y:
                res = ig_y - y
            else:
                res = ig_x - x
            if res > 0:
                iy, ix = ig_y - 1, ig_x - 1
                for i in range(0, len(sy)):
                    a += 1
                    if iy == sy[i] and ix == sx[i]:
                        a -= 1
            if a == l:
                return "q " + str(res)
        if ig_x > x and ig_y < y:
            print("2")
            a = 0
            if ig_x - x > y - ig_y:
                res = y - ig_y
            else:
                res = ig_x - x
            if res > 0:
                iy, ix = ig_y + 1, ig_x - 1
                for i in range(0, len(sy)):
                    a += 1
                    if iy == sy[i] and ix == sx[i]:
                        a -= 1
            if a == l:
                return "z " + str(res)
        if ig_x < x and ig_y > y:
            print("3")
            a = 0
            if x - ig_x > ig_y - y:
                res = ig_y - y
            else:
                res = x - ig_x
            if res > 0:
                iy, ix = ig_y - 1, ig_x + 1
                for i in range(0, len(sy)):
                    a += 1
                    if iy == sy[i] and ix == sx[i]:
                        a -= 1
            if a == l:
                return "e " + str(res)
        if ig_x < x and ig_y < y:
            print("4")
            a = 0
            if x - ig_x > y - ig_y:
                res = y - ig_y
            else:
                res = x - ig_x
            if res > 0:
                iy, ix = ig_y + 1, ig_x + 1
                for i in range(0, len(sy)):
                    a += 1
                    if iy == sy[i] and ix == sx[i]:
                        a -= 1
            if a == l:
                return "c " + str(res)
        if ig_x > x:
            print("5")
            a = 0
            res = ig_x - x
            ix, iy = ig_x - 1, ig_y
            for i in range(0, len(sx)):
                a += 1
                if ix == sx[i] and iy == sy[i]:
                    a -= 1
            if a == l:
                return "a " + str(res)
            else:
                a = 0
                if ig_y + 1 != my:
                    for i in range(0, len(sx)):
                        a += 1
                        if ig_x - 1 == sx[i] and ig_y + 1 == sy[i]:
                            a -= 1
                    if a == l:
                        return "z 1"
                else:
                    for i in range(0, len(sx)):
                        a += 1
                        if ig_x - 1 == sx[i] and ig_y - 1 == sy[i]:
                            a -= 1
                    if a == l:
                        return "q 1"
        if ig_x < x:
            print("6")
            a = 0
            res = x - ig_x
            ix, iy = ig_x + 1, ig_y
            for i in range(0, len(sx)):
                a += 1
                if ix == sx[i] and iy == sy[i]:
                    a -= 1
            if a == l:
                return "d " + str(res)
            else:
                a = 0
                if ig_y + 1 != my:
                    for i in range(0, len(sx)):
                        a += 1
                        if ig_x + 1 == sx[i] and ig_y + 1 == sy[i]:
                            a -= 1
                    if a == l:
                        return "c 1"
                else:
                    for i in range(0, len(sx)):
                        a += 1
                        if ig_x + 1 == sx[i] and ig_y - 1 == sy[i]:
                            a -= 1
                    if a == l:
                        return "e 1"
        if ig_y > y:
            print("7")
            a = 0
            res = ig_y - y
            ix, iy = ig_x, ig_y - 1
            for i in range(0, len(sx)):
                a += 1
                if ix == sx[i] and iy == sy[i]:
                    a -= 1
            if a == l:
                return "w " + str(res)
            else:
                a = 0
                if ig_x + 1 != mx:
                    for i in range(0, len(sx)):
                        a += 1
                        if ig_x + 1 == sx[i] and ig_y + 1 == sy[i]:
                            a -= 1
                    if a == l:
                        return "q 1"
                else:
                    for i in range(0, len(sx)):
                        a += 1
                        if ig_x - 1 == sx[i] and ig_y + 1 == sy[i]:
                            a -= 1
                    if a == l:
                        return "e 1"
        if ig_y < y:
            print("8")
            a = 0
            res = y - ig_y
            ix, iy = ig_x, ig_y + 1
            for i in range(0, len(sx)):
                a += 1
                if ix == sx[i] and iy == sy[i]:
                    a -= 1
            if a == l:
                return "s " + str(res)
            else:
                a = 0
                if ig_x + 1 != mx:
                    for i in range(0, len(sx)):
                        a += 1
                        if ig_x + 1 == sx[i] and ig_y - 1 == sy[i]:
                            a -= 1
                    if a == l:
                        return "z 1"
                else:
                    for i in range(0, len(sx)):
                        a += 1
                        if ig_x - 1 == sx[i] and ig_y - 1 == sy[i]:
                            a -= 1
                    if a == l:
                        return "c 1"
        return "f"
    def prompt(self):
        y_u, x_u = self.koor(self.n)
        y_op_m, x_op_m, n_m = self.players_xy()
        op_op = self.world_info.players[0]
        op = n_m[0]
        y_op, x_op = y_op_m[0], x_op_m[0]
        r = self.sqrt_mi(y_u, y_op, x_u, x_op)
        u = self.get_me()
        u_health, op_health = u.health, op_op.health
        if u_health > 1000:
            if r < 15:
                return "f " + str(op)
            else:
                return self.go()
        elif u_health > op_health:
            if r < 15:
                return "f " + str(op)
            else:
                return self.go()
        elif u_health < 800:
            if op_health < 500:
                if r < 15:
                    return "f " + str(op)
                else:
                    return self.go()
            elif op_health < 800:
                if r < 15:
                    return "f " + str(op)
                else:
                    plus = self.get_plus()
                    if not plus:
                        return "f " + str(op)
                    else:
                        return plus
            else:
                plus = self.get_plus()
                if not plus:
                    if r < 15:
                        return "f " + str(op)
                    else:
                        return self.go()
                else:
                    return plus
        elif op_health > u_health:
            plus = self.get_plus()
            if not plus:
                if r < 15:
                    return "f " + str(op)
                else:
                    return self.go()
            else:
                return plus
        else:
            if r < 15:
                return "f " + str(op)
            else:
                return self.go()
    def main(self):
        self.sock.send(self.unit_type)
        n = self.sock.recv(2)
        n = int(n)
        self.n = n
        while True:
            data = self.sock.recv(2)
            if data == b"go":
                string = self.prompt()
                while not string:
                    string = self.prompt()
                data = bytes(string.encode("utf-8"))
                self.sock.send(data)
            elif data == b"lo":
                self.lose()
            elif data == b"wi":
                self.win()
            elif data == b"mi":
                self.miss()
            elif data == b"nb":
                self.nb()
            elif data == b"mx":
                self.receive_matrix()
            elif data == b"af":
                self.ally_fire()
            elif data == b"tw":
                self.team_win()
            elif data == b"tl":
                self.team_lose()
            elif data == b"eg":
                self.end_game()
                break
            elif data == b"ag":
                self.abort_game()
                break
def main():
    arg_parser = ArgumentParser(description="Bowman is a client-server console game. "
                                            "See more: https://github.com/carzil/bowman")
    arg_parser.add_argument("ip", help="server IP address")
    arg_parser.add_argument("--port", default=9999, type=int, help="server port")
    args = arg_parser.parse_args()
    Bot(args.ip, args.port)
if __name__ == "__main__":
    main()
