import unittest
from io import StringIO
from game.server.world import World
from game.server.bowman import Bowman
from game.server.weapon import Bow, Axe, Spear
from game.server.spells import FireBall, Razor, HealthBreak, Heal
import sys


class TestBowman(unittest.TestCase):
    def setUp(self):
        map_content = StringIO("3 3\n. . .\n. & .\n. . .")
        map_content.name = "map0.txt"
        self.world = World(map_content, False)
        self.player1 = Bowman(1, self.world)
        self.world.add_player(self.player1)
        self.world.game_start()

    def testWorldSet(self):
        self.assertIs(self.player1.world, self.world)

    def testDamage(self):
        res = self.player1.damage(100)
        self.assertTrue(res)
        self.assertGreater(self.player1.__class__.health, self.player1.health)

    def testHeal(self):
        self.player1.health = 1
        res = self.player1.damage(-100)
        self.assertTrue(res)
        self.assertGreater(self.player1.health, 1)

    def testKillDamage(self):
        res = self.player1.damage(self.player1.__class__.health + 1)
        self.assertFalse(res)

    def testHealthRegenerate(self):
        self.player1.health = 1
        self.player1.regenerate()
        self.assertGreater(self.player1.health, 1)


class TestBowmanMovements(unittest.TestCase):
    def setUp(self):
        map_content = StringIO("3 3\n. . .\n. & .\n. . .")
        map_content.name = "map0.txt"
        self.world = World(map_content, False)
        self.player1 = Bowman(1, self.world)
        self.world.add_player(self.player1)
        self.world.game_start()

    def testMoveLeft(self):
        self.player1.move_left(1)
        self.assertEqual(self.player1.x, 1)
        self.assertEqual(self.player1.y, 0)

    def testMoveRight(self):
        self.player1.move_right(1)
        self.assertEqual(self.player1.x, 1)
        self.assertEqual(self.player1.y, 2)

    def testMoveUp(self):
        self.player1.move_up(1)
        self.assertEqual(self.player1.x, 0)
        self.assertEqual(self.player1.y, 1)

    def testMoveDown(self):
        self.player1.move_down(1)
        self.assertEqual(self.player1.x, 2)
        self.assertEqual(self.player1.y, 1)

    def testMoveUpLeft(self):
        self.player1.move_up_left(1)
        self.assertEqual(self.player1.x, 0)
        self.assertEqual(self.player1.y, 0)

    def testMoveUpRight(self):
        self.player1.move_up_right(1)
        self.assertEqual(self.player1.x, 0)
        self.assertEqual(self.player1.y, 2)

    def testMoveDownLeft(self):
        self.player1.move_down_left(1)
        self.assertEqual(self.player1.x, 2)
        self.assertEqual(self.player1.y, 0)

    def testMoveDowmRight(self):
        self.player1.move_down_right(1)
        self.assertEqual(self.player1.x, 2)
        self.assertEqual(self.player1.y, 2)

    def testOutOfMap(self):
        self.player1.move_up(100)
        self.assertEqual(self.player1.x, 0)
        self.assertEqual(self.player1.y, 1)

    def testMoveLeftHandling(self):
        _tmp = sys.stdout
        sys.stdin = StringIO("a 1\n")
        sys.stdout = StringIO()
        self.player1.update()
        sys.stdout = _tmp
        self.assertEqual(self.player1.x, 1)
        self.assertEqual(self.player1.y, 0)

    def testMoveRightHandling(self):
        _tmp = sys.stdout
        sys.stdin = StringIO("d 1\n")
        sys.stdout = StringIO()
        self.player1.update()
        sys.stdout = _tmp
        self.assertEqual(self.player1.x, 1)
        self.assertEqual(self.player1.y, 2)

    def testMoveUpHandling(self):
        _tmp = sys.stdout
        sys.stdin = StringIO("w 1\n")
        sys.stdout = StringIO()
        self.player1.update()
        sys.stdout = _tmp
        self.assertEqual(self.player1.x, 0)
        self.assertEqual(self.player1.y, 1)

    def testMoveDownHandling(self):
        _tmp = sys.stdout
        sys.stdin = StringIO("s 1\n")
        sys.stdout = StringIO()
        self.player1.update()
        sys.stdout = _tmp
        self.assertEqual(self.player1.x, 2)
        self.assertEqual(self.player1.y, 1)

    def testMoveUpLeftHandling(self):
        _tmp = sys.stdout
        sys.stdin = StringIO("q 1\n")
        sys.stdout = StringIO()
        self.player1.update()
        sys.stdout = _tmp
        self.assertEqual(self.player1.x, 0)
        self.assertEqual(self.player1.y, 0)

    def testMoveUpRightHandling(self):
        _tmp = sys.stdout
        sys.stdin = StringIO("e 1\n")
        sys.stdout = StringIO()
        self.player1.update()
        sys.stdout = _tmp
        self.assertEqual(self.player1.x, 0)
        self.assertEqual(self.player1.y, 2)

    def testMoveDownLeftHandling(self):
        _tmp = sys.stdout
        sys.stdin = StringIO("z 1\n")
        sys.stdout = StringIO()
        self.player1.update()
        sys.stdout = _tmp
        self.assertEqual(self.player1.x, 2)
        self.assertEqual(self.player1.y, 0)

    def testMoveDownRightHandling(self):
        _tmp = sys.stdout
        sys.stdin = StringIO("c 1\n")
        sys.stdout = StringIO()
        self.player1.update()
        sys.stdout = _tmp
        self.assertEqual(self.player1.x, 2)
        self.assertEqual(self.player1.y, 2)

