class creat_map():
    def __init__(self, name, x=25, y=25, sim='.'):
        self.name = name
        self.x = x
        self.y = y
        self.sim = sim

    def creat(self):
        res_map = ''
        world_map =[[self.sim for x in range(0,self.x)] for y in range(0,self.y)]
        file_name = "maps/" + self.name + ".txt"
        file = open(file_name, 'w')
        write = str(self.x) + ' ' + str(self.y) + "\n"
        file.write(write)
        for i in world_map:
            for j in i:
                res_map += j + ' '
            file.write(res_map)
            file.write("\n")
            res_map = ''
a = input()
creat_map(a).creat()
