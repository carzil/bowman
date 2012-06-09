from socket import *
from pickle import loads
from random import choice
import sys
def setup_socket(remote_ip):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect((remote_ip, 9999))
    data = sock.recv(5)
    if data == b"hello":
        return sock
    raise Exception("Oops! There is an server error")
def is_matrix(bs):
    if bs[-1] == 255:
        return True
    return False
def choice_unit_type():
    unit_type = b"r"
    return unit_type
    
def parse_matrix():
<<<<<<< Updated upstream
    global matrix
    matrix = matrix.split("\n")
    matrix = matrix[2:]
=======
    global matrix, is_matrix, op_number, u_namber, u_health, op_health
    matrix = matrix.split("\n")
    is_matrix = matrix
    op_number = matrix[1][7]
    u_namer = matrix[0][-2]
    matrix = matrix[3:]
>>>>>>> Stashed changes
    wmatrix = []
    for i in matrix:
       wmatrix.append(i.split())
    matrix = wmatrix

def u_helf():
    a = ""
    for i in is_matrix[0][9:14]:
        if i.is_digit():
            a += i
    u_health = int(a)
    
def op_helf():
    a = ""
    for i in is_matrix[1][14:19]:
        if i.is_digit():
            a += i
    u_health = int(a)
    
def do():
    return "f"
    
def main(argv):
    global matrix
    if len(argv) >= 2:
        sock = setup_socket(argv[1])
        unit_type = choice_unit_type()
        sock.send(unit_type)
        while True:
            data = sock.recv(2)
            if data == b"go":
                parse_matrix()
                string = do()
                string = bytes(string.encode("utf-8"))
                sock.send(string)
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
    matrix = ""
    main(sys.argv)
