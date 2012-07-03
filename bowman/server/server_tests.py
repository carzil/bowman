# Copyright 2012 Andreev Alexander <carzil@yandex.ru>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.

import unittest
from .main import get_unit_type, number_to_str
from .actors import Ranger, Damager, Mage, Tank

class TestServer(unittest.TestCase):
    def setUp(self):
        pass

    def testNumberToString(self):
        self.assertEqual(number_to_str(1), "01")
        self.assertEqual(number_to_str(10), "10")

    def testGetUnitType(self):
        tank = get_unit_type("t", 1)
        ranger = get_unit_type("r", 1)
        damager = get_unit_type("d", 1)
        mage = get_unit_type("m", 1)
        self.assertIs(tank, Tank)
        self.assertIs(damager, Damager)
        self.assertIs(ranger, Ranger)
        self.assertIs(mage, Mage)

