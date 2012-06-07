class creat_map():
    def __init__(self, name, a=20, b=20, sim='.'):
        self.name = name
        self.a = a
        self.b = b
        self.sim = sim

    def creat(self):
        res_map = ''
        world_map =[[self.sim for x in range(0,self.a)] for y in range(0,self.b)]
        file_name = "game/server/maps/" + self.name + ".txt"
        file = open(file_name, 'w')
        for i in world_map:
            for j in i:
                res_map += j + ' '
            file.write(res_map)
            file.write("\n")
            res_map = ''
