from socket import *
from pickle import loads
from argparse import ArgumentParser

def is_matrix(bs):
    try:
        if bs[-20:] == b"\xff" * 20:
            return True
        return False
    except IndexError:
        return False

class Client():
    def __init__(self, remote_ip, remote_port):
        self.remote_ip = remote_ip
        self.remote_port = remote_port
        self.connect()
        self.unit_type = self.choice_unit_type()
        self.main()

    def connect(self):
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.connect((self.remote_ip, self.remote_port))
        data = self.sock.recv(5)
        if data == b"hello":
            return
        raise Exception("Oops! There is an server error")


    def choice_unit_type(self):
        unit_type = b"r"
        string = input("Enter unit type, which you prefer (t, d, r, m): ")
        while not string:
            string = input("Enter unit type, which you prefer (t, d, r, m): ")
        if string == "t":
            unit_type = b"t"
        elif string == "d":
            unit_type = b"d"
        elif string == "m":
            unit_type = b"m"
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

    def prompt(self):
        return input(">> ").strip()[:10]

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

    Client(args.ip, args.port)


if __name__ == "__main__":
    main()
