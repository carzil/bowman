from configparser import ConfigParser
from game.server.exceptions import Exit, Restart
from game.server.log import game_log
from game.server.main import start, setup_socket
from argparse import ArgumentParser

if __name__ == "__main__":
    game_log.info("run Bowman v1.0")
    arg_parser = ArgumentParser(description="Bowman is a client-server console game. "
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
