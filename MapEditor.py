a,b = input("vvedite shiriny"),input("vvedite visoty")
world_map =[[None for x in range(0,int(a))] for y in range(0,int(b))]
biblioteca = {}
class Matrix():
    def __init__(self, make_matrix):
        self.world_map = world_map
        self.biblioteca = biblioteca
        
    def make_matrix(self):
        out = ""
        for i in self.world_map:
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
