class Matrix():
    biblioteca = {}
    def __init__(self, make_matrix):
        self.world_map = world_map
        self.biblioteca = biblioteca

    def print_map(self, a, b):
        self.a = input("vvedite shiriny")
        self.b = input("vvedite visoty")
        world_map =[[None for x in range(0,int(a))] for y in range(0,int(b))]
        
    def make_matrix(self):
        out = ""
        for i in self.world_map:
            otr = input()
            if otr[0:2] == '>>>':
                otrup = otr[4]
                for j in i:
                    out += otrup + ' '
            out += "\n"
            else:
                for j in i:
                    a = input()
                    out += a + " "
            print("---")
            out += "\n"
        return out

    def biblio(self):
        a = input()
        biblioteca[a] = [res]
        return biblioteca
res = Matrix(world_map).make_matrix()
biblioteca = Matrix(biblioteca).biblio()
print(res, biblioteca)
