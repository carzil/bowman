from socket import socket
from game.server.bowman import NetBowman
from game.server.exceptions import Restart
from game.server.log import net_log, game_log
from game.server.world import World

maxx, maxy = 20, 20

def restart():
    print("'q' or 'exit' to exit, something else to restart the server")
    q = input()
    if q in ["exit", "q"]:
        exit(0)
    else:
        start()

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
    return NetBowman(x, y, n, world, sock)

def start():
    global bm1, bm2, world
    game_log.info("world created")
    world = World(maxx, maxy)
    sock = setup_socket()
    bm1 = accept_client(0, 0, 1, world, sock)
    bm2 = accept_client(maxx - 1, maxy - 1, 2, world, sock)
    world.add_player(bm1)
    world.add_player(bm2)
    game_log.info("players added to world")
    game_log.info("server has started")
    game_log.info("game started")
    while True:
        world.update()
try:
    start()
except Restart:
    restart()
