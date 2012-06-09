import logging

LOG_FORMAT = "(%(levelname)s)[%(name)s]: %(message)s"
logging.basicConfig(format=LOG_FORMAT)
net_log = logging.getLogger("net")
net_log.setLevel(logging.DEBUG)
game_log = logging.getLogger("game")
game_log.setLevel(logging.DEBUG)
