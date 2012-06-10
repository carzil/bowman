from math import sqrt
import os
from random import choice
from game.server.bowman import NetBowman
from game.server.entity import Grass, Entity, HealthPack, SpawnPoint
from game.server.exceptions import Restart, Kill
from game.server.log import game_log

class World():
    def __init__(self, file_obj):
        self.spawn_points = []
        self.load_map(file_obj)
        self.players = []
        game_log.info("world created")
        game_log.info("map is '%s'", self.map_name)

    def game_start(self):
        for player in self.get_players():
            player._set()

    def load_map(self, file_obj):
        #XXX: handle broken maps
        x, y = map(int, file_obj.readline().split())
        self.x = x
        self.y = y
        self.world_map = [[None for j in range(x)] for i in range(y)]
        self.world_map_copy = [[None for j in range(x)] for i in range(y)]

        entities_dict = {}
        for i in Entity.__subclasses__():
            i().register(entities_dict)

        for i in range(self.y):
            string = file_obj.readline().strip().split(" ")
            cnt = 0
            for j in string:
                obj = entities_dict.get(j, Grass())
                if isinstance(obj, SpawnPoint):
                    self.spawn_points.append((i, cnt, SpawnPoint))
                    obj = Grass()
                self.world_map[i][cnt] = obj
                self.world_map_copy[i][cnt] = obj
                cnt += 1
        self.max_players = len(self.spawn_points)
        self.map_name = os.path.basename(file_obj.name)

    def get_random_spawn_point(self):
        obj = choice(self.spawn_points)
        self.spawn_points.remove(obj)
        return obj

    def add_player(self, bowman):
        self.players.append(bowman)
        spawn_point = self.get_random_spawn_point()
        bowman.x = spawn_point[0]
        bowman.y = spawn_point[1]

    def set_cell(self, x, y, value):
        self.world_map[x][y] = value

    def set_cell_copy(self, x, y, value):
        self.world_map_copy[x][y] = value

    def clean_position(self, x, y):
        self.set_cell(x, y, self.world_map_copy[x][y])

    def get_cell_copy(self, x, y):
        return self.world_map_copy[x][y]

    def check_heal(self, player):
        entity = self.get_cell_copy(player.x, player.y)
        if isinstance(entity, HealthPack):
            if entity.apply(player):
                self.set_cell_copy(player.x, player.y, Grass())

    def set_player(self, x, y, player):
        if y < 0 or y > self.y - 1 or x < 0 or x > self.x - 1:
            return False
        entity = self.get_cell(x, y)
        if isinstance(entity, NetBowman):
            if entity is not player:
                game_log.info("bowman %d was killed by bowman %d in a collision", player.n, entity.n)
                player.lose()
                raise Kill(player)
        elif entity and not entity.collidable and not entity.pickable:
            res = player.damage(entity.damage(player))
            if not res:
                player.lose()
                raise Kill(player)
        elif entity and not entity.collidable and entity.pickable:
            if entity.apply(player):
                self.set_cell_copy(x, y, Grass())
        elif entity.collidable:
            game_log.info("bowman %d collided with %s in (%d, %d)", player.n, entity.name, x, y)
            return False
        self.set_cell(x, y, player)
        return True

    def check_win(self):
        players = self.get_players()
        if len(players) == 1:
            players[0].win()
            self.end_game()
            raise Restart

    def update_player(self, player):
        if not player.killed:
            try:
                player.update()
            except Kill as instance:
                self.clean_position(instance.player.x, instance.player.y)
                instance.player.kill()
                self.check_win()

    def update(self):
        self.send_info()
        for player in self.players:
            self.update_player(player)
            self.send_info()
            self.update_player(player)
            self.send_info()

        for i in self.get_players():
            game_log.info("bowman %d is in cell (%d, %d)", i.n, i.x, i.y)

    def get_player(self, n):
        for i in self.get_players():
            if i.n == n:
                return i
        return None

    def get_closest_player(self, player):
        i = 1
        m_r = 0
        m_p = self.get_player(i)
        for i in self.get_players():
            m_p = i
            try:
                m_r = round(sqrt((m_p.x - player.x) ** 2 + (m_p.y - player.y) ** 2))
            except AttributeError: #m_p may be NoneType
                pass
            if m_r:
                break

        for i in self.get_players():
            m_r_ = round(sqrt((i.x - player.x) ** 2 + (i.y - player.y) ** 2))
            if m_r_ < m_r and m_r_:
                m_p, m_r = i, m_r_
        return m_p

    def get_players(self):
        return list(filter(lambda x: not x.killed, self.players))

    def clean_matrix(self):
        for i in range(maxx):
            for j in range(maxy):
                self.world_map[i][j] = None

    def get_cell(self, x, y):
        return self.world_map[x][y]

    def end_game(self):
        for player in self.get_players():
            try:
                player.end_game()
            except:
                pass

    def abort_game(self):
        for player in self.get_players():
            try:
                player.abort_game()
            except:
                pass

    def render_matrix(self):
        out = ""
        for i in self.world_map:
            for j in i:
                out += str(j) + " "
            out += "\n"
        return out

    def send_info(self):
        for player in self.players:
            player.send_info()