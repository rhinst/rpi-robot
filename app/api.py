from time import sleep
from itertools import cycle

from app.message_bus import Connection


def start_api(message_bus: Connection):
    while cycle([True]):
        sleep(0.001)
