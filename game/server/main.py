import os
from random import choice
from socket import socket, error
import sys
from game.server.const import maxx, maxy
from game.server.exceptions import Restart, Exit
from game.server.log import net_log, game_log
from game.server.world import World
from game.server.actors import Ranger, Tank, Damager

def setup_socket():
    sock = socket()
    net_log.info("socket has created")
    sock.bind(("", 9999))
    net_log.info("socket has binded")
    sock.listen(1)
    return sock

def accept_client(x, y, n, world, server_sock):
    sock, client = server_sock.accept()
    net_log.info("accepted client '%s:%s'" % (client[0], str(client[1])))
    sock.send(b"hello")
    unit_type = sock.recv(1)
    if unit_type == b"t":
        cls = Tank
        game_log.info("bowman %d is a tank", n)
    elif unit_type == b"d":
        cls = Damager
        game_log.info("bowman %d is a damager", n)
    else:
        cls = Ranger
        game_log.info("bowman %d is a ranger", n)
    return cls(x, y, n, world, sock, client)

def random_map(directory):
    files = os.listdir(directory)
    return open(os.path.join(directory, choice(files)))

def start():
    global bm1, bm2, world, sock
    if os.path.isdir(sys.argv[1]):
        map_file = random_map(sys.argv[1])
    else:
        map_file = open(sys.argv[1])
    world = World(maxx, maxy, map_file)
    try:
        bm1 = accept_client(0, 0, 1, world, sock)
        bm2 = accept_client(maxx - 1, maxy - 1, 2, world, sock)
    except error:
        game_log.critical("client disconnected")
        game_log.critical("restart")
        return
    world.add_player(bm1)
    world.add_player(bm2)
    game_log.info("players added to world")
    game_log.info("server has started")
    game_log.info("game started")
    while True:
        try:
            world.update()
        except (Exit, Restart):
            return
        except:
            game_log.fatal("unhandled exception have been raised")
            world.abort_game()
            sock.close()
            game_log.fatal("abort")
            raise

sock = setup_socket()

while True:
    start()
