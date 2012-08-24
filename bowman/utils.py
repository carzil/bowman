# Copyright 2012 Andreev Alexander <carzil@yandex.ru>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.

import struct
from .server.exceptions import Disconnect
import math

PACK_HEADER = ">l" # pack_size
PACK_HEADER_SIZE = struct.calcsize(PACK_HEADER)

class Connection():
    def __init__(self, socket_):
        self.socket = socket_

    def get_pack(self):
        data = self.socket.recv(PACK_HEADER_SIZE)
        try:
            pack_size = struct.unpack(PACK_HEADER, data)[0]
        except struct.error:
            raise Disconnect()
        data = self.socket.recv(pack_size)
            
        data = data.decode("utf-8")
        return data

    def send_pack(self, data):
        if not isinstance(data, bytes):
            data = bytes(data, "utf-8")
        l = len(data)
        pack_size = struct.pack(PACK_HEADER, l)
        self.socket.send(pack_size)
        self.socket.send(data)

def distance(player1, player2):
    return round(
        math.sqrt(
            (player1.x - player2.x) ** 2 + (player1.y - player2.y) ** 2
        )
    )
