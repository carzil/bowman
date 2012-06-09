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
    global matrix, up_matrix, op_number, u_number, u_health, op_health, mass
    matrix = matrix.split("\n")
    mass = ["0","1","2","3","4","5","6","7","8","9"]
    up_matrix = matrix
    op_number = matrix[1][7]
    u_number = matrix[0][-2]
    matrix = matrix[3:]
    wmatrix = []
    for i in matrix:
       wmatrix.append(i.split())
       matrix = wmatrix
    return matrix

def u_matrix():
    for i in range(0, len(matrix)):
        for j in range(0, len(matrix[i])):
            if matrix[i][j] == u_number:
                return i, j

def op_matrix():
    for i in range(0, len(matrix)):
        for j in range(0, len(matrix[i])):
            if matrix[i][j] == op_number:
                return i, j

def u_helf():
    a = ""
    for i in up_matrix[0][:-3]:
        if i in mass:
            a += i
    u_health = int(a)
    return u_health
    
def op_helf():
    a = ""
    for i in up_matrix[1][10:]:
        if i in mass:
            a += i
    op_health = int(a)
    return op_health

def search(sym='+'):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == sym:
                return True, i, j

def sqrt_mi(y1, y2, x1, x2):
    if y1 >= y2 and x1 >= x2:
        return round(sqrt((y1 - y2) ** 2 + (x1 - x2) ** 2))
    elif y1 >= y2 and x2 >= x1:
        return round(sqrt((y1 - y2) ** 2 + (x2 - x1) ** 2))
    elif y2 >= y1 and x1 >= x2:
        return round(sqrt((y2 - y1) ** 2 + (x1 - x2) ** 2))
    elif y2 >= y1 and x2 >= x1:
        return round(sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2))

def search_health():
    tf, y_plus, x_plus = search()
    if tf:
        if x_u > x_plus:
            res = x_u - x_plus
            return "a " + str(res)
        elif x_u < x_plus:
            res = x_plus - x_u
            return "d " + str(res)
        elif y_u > y_plus:
            res = y_u - y_plus
            return "w " + str(res)
        elif y_u < y_plus:
            res = y_plus - y_u
            return "s " + str(res)
    else:
        return "!"

def do():
    y_u, x_u = u_matrix()
    y_op, x_op = op_matrix()
    r = sqrt_mi(y_u, y_op, x_u, x_op)
    u_health, op_health = u_helf(), op_helf()
    if u_health > 800:
        return "f"
    elif u_health > op_health:
        if r < 16:
            return "f"
        else:
            plus = search_health()
            if plus != "!":
                return plus
            else:
                return "f"
    else:
        plus = search_health()
        if plus != "!":
            return plus
        else:
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
