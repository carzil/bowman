class WorldInfo():
    def __init__(self, world, players, string, rt, bt):
        self.world = world
        self.world_s = string
        self.players = players
        self.red_team = rt
        self.blue_team = bt

class PlayerInfo():
    def __init__(self, klass, n, health, mana):
        self.klass = klass
        self.n = n
        self.health = health
        self.mana = mana

class EntityInfo():
    def __init__(self, s, n):
        self.symbol = s
        self.name = n

class TeamInfo():
    def __init__(self, players):
        self.players = players