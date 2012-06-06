from socket import socket
from game.server.exceptions import Restart, Exit
from game.server.log import net_log, game_log
from game.server.world import World
from game.server.actors import Ranger, Tank, Damager

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
    unit_type = sock.recv(1)
    cls = Ranger
    if unit_type == b"t":
        cls = Tank
    elif unit_type == b"d":
        cls = Damager
    return cls(x, y, n, world, sock, client)

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
        try:
            world.update()
        except:
            game_log.fatal("unhandled exception have been raised")
            world.abort_game()
            game_log.fatal("abort")
            raise
try:
    start()
except Restart:
    restart()
except Exit:
    exit(1)
