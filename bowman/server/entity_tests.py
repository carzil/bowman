# Copyright 2012 Andreev Alexander <carzil@yandex.ru>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.

import unittest
from .entity import Entity, Grass, Wall, Spikes, HealthPack, SpawnPoint
from .player import Player

def WorldMock():
    def __getattr___(self, name):
        return lambda: None

class TestEntity(unittest.TestCase):
    def setUp(self):
        self.grass = Grass()
        self.wall = Wall()
        self.spikes = Spikes()
        self.hp = HealthPack()
        self.sp = SpawnPoint()
        self.player1 = Player(1, WorldMock())

    def testInheritance(self):
        self.assertIsInstance(self.grass, Entity)
        self.assertIsInstance(self.wall, Entity)
        self.assertIsInstance(self.spikes, Entity)
        self.assertIsInstance(self.hp, Entity)
        self.assertIsInstance(self.sp, Entity)

    def testNameSet(self):
        self.assertEqual(self.grass.name, "grass")
        self.assertEqual(self.wall.name, "wall")
        self.assertEqual(self.spikes.name, "spikes")
        self.assertEqual(self.hp.name, "heal")
        self.assertEqual(self.sp.name, "spawn point")

    def testSymbols(self):
        self.assertEqual(self.grass.symbol, ".")
        self.assertEqual(self.wall.symbol, "*")
        self.assertEqual(self.spikes.symbol, "#")
        self.assertEqual(self.hp.symbol, "+")
        self.assertEqual(self.sp.symbol, "&")

    def testPickables(self):
        self.assertTrue(self.hp.pickable)

    def testHP(self):
        self.assertEqual(self.hp.lives, HealthPack.lives)

    def testHPNotPicked(self):
        res = self.hp.apply(self.player1)
        self.assertFalse(res)

    def testHPPicked(self):
        self.player1.health -= self.hp.lives + 1
        res = self.hp.apply(self.player1)
        self.assertTrue(res)
        self.assertGreater(self.player1.health, 1)

    def testSpikes(self):
        damage = self.spikes.damage(self.player1)
        self.assertGreater(damage, 0)
