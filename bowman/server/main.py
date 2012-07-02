# Copyright 2012 Andreev Alexander <carzil@yandex.ru>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.

import os
from random import choice
from socket import socket, error
import select
from threading import Thread
from configparser import ConfigParser
from argparse import ArgumentParser
from .exceptions import Restart, Exit
from .log import net_log, game_log
from .world import World
from .actors import Ranger, Tank, Damager, Mage

def setup_socket(host, port):
    sock = socket()
    net_log.info("socket has created")
    sock.bind((host, port))
    net_log.info("socket has binded")
    net_log.info("server is listening at %s:%d", host or "*", port)
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
    return os.path.join(directory, choice(files))

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
            raise

def start(map_path, players_num, sock, itb, config):
    is_map_dir = False
    if os.path.isdir(map_path):
        is_map_dir = True
        map_path = random_map(map_path)

    try:
        map_file = open(map_path, encoding="utf-8")
    except IOError:
        game_log.critical("map '%s' not found", map_path)
        game_log.critical("abort")
        exit(1)

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
    try:
        updater_process.start()
    except:
        raise

def main():
    game_log.info("run Bowman v1.0")
    arg_parser = ArgumentParser(description="Bowman is a client-server console game.\n"
    "See more: https://github.com/carzil/bowman")
    arg_parser.add_argument("-c", "--config", default="config.cfg")
    args = arg_parser.parse_args()
    
    config = ConfigParser(allow_no_value=True)
    config.read(args.config)

    host = config.get("general", "host", fallback="")
    port = config.getint("general", "port", fallback=9999)
    max_players = config.getint("game", "max_players", fallback=2)
    itb = config.getboolean("game", "is_team_battle", fallback=False)
    _map = config.get("game", "map")

    server_socket = setup_socket(host, port)
    while True:
        try:
            start(_map, max_players, server_socket, itb, config)
        except (Exit, Restart):
            pass
