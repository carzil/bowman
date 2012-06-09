from game.server.log import game_log
from game.server.main import start, setup_socket
from argparse import ArgumentParser

if __name__ == "__main__":
    game_log.info("run Bowman v1.0")
    arg_parser = ArgumentParser(description="Bowman is a client-server console game. "
    "See more: https://github.com/carzil/bowman")
    arg_parser.add_argument("map")
    arg_parser.add_argument("--port", default=9999, type=int)
    arg_parser.add_argument("--host", default="")
    arg_parser.add_argument("--players", default=2, type=int)
    args = arg_parser.parse_args()

    server_socket = setup_socket(args.host, args.port)
    while True:
        start(args.map, args.players, server_socket)