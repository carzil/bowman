# Copyright 2012 Andreev Alexander <carzil@yandex.ru>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.

import unittest
import socket
import os
from .main import get_unit_type, number_to_str, setup_socket, accept_client,\
                  random_map, PlayerInfo
from .actors import *
from ..utils import Connection

class TestServer(unittest.TestCase):
    def setUp(self):
        pass

    def testNumberToString(self):
        self.assertEqual(number_to_str(1), "01")
        self.assertEqual(number_to_str(10), "10")

    def test_setup_socket(self):
        sock = setup_socket("localhost", 9999)
        self.assertEqual(sock.family, socket.AF_INET)
        self.assertEqual(sock.type, socket.SOCK_STREAM)
        self.assertEqual(sock.proto, socket.IPPROTO_IP)
        self.assertEqual(
            sock.getsockopt(socket.IPPROTO_IP, socket.SO_REUSEADDR), 0
        )
        self.assertIsInstance(sock, socket.socket)
        sock.close()

    def test_accept_client(self):
        sock = setup_socket("localhost", 9999)
        client_sock = socket.socket()
        client_sock.connect(("localhost", 9999))
        csock, client, connection = accept_client(sock)
        self.assertIsInstance(csock, socket.socket)
        self.assertIsInstance(connection, Connection)
        self.assertIsInstance(client, tuple)
        self.assertEqual(len(client), 2)
        self.assertIsInstance(client[0], str)
        self.assertIsInstance(client[1], int)
        sock.close()

    def test_random_map_select(self):
        MAPS_DIR = "maps"
        maps = list(
            map(lambda x: os.path.join(MAPS_DIR, x), os.listdir(MAPS_DIR))
        )
        res = random_map(MAPS_DIR)
        self.assertIn(res, maps)

    def test_get_unit_type(self):
        rogue = get_unit_type("r", 1)
        self.assertIs(rogue, Rogue)

        killer = get_unit_type("k", 1)
        self.assertIs(killer, Killer)

        hunter = get_unit_type("h", 1)
        self.assertIs(hunter, Hunter)

        warrior = get_unit_type("w", 1)
        self.assertIs(warrior, Warrior)

        sniper = get_unit_type("s", 1)
        self.assertIs(sniper, Sniper)

        assasin = get_unit_type("a", 1)
        self.assertIs(assasin, Assasin)

        dark_mage = get_unit_type("dm", 1)
        self.assertIs(dark_mage, DarkMage)

        druid = get_unit_type("dr", 1)
        self.assertIs(druid, Druid)

        light_mage = get_unit_type("lm", 1)
        self.assertIs(light_mage, LightMage)

        other = get_unit_type("asdf", 1)
        self.assertIs(other, Rogue)

    def test_PlayerInfo(self):
        client = ("localhost", 1234)
        n = 1
        connection = None
        pi = PlayerInfo(client, n, connection)
        c, n_, conn = pi
        self.assertIs(c, client)
        self.assertIs(n_, n)
        self.assertIs(conn, connection)






