#!/usr/bin/env python
# Copyright 2012 Andreev Alexander <carzil@yandex.ru>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.

from socket import *
from pickle import loads
from argparse import ArgumentParser
from bowman.utils import Connection
import os, sys

class Client():
    def __init__(self, remote_ip, remote_port):
        self.remote_ip = remote_ip
        self.remote_port = remote_port
        self.connect()
        self.world_info = None
        self.unit_type = self.choice_unit_type()
        self.tr_nums = None
        self.tb_nums = None
        self.team = None
        self.main()

    def clear_screen(self):
        if sys.platform == "win32":
            os.system("cls")
        else:
            os.system("clear")

    def connect(self):
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.connect((self.remote_ip, self.remote_port))
        self.connection = Connection(self.sock)
        data = self.connection.get_pack()
        if data == "hello":
            return
        raise Exception("Oops! There is an server error")

    def choice_unit_type(self):
        unit_type = "r"
        string = input("Enter unit type, which you prefer (t, d, r, m): ").strip()[:1]
        while not string:
            string = input("Enter unit type, which you prefer (t, d, r, m): ").strip()[:1]
        if string == "t":
            unit_type = "t"
        elif string == "d":
            unit_type = "d"
        elif string == "m":
            unit_type = "m"
        return unit_type

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
        out += ", your marker is %d\n" % (self.n,)
        for i in players:
            if i.n != self.n:
                if i.klass == "m":
                    out += "Player %d has %d lives and %d mana" % (i.n, i.health, i.mana)
                else:
                    out += "Player %d has %d lives" % (i.n, i.health)
                out += "\n"
        if self.world_info.blue_team and self.world_info.red_team:
            if not self.tr_nums:
                self.tr_nums = ", ".join([str(i.n) for i in self.world_info.red_team.players])
            if not self.tb_nums:
                self.tb_nums = ", ".join([str(i.n) for i in self.world_info.blue_team.players])
            if not self.team:
                for i in self.world_info.blue_team.players:
                    if i.n == self.n:
                        self.team = "b"
                if not self.team:
                    self.team = "r"
            if self.team == "r":
                print("Your team is %s" % (self.tr_nums,))
                print("Blue team is %s" % (self.tb_nums,))
            else:
                print("Your team is %s" % (self.tb_nums,))
                print("Red team is %s" % (self.tr_nums,))

        return out

    def receive_matrix(self):
        data = self.connection.get_pack()
        self.clear_screen()
        print(data)

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

    def prompt(self):
        return input(">> ").strip()

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

    Client(args.ip, args.port)


if __name__ == "__main__":
    main()
