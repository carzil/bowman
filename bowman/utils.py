# Copyright 2012 Andreev Alexander <carzil@yandex.ru>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
import struct

PACK_HEADER = ">l" # pack_size
PACK_HEADER_SIZE = struct.calcsize(PACK_HEADER)

class Connection():
    def __init__(self, socket_):
        self.socket = socket_

    def get_pack(self):
        data = self.socket.recv(PACK_HEADER_SIZE)
        pack_size = struct.unpack(PACK_HEADER, data)[0]
        data = b""
        for i in range(pack_size):
            data = b"".join((data, self.socket.recv(1)))
        try:
            data = data.decode("utf-8")
        except:
            pass
        return data

    def send_pack(self, data):
        if not isinstance(data, bytes):
            data = bytes(data, "utf-8")
        l = len(data)
        pack_size = struct.pack(PACK_HEADER, l)
        self.socket.send(pack_size)
        self.socket.send(data)

