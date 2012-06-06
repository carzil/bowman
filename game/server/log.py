import logging

LOG_FORMAT = "[%(name)s(%(levelname)s)]: %(message)s"
logging.basicConfig(format=LOG_FORMAT)
net_log = logging.getLogger("net")
net_log.setLevel(logging.DEBUG)
game_log = logging.getLogger("server")
game_log.setLevel(logging.DEBUG)