from time import sleep
from threading import Thread

from app.message_bus import Connection


class VoiceController(Thread, Connection):
    messge_bus: Connection

    def __init__(self, message_bus: Connection):
        super().__init__()
        self.message_bus = message_bus

    def run(self):
        while True:
            sleep(0.001)
