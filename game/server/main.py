import os
from random import choice
from socket import socket, error
from game.server.exceptions import Restart, Exit
from game.server.log import net_log, game_log
from game.server.world import World
from game.server.actors import Ranger, Tank, Damager, Mage

def setup_socket(host, port):
    sock = socket()
    net_log.info("socket has created")
    sock.bind((host, port))
    net_log.info("socket has binded")
    sock.listen(10)
    return sock

def accept_client(n, world, server_sock):
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
    elif unit_type == b"m":
        cls = Mage
        game_log.info("bowman %d is a mage", n)
    else:
        cls = Ranger
        game_log.info("bowman %d is a ranger", n)
    return cls(sock, client, n, world)

def random_map(directory):
    files = os.listdir(directory)
    return open(os.path.join(directory, choice(files)))

def accept_all_clients(n, world, server_sock):
    clients = []
    for i in range(n):
        player = accept_client(i + 1, world, server_sock)
        clients.append(player)
        world.add_player(player)

def start(map_path, players_num, sock):

    if os.path.isdir(map_path):
        is_map_dir = True
        map_file = random_map(map_path)
    else:
        is_map_dir = False
        map_file = open(map_path)

    world = World(map_file)
    if world.max_players > players_num:
        if is_map_dir:
            return
        else:
            game_log.critical("there isn't enough spawn points on map '%s'", world.map_name)

    try:
        game_log.info("waiting for %d players", players_num)
        players = accept_all_clients(players_num, world, sock)
    except error:
        game_log.critical("client disconnected")
        game_log.critical("restart")
        return

    game_log.info("server started")
    game_log.info("game started")
    game_log.info("game with %d players", players_num)
    game_log.info("map is '%s'", world.map_name)

    world.game_start()

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
