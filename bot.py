from socket import *
from pickle import loads
from random import choice
from math import sqrt
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
    global matrix, op_number, u_namber
    matrix = matrix.split("\n")
    op_number = matrix[1][7]
    u_namer = matrix[0][-2]
    matrix = matrix[3:]
    wmatrix = []
    for i in matrix:
       wmatrix.append(i.split())
    matrix = wmatrix
    return matrix, op_namber, u_namber

def u_matrix():
    for i in range(len(matrix)):
        for j in range(len(i)):
            if matrix[i][j] == u_namber:
                return i, j

def op_matrix():
    for i in range(len(matrix)):
        for j in range(len(i)):
            if matrix[i][j] == op_namber:
                return i, j

def do():
    y_u, x_u = u_matrix()
    y_op, x_op = op_matrix()
    r = round(sqrt((y_u - y_op) ** 2 + (x_y - x_op) ** 2))

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
