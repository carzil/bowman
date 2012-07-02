# Copyright 2012 Andreev Alexander <carzil@yandex.ru>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.

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

    def __str__(self):
        str(self.n)

class EntityInfo():
    def __init__(self, s, n):
        self.symbol = s
        self.name = n

    def __str__(self):
        return self.symbol

class TeamInfo():
    def __init__(self, team):
        self.players = team.players
