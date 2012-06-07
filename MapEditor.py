print("чтобы создать карту введите: creat_map(имя карты(которую создаёш), ширина(по умолчанию = 20), высота(по умолчанию = 20), текстура(по умолчанию '.'))")
class creat_map():
    def __init__(self, name, sim='.', x=25, y=25):
        self.name = name
        self.x = y
        self.x = y
        self.sim = sim

    def creat(self):
        res_map = ''
        world_map =[[self.sim for x in range(0,self.x)] for y in range(0,self.y)]
        file_name = "game/server/maps/" + self.name + ".txt"
        file = open(file_name, 'w')
        write = str(x) + ' ' + str(y) + "\n"
        file.write(write)
        for i in world_map:
            for j in i:
                res_map += j + ' '
            file.write(res_map)
            file.write("\n")
            res_map = ''


# чтобы создать карту введите:
# creat_map(имя карты(которую создаёш), ширина(по умолчанию = 20), высота(по умолчанию = 20), текстура(по умолчанию '.'))
