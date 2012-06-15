import os
from random import choice
from socket import socket, error
import select
from threading import Thread
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

def accept_client(server_sock):
    sock, client = server_sock.accept()
    net_log.info("accepted client '%s:%s'" % (client[0], str(client[1])))
    sock.send(b"hello")
    return sock, client

def get_unit_type(unit_type, sock, n, world, client):
    if unit_type == b"t":
        cls = Tank
        game_log.info("player %d is a tank", n)
    elif unit_type == b"d":
        cls = Damager
        game_log.info("player %d is a damager", n)
    elif unit_type == b"m":
        cls = Mage
        game_log.info("player %d is a mage", n)
    else:
        cls = Ranger
        game_log.info("player %d is a ranger", n)
    return cls(sock, client, n, world)

def random_map(directory):
    files = os.listdir(directory)
    return open(os.path.join(directory, choice(files)))

class PlayerInfo():
    def __init__(self, client, n):
        self.client = client
        self.n = n

    def __iter__(self):
        yield self.client
        yield self.n

def number_to_str(n):
    n = str(n)
    if len(n) < 2:
        return "0" + n
    return n

def accept_all_clients(n, world, server_sock):
    players = []
    track = [server_sock]
    socks_info = {}
    i = 0
    clients_missed = 0
    while True:
        if len(players) + clients_missed == n and len(players) > 0:
            break
        elif clients_missed == n:
            game_log.critical("all players disconnected")
            game_log.critical("restart")
            raise Restart
        r, w, e = select.select(track, [], [])
        for sock in r:
            if sock is server_sock:
                i += 1
                client_sock, client = accept_client(server_sock)
                socks_info[client_sock] = PlayerInfo(client, i)
                track.append(client_sock)
            else:
                client, c_n = socks_info.get(sock)
                try:
                    unit_type = sock.recv(1)
                    sock.send(bytes(number_to_str(c_n), "utf-8"))
                except error:
                    track.remove(sock)
                    del socks_info[sock]
                    net_log.warning("client '%s:%d' disconnected", client[0], client[1])
                    clients_missed += 1
                else:
                    player = get_unit_type(unit_type, sock, c_n, world, client)
                    world.add_player(player)
                    players.append(player)
    if len(players) == 1:
        game_log.critical("game with 1 player")
        game_log.critical("restart")
        world.abort_game()
        raise Restart

def updater(world, sock):
    world.game_start()

    while True:
        try:
            world.update()
        except (Exit, Restart):
            return
        except:
            game_log.fatal("unhandled exception have been raised")
            game_log.fatal("abort")
            world.abort_game()
            sock.close()
            raise

def start(map_path, players_num, sock, itb):
    if os.path.isdir(map_path):
        is_map_dir = True
        map_file = random_map(map_path)
    else:
        is_map_dir = False
        map_file = open(map_path)

    world = World(map_file, itb)
    game_log.info("%d spawn points", world.max_players)
    if world.max_players < players_num:
        if is_map_dir:
            return
        else:
            game_log.critical("there isn't enough spawn points on map '%s'", world.map_name)
            game_log.critical("abort")
            exit(1)

    game_log.info("waiting for %d players", players_num)
    accept_all_clients(players_num, world, sock)

    game_log.info("server started")
    game_log.info("game started")
    if not itb:
        game_log.info("game with %d players", players_num)
    else:
        game_log.info("team game with %d players", players_num)

    world.game_start()
    updater_process = Thread(target=updater, args=(world, sock))
    updater_process.daemon = True
    updater_process.start()