class TestBowmanAttack(unittest.TestCase):  
    def setUp(self):
        map_content = StringIO("10 10\n"
                               "& . . . . . . . . .\n"
                               ". . . . . . . . . .\n"
                               ". . . . . . . . . .\n"
                               ". . . . . . . . . .\n"
                               ". . . . . . . . . .\n"
                               ". . . . . . . . . .\n"
                               ". . . . . . . . . .\n"
                               ". . . . . . . . . .\n"
                               ". . . . . . . . . .\n"
                               ". . . . . . . . . &\n")
        map_content.name = "map0.txt"
        self.world = World(map_content, False)
        self.player1 = Bowman(1, self.world)
        self.world.add_player(self.player1)
        self.player2 = Bowman(2, self.world)
        self.world.add_player(self.player2)
        self.world.game_start()

    def testGetWeapon(self):
        ss = ["f", "2", "b"]
        weapon = self.player1.get_weapon(ss, 2)
        self.assertIsInstance(weapon, Bow)

        ss = ["f", "2", "a"]
        weapon = self.player1.get_weapon(ss, 2)
        self.assertIsInstance(weapon, Axe)

        ss = ["f", "2", "s"]
        weapon = self.player1.get_weapon(ss, 2)
        self.assertIsInstance(weapon, Spear)

        ss = ["f", "2"]
        weapon = self.player1.get_weapon(ss, 2)
        self.assertIsInstance(weapon, Bow)

    def testGetClosestPlayer(self):
        ss = ["f", "2"]
        player = self.player1.get_closest_player(ss, 1)
        self.assertIs(player, self.player2)

        ss = ["f"]
        player = self.player1.get_closest_player(ss, 1)
        self.assertIs(player, self.player2)

    def testGetSpell(self):
        ss = ["m"]
        spell = self.player1.get_spell(ss, 1)
        self.assertIsInstance(spell, FireBall)

        ss = ["m", "hb"]
        spell = self.player1.get_spell(ss, 1)
        self.assertIsInstance(spell, HealthBreak)

        ss = ["m", "r"]
        spell = self.player1.get_spell(ss, 1)
        self.assertIsInstance(spell, Razor)

        ss = ["m", "h"]
        spell = self.player1.get_spell(ss, 1)
        self.assertIsInstance(spell, Heal)

    def testSimpleFireHandling(self):
        _tmp = sys.stdout
        sys.stdin = StringIO("f\n")
        sys.stdout = StringIO()
        self.player1.update()
        sys.stdout = _tmp
        self.assertLess(self.player2.health, self.player2.__class__.health)

    def testAimFireHandling(self):
        _tmp = sys.stdout
        sys.stdin = StringIO("f 2\n")
        sys.stdout = StringIO()
        self.player1.update()
        sys.stdout = _tmp
        self.assertLess(self.player2.health, self.player2.__class__.health)

    def testAimFireHandling2(self):
        _tmp = sys.stdout
        sys.stdin = StringIO("f 2 b\n")
        sys.stdout = StringIO()
        self.player1.update()
        sys.stdout = _tmp
        self.assertLess(self.player2.health, self.player2.__class__.health)

    def testFireMissHandling(self):
        _tmp = sys.stdout
        sys.stdin = StringIO("f 2 a\n")
        sys.stdout = StringIO()
        self.player1.update()
        sys.stdout = _tmp
        self.assertEqual(self.player2.health, self.player2.__class__.health)
