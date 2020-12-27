from threading import Thread
from typing import List, Dict
from time import sleep

from app.message_bus import Connection, CommandMessage
from app.command import Command


class Subsystem(Thread):
    message_bus: Connection
    commands: Dict[str, Command]

    def __init__(self, message_bus: Connection):
        super().__init__()
        self.message_bus = message_bus
        self.commands = {}
        for command in self.register_commands():
            self.commands[command.name] = command
        if len(self.commands) > 0:
            self.message_bus.subscribe("core.command")

    def register_commands(self) -> List[Command]:
        return []

    def process_command(self, msg: CommandMessage):
        if msg.command in self.commands:
            self.commands[msg.command].callback(msg)

    def run(self):
        message_processors = {"core.command": self.process_command}
        while True:
            msg = self.message_bus.get_message()
            if msg:
                message_processors[msg.channel](msg)
            sleep(0.001)
