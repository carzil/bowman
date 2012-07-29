# Copyright 2012 Andreev Alexander <carzil@yandex.ru>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.

from socket import *
from argparse import ArgumentParser
from bowman.utils import Connection
import sys
import os
from bowman.lib import colorama


colorama.init(autoreset=True)
UNIT_TYPES_SYMBOLS = ["r", "k", "h", "w", "s", "a", "dm", "lm", "dr"]


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
        string = input("Enter unit type, which you prefer: ").strip()
        while not string or string not in UNIT_TYPES_SYMBOLS:
            string = input("Enter unit type, which you prefer: ").strip()
        return string

    def lose(self):
        print("You lose!")

    def win(self):
        print("You win!")

    def miss(self):
        print("You missed!")

    def nb(self):
        print("You have been stopped by wall!")

    def receive_matrix(self):
        self.clear_screen()
        print("Type 'help' or 'h' for help.")
        data = self.connection.get_pack()
        for i in data:
            if i.isdigit() and i != str(self.n):
                print(colorama.Fore.RED + colorama.Style.BRIGHT + i, end="")
            elif i.isdigit() and i == str(self.n):
                print(colorama.Fore.YELLOW + i, end="", sep="")
            elif i == "*":
                print(colorama.Fore.BLUE + i, end="", sep="")
            elif i == "+":
                print(colorama.Fore.GREEN + colorama.Style.BRIGHT + i, end="")
            elif i == "#":
                print(colorama.Fore.RED + i, end="", sep="")
            else:
                print(i, end="", sep="")

    def print(self):
        data = self.connection.get_pack()
        print(data)

    def end_game(self):
        print("Game finished!")
        self.sock.close()

    def abort_game(self):
        print(
            "Game aborted, because fatal error has been raised on the server!"
        )
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
            elif data == "pr":
                self.print()


def main():
    arg_parser = ArgumentParser(
        description="Bowman is a client-server console game. "
        "See more: https://github.com/carzil/bowman"
    )

    arg_parser.add_argument(
        "--host",
        help="server host",
        default="localhost"
    )

    arg_parser.add_argument(
        "--port",
        default=9999,
        type=int,
        help="server port"
    )

    args = arg_parser.parse_args()

    Client(args.host, args.port)


if __name__ == "__main__":
    main()
