#!/usr/bin/env python
# Copyright 2012 Andreev Alexander <carzil@yandex.ru>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.

import unittest
from bowman.server.log import net_log, game_log

def main():
    # no log messages
    net_log.setLevel(1000000000000)
    game_log.setLevel(1000000000000)


    loader = unittest.TestLoader()
    suite = loader.discover(".", "*_tests.py")
    test_runner = unittest.TextTestRunner(verbosity=2)
    test_runner.run(suite)

if __name__ == '__main__':
    main()
