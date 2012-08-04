# Copyright 2012 Andreev Alexander <carzil@yandex.ru>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.

from socket import socket
from argparse import ArgumentParser
from bowman.utils import Connection
import sys
import os
from bowman.lib import colorama


colorama.init(autoreset=True)
UNIT_TYPES_SYMBOLS = ["r", "k", "h", "w", "s", "a", "dm", "lm", "dr"]
CHOICE_UNIT_TYPE_PROMT = "Enter unit type, which you prefer: "
COLORED_OUTPUT = True


class Client():
    def __init__(self, remote_ip, remote_port):
        '''
        Constructor for class Client.
        It takes destination host and port and connect to it.
        '''
        self.remote_ip = remote_ip
        self.remote_port = remote_port
        self._connect()
        self.world_info = None
        self.unit_type = self.choice_unit_type()
        self.tr_nums = None
        self.tb_nums = None
        self.team = None
        self.main()

    def clear_screen(self):
        '''
        This function call os command to clear screen.
        '''
        if sys.platform == "win32":
            os.system("cls")
        else:
            os.system("clear")

    def _connect(self):
        '''
        This function connect Client class instance to remote server.
        '''
        self._sock = socket()
        self._sock.connect((self.remote_ip, self.remote_port))
        self._connection = Connection(self._sock)
        data = self._connection.get_pack()
        if data == "hello":
            return
        raise Exception("Oops! There is an server error")

    def choice_unit_type(self):
        '''
        Reads from input string 
        and if there is such unit abbreviate, returns it.
        '''
        string = input(CHOICE_UNIT_TYPE_PROMT).strip()
        while not string or string not in UNIT_TYPES_SYMBOLS:
            string = input(CHOICE_UNIT_TYPE_PROMT).strip()
        return string

    def lose(self):
        '''
        This function invokes when player lose.
        '''
        print("You lose!")

    def win(self):
        '''
        This function invokes when player win.
        '''
        print("You win!")

    def miss(self):
        '''
        This function invokes when player missed.
        '''
        print("You missed!")

    def receive_matrix(self):
        '''
        This function receive new battle field representation and colorize it
        if COLORED_OUTPUT is True.
        '''
        self.clear_screen()
        print("Type 'help' or 'h' for help.")
        data = self._connection.get_pack()
        if COLORED_OUTPUT:
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
        else:
            print(data)

    def print(self):
        '''
        Prints string received from server.
        '''
        data = self._connection.get_pack()
        print(data)

    def end_game(self):
        '''
        Notify that game was finished and close connection to server.
        '''
        print("Game finished!")
        self._sock.close()

    def abort_game(self):
        '''
        Notify that game was aborted and close connection to server.
        '''
        print(
            "Game aborted, because fatal error has been raised on the server!"
        )
        self._sock.close()

    def ally_fire(self):
        '''
        This function invokes when player is trying to fire his ally.
        '''
        print("This player is your ally!")

    def team_lose(self):
        '''
        This function invokes when player team lose.
        '''
        print("Your team lose!")

    def team_win(self):
        '''
        This function invokes when player team win.
        '''
        print("Your team win!")

    def prompt(self):
        '''
        Prompt a string from user.
        '''
        return input(">> ").strip()

    def main(self):
        '''
        Main loop of client.
        It receives two-symbol package 
        and invokes function depend on package content.
        '''
        self._connection.send_pack(self.unit_type)
        n = self._connection.get_pack()
        n = int(n)
        self.n = n
        print("Waiting for game start...")
        while True:
            data = self._connection.get_pack()
            if data == "go":
                string = self.prompt()
                while not string:
                    string = self.prompt()
                self._connection.send_pack(string)
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
