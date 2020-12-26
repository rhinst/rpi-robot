from time import sleep
from threading import Thread

from app.message_bus import MessageBusConnection


class VoiceController(Thread, MessageBusConnection):
    message_bus_connection: MessageBusConnection

    def __init__(self, message_bus_connection: MessageBusConnection):
        super().__init__()
        self.message_bus_connection = message_bus_connection

    def run(self):
        while True:
            sleep(0.001)
