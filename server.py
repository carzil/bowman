from game.server.log import game_log
from game.server.main import start

if __name__ == "__main__":
    game_log.info("run Bowman v1.0")
    while True:
        start()