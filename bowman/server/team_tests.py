# Copyright 2012 Andreev Alexander <carzil@yandex.ru>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.

from io import StringIO
import unittest
from .player import Player
from .world import World
from .team import Team

class TestTeam(unittest.TestCase):
    def setUp(self):
        map_content = StringIO("3 2\n& & &\n& & &")
        map_content.name = "map0.txt"
        self.world = World(map_content, False)
        self.player1 = Player(1, self.world)
        self.player2 = Player(2, self.world)
        self.player3 = Player(3, self.world)
        self.player4 = Player(4, self.world)
        self.test_team = Team()
        self.test_team2 = Team()

    def testAddPlayers(self):
        self.test_team.add_player(self.player1)
        self.test_team.add_player(self.player2)
        self.assertEqual(self.test_team.players, [self.player1, self.player2])
        self.test_team2.add_player(self.player3)
        self.test_team2.add_player(self.player4)
        self.assertEqual(self.test_team2.players, [self.player3, self.player4])

    def testGetPlayers(self):
        self.test_team.add_player(self.player1)
        self.test_team.add_player(self.player2)
        self.assertEqual(self.test_team.get_players(), [self.player1, self.player2])

    def testGetPlayersNum(self):
        self.test_team.add_player(self.player1)
        self.test_team.add_player(self.player2)
        self.assertEqual(self.test_team.get_players_num(), 2)

    def testGetAlivePlayersNum(self):
        self.player1.kill()
        self.test_team.add_player(self.player1)
        self.test_team.add_player(self.player2)
        self.assertEqual(self.test_team.get_alive_players_num(), 1)

    def testTeamContains(self):
        self.test_team.add_player(self.player1)
        self.test_team.add_player(self.player2)
        self.assertTrue(self.player1 in self.test_team)

