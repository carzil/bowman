# Copyright 2012 Andreev Alexander <carzil@yandex.ru>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.

import unittest
import socket
import math
from .server.player import Player
from .server.exceptions import Disconnect
from .utils import distance, Connection

class TestUtils(unittest.TestCase):
    def test_distance(self):
        player1 = Player(1, None)
        player2 = Player(2, None)
        player1.x = 10
        player1.y = 10
        player2.x = 0
        player2.y = 1
        self.assertEqual(
            distance(player1, player2),
            round(math.sqrt(
                (player1.x - player2.x) ** 2 + (player1.y - player2.y) ** 2)
            )
        )

    def test_connection(self):
        socket1, socket2 = socket.socketpair()
        connection1 = Connection(socket1)
        connection2 = Connection(socket2)
        message = "test message"
        connection1.send_pack(message)
        rmessage = connection2.get_pack()
        self.assertEqual(message, rmessage)

    def test_connection_fail(self):
        socket1, socket2 = socket.socketpair()
        connection1 = Connection(socket1)
        socket2.close()
        with self.assertRaises(Disconnect) as exc:
            message = connection1.get_pack()


