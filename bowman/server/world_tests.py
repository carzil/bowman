# Copyright 2012 Andreev Alexander <carzil@yandex.ru>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.

import unittest
import logging
from io import StringIO
from .world import *
from .entity import Grass, Wall, Spikes, HealthPack, SpawnPoint
from .exceptions import Retry, Kill, Restart
from .player import Player
import sys

class TestWorld(unittest.TestCase):
    def setUp(self):
        map_content = StringIO("3 2\n. # &\n+ * &")
        map_content.name = "map0.txt"
        self.world = World(map_content, False)

    def testGrassEntitySet(self):
        self.assertIsInstance(self.world.get_cell(0, 0), Grass)

    def testSpikesEntitySet(self):
        self.assertIsInstance(self.world.get_cell(0, 1), Spikes)

    def testHealthPackEntitySet(self):
        self.assertIsInstance(self.world.get_cell(1, 0), HealthPack)

    def testWallEntitySet(self):
        self.assertIsInstance(self.world.get_cell(1, 1), Wall)

    def testSpawnPointsSet(self):
        self.assertEqual(self.world.max_players, 2)
    
    def testMapNameSet(self):
        self.assertEqual(self.world.map_name, "map0.txt")

    def testMapSize(self):
        self.assertEqual(self.world.x, 3)
        self.assertEqual(self.world.y, 2)

    def testBrokenMapLoad(self):
        map_content = StringIO("3 3\n. # &\n+ * &")
        map_content.name = "map0.txt"
        with self.assertRaises(Retry) as cm:
            self.world.load_map(map_content)

    def testGetCell(self):
        entity = self.world.get_cell(0, 0)
        self.assertIsInstance(entity, Grass)

        entity = self.world.get_cell(0, 1)
        self.assertIsInstance(entity, Spikes)

        entity = self.world.get_cell(0, 2)
        self.assertIsInstance(entity, Grass)

        entity = self.world.get_cell(1, 0)
        self.assertIsInstance(entity, HealthPack)

        entity = self.world.get_cell(1, 1)
        self.assertIsInstance(entity, Wall)

        entity = self.world.get_cell(1, 2)
        self.assertIsInstance(entity, Grass)

        entity = self.world.get_cell(100, 100)
        self.assertEqual(entity, None)

    def testRandomSpawnPoint(self):
        x, y, spawn_point = self.world.get_random_spawn_point()
        self.assertIsInstance(spawn_point, SpawnPoint)
        self.assertIsInstance(x, int)
        self.assertIsInstance(y, int)
        self.world.spawn_points.append((x, y, spawn_point))
    
    def testSetCell(self):
        old_entity = self.world.get_cell(0, 1) # spikes
        self.world.set_cell(0, 1, Grass())
        new_entity = self.world.get_cell(0, 1)
        self.assertIsInstance(new_entity, Grass)
        self.world.set_cell(0, 1, old_entity)

    def testSetCellCopy(self):
        self.world.set_cell_copy(0, 1, Grass())
        self.world.clean_position(0, 1)
        self.assertIsInstance(self.world.get_cell(0, 1), Grass)

    def testCleanPosition(self):
        self.world.set_cell(0, 1, HealthPack())
        self.world.clean_position(0, 1)
        self.assertIsInstance(self.world.get_cell(0, 1), Spikes)

    def testAddPlayer(self):
        player1 = Player(1, self.world)
        self.world.add_player(player1)
        self.assertEqual(len(self.world.players), 1)
        self.assertIs(self.world.players[0], player1)

        player2 = Player(2, self.world)
        self.world.add_player(player2)
        self.assertEqual(len(self.world.players), 2)
        self.assertIs(self.world.players[1], player2)

    def testGameStart(self):
        player1 = Player(1, self.world)
        self.world.add_player(player1)

        player2 = Player(2, self.world)
        self.world.add_player(player2)

        self.assertIsInstance(self.world.get_cell(player1.x, player1.y), Grass)
        self.assertIsInstance(self.world.get_cell(player2.x, player2.y), Grass)

        self.world.game_start()

        self.assertGreater(self.world.players[1].n, self.world.players[0].n)
        self.assertEqual(self.world.players_num, 2)
        self.assertIsInstance(self.world.get_cell(player1.x, player1.y), Player)
        self.assertIsInstance(self.world.get_cell(player2.x, player2.y), Player)


class TestWorldWithOnePlayer(unittest.TestCase):
    def setUp(self):
        map_content = StringIO("3 2\n. # &\n+ . *")
        map_content.name = "map0.txt"
        self.world = World(map_content, False)
        self.player1 = Player(1, self.world)
        self.world.add_player(self.player1)
        self.world.game_start()

    def testGetPlayer(self):
        p1 = self.world.get_player(1)
        self.assertIs(p1, self.player1)

    def testSetPlayerOutOfMap(self):
        res = self.world.set_player(self.player1, 100, 100)
        self.assertFalse(res)

    def testSetPlayerOnSpikes(self):
        old_health = self.player1.health
        self.player1.health = 1
        with self.assertRaises(Kill) as exc:
            self.world.set_player(0, 1, self.player1)
        self.assertIs(exc.exception.player, self.player1)
        self.player1.health = old_health

    def testSetPlayerOnWall(self):
        res = self.world.set_player(1, 2, self.player1)
        self.assertFalse(res)

    def testSetOnHealthPack(self):
        self.player1.health = 1
        res = self.world.set_player(1, 0, self.player1)
        self.assertTrue(res)
        self.assertGreater(self.player1.health, 1)

    def testCheckWin(self):
        with self.assertRaises(Restart) as exc:
            self.world.check_win()

    def testKillPlayer(self):
        x, y = self.player1.x, self.player1.y
        entity = self.world.get_cell(x, y)
        self.assertIsInstance(entity, Player)

        self.world.kill_player(self.player1)
        self.assertTrue(self.player1.killed)

        entity = self.world.get_cell(x, y)
        self.assertIsInstance(entity, Grass)

    def testCheckHeal(self):
        self.player1.set_position(1, 0)
        self.player1.health = 1
        self.world.check_heal(self.player1)
        self.assertGreater(self.player1.health, 1)

    def testGetPlayers(self):
        players = self.world.get_players()
        self.assertEqual(players, [self.player1])

    def testRenderMatrix(self):
        self.assertEqual(self.world.render_matrix_for_player(self.player1), ". # 1\n+ . *\n")

    def testUpdate(self):
        sys.stdin = StringIO("f\n" * 20)
        _tmp = sys.stdout
        tmp_stdout = StringIO()
        sys.stdout = tmp_stdout
        self.world.update()
        sys.stdout = _tmp
        tmp_stdout.close()

class TestWorldWithPlayers(unittest.TestCase):
    def setUp(self):
        map_content = StringIO("3 2\n. # &\n+ . &")
        map_content.name = "map0.txt"
        self.world = World(map_content, False)
        self.player1 = Player(1, self.world)
        self.player2 = Player(2, self.world)
        self.world.add_player(self.player1)
        self.world.add_player(self.player2)
        self.world.game_start()

    def testPlayersCollision(self):
        x, y = 0, 2
        cell = self.world.get_cell(x, y)
        if cell is self.player1:
            x, y = 1, 2

        with self.assertRaises(Kill) as exc:
            self.world.set_player(x, y, self.player1)

        self.assertIs(exc.exception.player, self.player1)
