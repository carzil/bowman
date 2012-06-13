from math import sqrt
import os
from random import choice
from game.server.bowman import NetBowman, Bowman
from game.server.entity import Grass, Entity, HealthPack, SpawnPoint
from game.server.exceptions import Restart, Kill
from game.server.log import game_log
from game.info import WorldInfo, PlayerInfo, EntityInfo
from game.server.team import Team

class World():
    def __init__(self, file_obj, is_team_battle):
        self.spawn_points = []
        self.load_map(file_obj)
        self.players = []
        game_log.info("world created")
        game_log.info("map is '%s'", self.map_name)
        self.itb = is_team_battle
        if is_team_battle:
            self.team_red = Team()
            self.team_blue = Team()

    def game_start(self):
        self.players.sort(key=lambda x: x.n)
        self.players_num = len(self.players)

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
        if self.itb:
            tr_num = self.team_red.get_players_num()
            tb_num = self.team_blue.get_players_num()
            if tr_num > tb_num:
                self.team_blue.add_player(bowman)
                bowman.team = self.team_blue
            else:
                self.team_red.add_player(bowman)
                bowman.team = self.team_red

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
                game_log.info("player %d was killed by player %d in a collision", player.n, entity.n)
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
            game_log.info("player %d collided with %s in (%d, %d)", player.n, entity.name, x, y)
            return False
        self.set_cell(x, y, player)
        return True

    def team_game_end(self, winners, losers):
        for i in winners.get_players():
            i.team_win()
        for i in losers.get_players():
            i.team_lose()
        self.end_game()


    def check_win(self):
        if not self.itb:
            players = self.get_players()
            if len(players) == 1:
                players[0].win()
                game_log.info("player %d is winner", players[0].n)
                self.end_game()
                raise Restart
        else:
            tr_num = self.team_red.get_alive_players_num()
            tb_num = self.team_blue.get_alive_players_num()
            if not tr_num:
                game_log.info("blue team win")
                self.team_game_end(self.team_blue, self.team_red)
                raise Restart
            elif not tb_num:
                game_log.info("red team win")
                self.team_game_end(self.team_red, self.team_blue)
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
            game_log.info("player %d is in cell (%d, %d)", i.n, i.x, i.y)

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
        for player in self.players:
            try:
                player.end_game()
            except:
                pass
        game_log.info("game ended")

    def abort_game(self):
        for player in self.players:
            try:
                player.abort_game()
            except:
                pass
        game_log.info("game aborted")

    def get_margin(self):
        if self.players_num < 10:
            return " "
        else:
            return "  "

    def render_matrix(self):
        out = ""
        for i in self.world_map:
            for j in i:
                s = str(j)
                if len(s) == 2:
                    out += str(s)
                else:
                    out += str(s) + " "

            out += "\n"
        return out

    def get_player_info(self, player):
        return PlayerInfo(
            player.klass,
            player.n,
            player.health,
            player.mana,
        )

    def get_info(self):
        p_info = []
        matrix = [[None for j in range(self.x)] for i in range(self.y)]
        for i in range(self.x):
            for j in range(self.y):
                e = self.world_map[i][j]
                if isinstance(e, Bowman):
                    obj = self.get_player_info(e)
                    p_info.append(obj)
                elif isinstance(e, Entity):
                    obj = EntityInfo(e.symbol, e.name)
                else:
                    obj = None
                matrix[i][j] = obj
        return WorldInfo(matrix, p_info, self.render_matrix())

    def send_info(self):
        info = self.get_info()
        for player in self.players:
            player.send_info(info)
