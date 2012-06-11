from socket import *
from pickle import loads
from argparse import ArgumentParser

def is_matrix(bs):
    if bs[-1] == 255:
        return True
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

    def receive_matrix(self):
        d = self.sock.recv(1)
        while not is_matrix(d):
            d += self.sock.recv(1)
        matrix = loads(d)
        print(matrix)

    def end_game(self):
        print("Game finished!")
        self.sock.close()

    def abort_game(self):
        print("Game aborted, because fatal error has been raised on the server!")
        self.sock.close()

    def prompt(self):
        return input(">> ").strip()[:5]

    def main(self):
        self.sock.send(self.unit_type)
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
