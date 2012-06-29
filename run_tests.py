#!/usr/bin/env python
# Copyright 2012 Andreev Alexander <carzil@yandex.ru>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.

import unittest
from game.server.world_tests import TestWorld, TestWorldWithOnePlayer
from game.server.bowman_tests import TestBowman, TestBowmanMovements, TestBowmanAttack
from game.server.log import net_log, game_log

# no log messages
net_log.setLevel(1000000000000)
game_log.setLevel(1000000000000)

test_cases = (TestWorld, TestWorldWithOnePlayer, TestBowmanMovements, TestBowman, TestBowmanAttack)

loader = unittest.TestLoader()
suite = unittest.TestSuite()
for test_case in test_cases:
    tests = loader.loadTestsFromTestCase(test_case)
    suite.addTests(tests)
unittest.TextTestRunner(verbosity=2).run(suite)