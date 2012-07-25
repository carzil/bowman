from socket import *
from argparse import ArgumentParser
from bowman.utils import Connection
from math import sqrt
import sys, os

UNIT_TYPES_SYMBOLS = ["r", "k", "h", "w", "s", "a", "dm", "lm", "dr"]

class bot():
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
        return 'r'

    def lose(self):
        print("You lose!")

    def win(self):
        print("You win!")

    def miss(self):
        print("You missed!")

    def nb(self):
        print("You have been stopped by wall!")
        
    def get_matrix(self):
        return self.connection.get_pack()
    
    def receive_matrix(self):
        global data
        data = self.get_matrix()
        self.clear_screen()
        world = data.splitlines()
        for i in range(len(world)):
            world[i] = world[i].split()
            for j in range(len(world[i])):
                if world[i][j][0] == '?':
                    world[i][j] = '?'
            world[i] = ' '.join(world[i])
        world = '\n'.join(world)
        print("Type 'help' or 'h' for help.")
        print(world)
        
    def parse_matrix(self):
        mas = [str(x) for x in range(0, 10)]
        world = data.splitlines()
        l = len(world)
        u_n = []
        un = world[0].split()
        u_n = un[-1][1]
        u_h = ''
        for i in range(len(un[2])):
            if un[2][i] == '/':
                break
            else:
                u_h += un[2][i]
        u_h = int(u_h)
        a, op_n, op_h = 1, [], []
        while True:
            if world[a]:
                oph = ''
                oh = world[a].split()
                op_n.append(oh[1])
                op_hel = []
                for i in range(len(oh[3])):
                    if oh[3][i] == '/':
                        break
                    else:
                        oph += oh[3][i]
                op_h.append(int(oph))
            else:
                break
            a += 1
        a += 1
        u_team = []
        if world[a]:
            b = world[a].split()
            i = 4
            c = True
            while c:
                u_team.append(b[i][0])
                if b[i][-1] != ',':
                    c = False
                i += 1
            a += 1
        a += 1
        for i in range(len(world)):
            world[i] = world[i].split()
        for i in range(len(world)):
            for j in range(len(world[i])):
                if world[i][j][0] == '?':
                    world[i][j] = world[i][j][1]
        for i in range(len(u_team)):
            b = 0
            for j in range(len(op_n)):
                if op_n[j - b] == u_team[i]:
                    q = op_n.pop(j)
                    b += 1
        return u_n, u_h, op_n, op_h, world[a:]

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
        
    def bfs(self, y, x, op, m, n, n2, mas, go):
        ma = [x for x in range(1000)]
        mop = [str(x) for x in range(10)]
        p = []
        for i in range(10):
            if mop[i] != op:
                p.append(mop[i])
        if x - 1 != -1:
            if m[y][x - 1] != '*' and m[y][x - 1] not in p:
                if m[y][x - 1] == op:
                    go[y][x - 1] = [y, x]
                    return m, mas, go, True, [y, x - 1], m[y][x] + 1
                if m[y][x - 1] not in ma:
                    m[y][x - 1] = m[y][x] + 1
                    mas.append([y, x - 1])
                    go[y][x - 1] = [y, x]
        if y - 1 != -1:
            if m[y - 1][x] != '*' and m[y - 1][x] not in p:
                if m[y - 1][x] == op:
                    go[y - 1][x] = [y, x]
                    return m, mas, go, True, [y - 1, x], m[y][x] + 1
                if m[y - 1][x] not in ma:
                    m[y - 1][x] = m[y][x] + 1
                    mas.append([y - 1, x])
                    go[y - 1][x] = [y, x]
        if x + 1 < n:
            if m[y][x + 1] != '*' and m[y][x + 1] not in p:
                if m[y][x + 1] == op:
                    go[y][x + 1] = [y, x]
                    return m, mas, go, True, [y, x + 1], m[y][x] + 1
                if m[y][x + 1] not in ma:
                    m[y][x + 1] = m[y][x] + 1
                    mas.append([y, x + 1])
                    go[y][x + 1] = [y, x]
        if y + 1 < n2:
            if m[y + 1][x] != '*' and m[y + 1][x] not in p:
                if m[y + 1][x] == op:
                    go[y + 1][x] = [y, x]
                    return m, mas, go, True, [y + 1, x], m[y][x] + 1
                if m[y + 1][x] not in ma:
                    m[y + 1][x] = m[y][x] + 1
                    mas.append([y + 1, x])
                    go[y + 1][x] = [y, x]
        if x + 1 < n and y + 1 < n2:
            if m[y + 1][x + 1] != '*' and m[y + 1][x + 1] not in p:
                if m[y + 1][x + 1] == op:
                    go[y + 1][x + 1] = [y, x]
                    return m, mas, go, True, [y + 1, x + 1], m[y][x] + 1     
                if m[y + 1][x + 1] not in ma:
                    m[y + 1][x + 1] = m[y][x] + 1
                    mas.append([y + 1, x + 1])
                    go[y + 1][x + 1] = [y, x]
        if x - 1 > -1 and y - 1 > -1:
            if m[y - 1][x - 1] != '*' and m[y - 1][x - 1] not in p:
                if m[y - 1][x - 1] == op:
                    go[y - 1][x - 1] = [y, x]
                    return m, mas, go, True, [y - 1, x - 1], m[y][x] + 1
                if m[y - 1][x - 1] not in ma:
                    m[y - 1][x - 1] = m[y][x] + 1
                    mas.append([y - 1, x - 1])
                    go[y - 1][x - 1] = [y, x]        
        if y - 1 > -1 and x + 1 < n:
            if m[y - 1][x + 1] != '*' and m[y - 1][x + 1] not in p:
                if m[y - 1][x + 1] == op:
                    go[y - 1][x + 1] = [y, x]
                    return m, mas, go, True, [y - 1, x + 1], m[y][x] + 1
                if m[y - 1][x + 1] not in ma:
                    m[y - 1][x + 1] = m[y][x] + 1
                    mas.append([y - 1, x + 1])
                    go[y - 1][x + 1] = [y, x]
        if x - 1 > -1 and y + 1 < n2:
            if m[y + 1][x - 1] != '*' and m[y + 1][x - 1] not in p:
                if m[y + 1][x - 1] == op:
                    go[y + 1][x - 1] = [y, x]
                    return m, mas, go, True, [y + 1, x - 1], m[y][x] + 1
                if m[y + 1][x - 1] not in ma:
                    m[y + 1][x - 1] = m[y][x] + 1
                    mas.append([y + 1, x - 1])
                    go[y + 1][x - 1] = [y, x]
        return m, mas, go, False, [], 0
    
    def dfs(self, matrix, u, op):
        m = matrix
        go = [[[] for x in range(len(m[y]))] for y in range(len(m))]
        n2, n = len(m), len(m[0])
        for i in range(len(m)):
            for j in range(len(m[i])):
                if m[i][j] == str(u):
                    mas = [[i, j]]
                    m[i][j] = 0
        for i in range(n * n2):
            m, mas, go, b, res, ras = self.bfs(mas[i][0], mas[i][1], op, m, n, n2, mas, go)
            if b == True:
                break
        r = [res]
        for i in range(ras):
            r.append(go[res[0]][res[1]])
            res = go[res[0]][res[1]]
        return r
    
    def parse_r(self, r):
        r.reverse()
        res = []
        for i in range(len(r) - 1):
            if r[i + 1][0] > r[i][0] and r[i + 1][1] > r[i][1]:
                res.append(['c', 1])
            elif r[i + 1][0] > r[i][0] and r[i + 1][1] == r[i][1]:
                res.append(['s', 1])
            elif r[i + 1][0] < r[i][0] and r[i + 1][1] < r[i][1]:
                res.append(['q', 1])
            elif r[i + 1][0] > r[i][0] and r[i + 1][1] < r[i][1]:
                res.append(['z', 1])
            elif r[i + 1][0] < r[i][0] and r[i + 1][1] > r[i][1]:
                res.append(['e', 1])
            elif r[i + 1][0] < r[i][0] and r[i + 1][1] == r[i][1]:
                res.append(['w', 1])
            elif r[i + 1][0] == r[i][0] and r[i + 1][1] > r[i][1]:
                res.append(['d', 1])
            elif r[i + 1][0] == r[i][0] and r[i + 1][1] < r[i][1]:
                res.append(['a', 1])
        return res
    
    def parse_res(self, r):
        res, a = [], []
        for i in range(len(r)):
            if a == []:
                a = r[i]
            elif a[0] == r[i][0]:
                a[1] += 1
            else:
                res.append(a)
                a = r[i]
        if res == []:
            res.append(a)
        return res
    
    def sqrt_mi(self, y1, y2, x1, x2):
        if y1 >= y2 and x1 >= x2:
            return round(sqrt((y1 - y2) ** 2 + (x1 - x2) ** 2))
        elif y1 >= y2 and x2 >= x1:
            return round(sqrt((y1 - y2) ** 2 + (x2 - x1) ** 2))
        elif y2 >= y1 and x1 >= x2:
            return round(sqrt((y2 - y1) ** 2 + (x1 - x2) ** 2))
        elif y2 >= y1 and x2 >= x1:
            return round(sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2))
    
    def g(self, world, u_n, op):
        r = self.dfs(world, u_n, op)
        res = self.parse_r(r)
        go = self.parse_res(res)
        return go[0][0] + ' ' + str(go[0][1])
    
    def prompt(self):
        u_n, u_h, op_n, op_h, world = self.parse_matrix()
        plus = False
        m = 1000
        ind = 0
        for i in range(len(world)):
            for j in range(len(world[i])):
                if world[i][j] == u_n:
                    uy, ux = i, j
                elif world[i][j] == '+':
                    plus = True
        for x in range(len(op_n)):   
            for i in range(len(world)):
                for j in range(len(world[i])):
                    if world[i][j] == op_n[x]:
                        rr = self.sqrt_mi(i, uy, j, ux)
                        if op_h[x] < 500 and rr < 10:
                            m = 0
                            ind = x
                            r = rr
                        elif rr < m:
                            m = rr
                            ind = x
                            r = rr
        op = op_n[ind]
        oh = op_h[ind]
        if u_h > 1000:
            if r > 9:
                return self.g(world, u_n, op)
            else:
                return 'f' + ' ' + op
        elif u_h + 100 > oh:
            if r > 9 and plus:
                return self.g(world, u_n, '+')
            elif r > 9:
                return self.g(world, u_n, op)
            else:
                return 'f' + ' ' + op
        elif oh < 1300 and oh > 950:
            if r > 9 and plus:
                return self.g(world, u_n, '+')
            elif r > 9:
                return self.g(world, u_n, op)
            else:
                return 'f' + ' ' + op            
        else:
            if plus:
                return self.g(world, u_n, '+')
            elif r > 9:
                return self.g(world, u_n, op)
            else:
                return 'f' + ' ' + op            
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
    arg_parser = ArgumentParser(description="Bowman is a client-server console game. "
    "See more: https://github.com/carzil/bowman")
    arg_parser.add_argument("ip", help="server IP address")
    arg_parser.add_argument("--port", default=9999, type=int, help="server port")

    args = arg_parser.parse_args()

    bot(args.ip, args.port)


if __name__ == "__main__":
    main()