from time import sleep
from threading import Thread
from itertools import cycle

from app.message_bus import Connection


class Api(Thread):
    message_bus: Connection

    def __init__(self, message_bus: Connection):
        super().__init__()
        self.message_bus = message_bus

    def run(self):
        while cycle([True]):
            sleep(0.001)
