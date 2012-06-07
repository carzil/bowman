class Entity():
    collidable = False
    name = "entity"

    def __str__(self):
        return ""

    def damage(self):
        return 0

class Grass(Entity):
    name = "grass"

    def __str__(self):
        return "."

class Wall(Entity):
    collidable = True
    name = "wall"

    def __str__(self):
        return "*"
