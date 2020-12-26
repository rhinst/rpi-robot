from threading import Thread

from app.message_bus import Connection, CommandMessage


class Subsystem(Thread):
    message_bus: Connection

    def __init__(self, message_bus: Connection):
        super().__init__()
        self.message_bus = message_bus

    def run(self):
       while True:
           message = self.message_bus.get_message()
           if message.channel == "core.command":

