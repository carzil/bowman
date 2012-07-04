#!/usr/bin/env python
# Copyright 2012 Boris Tuzhilin
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.

from socket import *
from argparse import ArgumentParser
from math import sqrt
from bowman.utils import Connection
import re

PLAYER_RE = re.compile(r"Player (\d+) have (\d+) lives")
ME_RE = re.compile(r"You have (\d+) lives, your marker is '(\d+)'")

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
        self.connection = Connection(self.sock)
        data = self.connection.get_pack()
        if data == "hello":
            return
        raise Exception("Oops! There is an server error")

    def choice_unit_type(self):
        return "r"

    def lose(self):
        print("You lose!")

    def win(self):
        print("You win!")

    def miss(self):
        print("You missed!")

    def nb(self):
        print("You have been stopped by wall!")

    def receive_matrix(self):
        data = self.connection.get_pack()
        self.parse_matrix(data)
        print(data)

    def parse_matrix(self, data):
        data = data.splitlines()
        cnt = 0
        for i in data:
            cnt += 1
            if not i:
                break
        players = []
        m = ME_RE.match(data[0])
        players.append(list(map(int, list(reversed(m.groups())))))
        for i in data[:cnt]:
            m = PLAYER_RE.match(i)
            if m:
                players.append(list(map(int, m.groups())))
        data = data[cnt:]
        data = list(map(lambda x: x.split(), data))
        self.world = data
        self.players = players

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
        for i in self.players:
            if i[0] == self.n:
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
        for i in range(len(self.world)):
            for j in range(len(self.world[i])):
                    if self.world[i][j] == "+":
                        res_y += [i]
                        res_x += [j]
        if res_x != [] and res_y != []:
            return res_y, res_x
        else:
            return None, None
    def search_star(self):
        res_x, res_y = [], []
        for i in range(len(self.world)):
            for j in range(len(self.world[i])):
                    if self.world[i][j] == "*":
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
        # TODO: rewrite this
#        if not self.world_info.blue_team:
#            return "n"
#        else:
#            for i in self.world_info.blue_team.players:
#                if i.n == self.n:
#                    return "r"
#            for i in self.world_info.red_team.players:
#                if i.n == self.n:
#                    return "b"
        return "n"

    def maxxy(self):
        i = len(self.world)
        j = len(self.world[0])
        return i, j
    def players_xy(self):
        res_y, res_x, res_n = [], [], []
        for i in range(len(self.world)):
            for j in range(len(self.world[i])):
                    if self.world[i][j].isdigit() and self.world[i][j] != str(self.n):
                        res_y.append(i)
                        res_x.append(j)
                        res_n.append(self.world[i][j])
        return res_y, res_x, res_n
    def koor(self, n_igrok):
        self.n_i = n_igrok
        for i in range(0, len(self.world)):
            for j in range(len(self.world[i])):
                    if self.world[i][j] == str(self.n_i):
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
        op_op = self.players[0]
        op = n_m[0]
        y_op, x_op = y_op_m[0], x_op_m[0]
        r = self.sqrt_mi(y_u, y_op, x_u, x_op)
        u_n, u_health = self.get_me()
        u_health, op_health = u_health, op_op[1]
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
        self.connection.send_pack(self.unit_type)
        n = self.connection.get_pack()
        n = int(n)
        self.n = n
        print("Waiting for game start...")
        while True:
            data = self.connection.get_pack()
            if data == "go":
                string = self.prompt()
                while not string:
                    string = self.prompt()
                self.connection.send_pack(string)
            elif data == "lo":
                self.lose()
            elif data == "wi":
                self.win()
            elif data == "mi":
                self.miss()
            elif data == "nb":
                self.nb()
            elif data == "mx":
                self.receive_matrix()
            elif data == "af":
                self.ally_fire()
            elif data == "tw":
                self.team_win()
            elif data == "tl":
                self.team_lose()
            elif data == "eg":
                self.end_game()
                break
            elif data == "ag":
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
