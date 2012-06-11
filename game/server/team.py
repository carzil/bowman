class Team():
    def __init__(self):
        self.players = []

    def __contains__(self, item):
        return item in self.players

    def add_player(self, player):
        self.players.append(player)

    def get_players_num(self):
        return len(self.players)

    def get_alive_players_num(self):
        return len(list(
            filter(lambda x: not x.killed, self.players)
        ))

    def get_players(self):
        return self.players
