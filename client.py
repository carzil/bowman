from socket import *
from pickle import loads
import sys

def setup_socket(remote_ip):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect((remote_ip, 9999))
    return sock

def is_matrix(bs):
    if bs[-1] == 255:
        return True
    return False

def main(argv):
    if len(argv) >= 2:
        sock = setup_socket(argv[1])
        unit_type = "r"
        if len(argv) == 3:
            unit_type = argv[2]
        if unit_type == "d":
            sock.send(b"d")
        elif unit_type == "t":
            sock.send(b"t")
        else:
            sock.send(b"r")
        while True:
            data = sock.recv(2)
            if data == b"go":
                string = input(">> ")[:5]
                while not string:
                    string = input(">> ")[:5]
                data = bytes(string.encode("utf-8"))
                sock.send(data)
            elif data == b"lo":
                print("You lose!")
            elif data == b"wi":
                print("You win!")
            elif data == b"mi":
                print("You have missed!")
            elif data == b"nb":
                print("You have been stopped by wall!")
            elif data == b"mx":
                d = sock.recv(1)
                while not is_matrix(d):
                    d += sock.recv(1)
                matrix = loads(d)
                print(matrix)
            elif data == b"eg":
                print("Game finished!")
                sock.close()
                break
            elif data == b"ag":
                print("Game aborted, because fatal error has been raised on the server!")
                sock.close()
                break


if __name__ == "__main__":
    main(sys.argv)
