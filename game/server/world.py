from game.server.bowman import NetBowman
from game.server.const import maxx, maxy
from game.server.entity import Grass, Wall, Spikes, Entity
from game.server.exceptions import Restart
from game.server.log import game_log

class World():
    def __init__(self, file_obj):
        self.load_map(file_obj)
        self.players = []
        game_log.info("world created")
        game_log.info("map is '%s'", file_obj.name)

    def load_map(self, file_obj):
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
                self.world_map[i][cnt] = obj
                self.world_map_copy[i][cnt] = obj
                cnt += 1

    def add_player(self, bowman):
        self.players.append(bowman)

    def set_cell(self, x, y, value):
        self.world_map[x][y] = value

    def set_cell_copy(self, x, y, value):
        self.world_map_copy[x][y] = value

    def clean_position(self, x, y):
        self.set_cell(x, y, self.world_map_copy[x][y])

    def set_player(self, x, y, player):
        if y < 0 or y > self.y - 1 or x < 0 or x > self.x - 1:
            return False
        entity = self.get_cell(x, y)
        if isinstance(entity, NetBowman):
            if entity is not player:
                game_log.info("bowman %d was killed by bowman %d in a collision")
                player.lose()
                entity.win()
                raise Restart
        elif entity and not entity.collidable and not entity.pickable:
            res = player.damage(entity.damage(player))
            if not res:
                player.lose()
                for i in self.get_players():
                    if i is not player:
                        i.win()
                raise Restart
        elif entity and not entity.collidable and entity.pickable:
            if entity.apply(player):
                self.set_cell_copy(x, y, Grass())
        elif entity.collidable:
            game_log.info("bowman %d collided with %s in (%d, %d)", player.n, entity.name, x, y)
            return False
        self.set_cell(x, y, player)
        return True

    def update(self):
        for player in self.get_players():
            player.send_info()

        for player in self.get_players():
            player.update()
            for player2 in self.get_players():
                player2.send_info()

        for i in self.get_players():
            game_log.info("bowman %d is in cell (%d, %d)", i.n, i.x, i.y)

    def get_players(self):
        return self.players

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
