from game.server.const import maxx, maxy

class World():
    def __init__(self, maxx, maxy):
        self.world_map = [[None for j in range(maxy)] for i in range(maxx)]
        self.players = []

    def add_player(self, bowman):
        self.players.append(bowman)

    def set_cell(self, x, y, value):
        self.world_map[x][y] = value

    def update(self):
        for player in self.get_players():
            player.send_info()

        for player in self.get_players():
            player.update()
            for player2 in self.get_players():
                player2.send_info()

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
            player.end_game()

    def render_matrix(self):
        out = ""
        for i in self.world_map:
            for j in i:
                if j:
                    out += str(j.n) + " "
                else:
                    out += ". "
            out += "\n"
        return out
